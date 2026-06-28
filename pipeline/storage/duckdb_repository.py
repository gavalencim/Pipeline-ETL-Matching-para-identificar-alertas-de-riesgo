import json
import duckdb
from config.settings import DUCKDB_PATH
from pipeline.normalization.schemas import CanonicalSanction


class DuckDBRepository:
    """
    Repositorio responsable de la persistencia de registros canónicos.

    Responsabilidades:
    - Abrir la conexión con DuckDB.
    - Crear automáticamente la tabla si no existe.
    - Insertar uno o varios registros.
    - Consultar información básica de la base de datos.
    - Cerrar la conexión.

    El resto del proyecto nunca debe escribir SQL directamente.
    Toda la persistencia pasa por esta clase.
    """

    def __init__(self):
        # Inicializar la conexión y garantizar que exista la tabla.

        self.connection = duckdb.connect(str(DUCKDB_PATH))
        self.create_table()

    # Creacion de tablas

    def create_table(self):
        # Crear la tabla de sanciones si aún no existe.

        self.connection.execute(
            """
            CREATE TABLE IF NOT EXISTS sanctions (

                id_registro VARCHAR,
                fuente VARCHAR,
                tipo_sujeto VARCHAR,
                nombres VARCHAR,
                apellidos VARCHAR,
                aliases JSON,
                fecha_nacimiento VARCHAR,
                nacionalidad JSON,
                numero_documento VARCHAR,
                tipo_sancion VARCHAR,
                fecha_sancion VARCHAR,
                fecha_vencimiento VARCHAR,
                programa_sancion VARCHAR,
                codigo_referencia VARCHAR,
                url_referencia VARCHAR,
                comentarios VARCHAR,
                activo BOOLEAN,
                fecha_ingesta TIMESTAMP,
                hash_contenido VARCHAR,
                PRIMARY KEY (fuente, id_registro)
            )
            """
        )


    def _to_row(self, sanction: CanonicalSanction) -> list:
        """
        Convierte un CanonicalSanction en una fila compatible
        con DuckDB.

        Esto evita duplicar código entre insert() e insert_many().
        """

        return [

            sanction.id_registro,
            sanction.fuente,
            sanction.tipo_sujeto,
            sanction.nombres,
            sanction.apellidos,
            json.dumps(sanction.aliases),
            sanction.fecha_nacimiento,
            json.dumps(sanction.nacionalidad),
            sanction.numero_documento,
            sanction.tipo_sancion,
            sanction.fecha_sancion,
            sanction.fecha_vencimiento,
            sanction.programa_sancion,
            sanction.codigo_referencia,
            sanction.url_referencia,
            sanction.comentarios,
            sanction.activo,
            sanction.fecha_ingesta,
            sanction.hash_contenido
        ]

    # Insercion
    def insert(self, sanction: CanonicalSanction):
        # Insertar un único registro.

        self.connection.execute(
            """
            INSERT INTO sanctions
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            self._to_row(sanction)
        )

    def insert_many(self, sanctions: list[CanonicalSanction]):
        # Inserta múltiples registros utilizando executemany(),
        # mucho más eficiente para cargas masivas.

        if not sanctions:
            return

        rows = [self._to_row(sanction) for sanction in sanctions]

        self.connection.executemany(
            """
            INSERT INTO sanctions
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            rows
        )

    # Consultas
    def count_records(self) -> int:
        # Retornar la cantidad de registros almacenados

        result = self.connection.execute(
            """
            SELECT COUNT(*)
            FROM sanctions
            """
        ).fetchone()

        return result[0]

    # Cierre
    def close(self):
        """
        Cierra la conexión con DuckDB.
        """

        self.connection.close()

    # Indices
    def load_index(self) -> dict:
        """
        Carga los hashes existentes en memoria.
        Retorna:

        {
            ("OFAC", "4375"): "abc123...",
            ("OFAC", "4310"): "def456..."
        }
        """

        rows = self.connection.execute(
            """
            SELECT
                fuente,
                id_registro,
                hash_contenido, 
                activo
            FROM sanctions
            """
        ).fetchall()

        index = {}

        for fuente, id_registro, hash_contenido, activo in rows:

            index[(fuente, id_registro)] = {
                "hash": hash_contenido,
                "activo": activo
            }

        return index
    
    def update_many(self, sanctions: list[CanonicalSanction]):
        # Actualizar registros existentes cuyo contenido cambió.
        if not sanctions:
            return

        query = """
            UPDATE sanctions
            SET
                tipo_sujeto = ?,
                nombres = ?,
                apellidos = ?,
                aliases = ?,
                fecha_nacimiento = ?,
                nacionalidad = ?,
                numero_documento = ?,
                tipo_sancion = ?,
                fecha_sancion = ?,
                fecha_vencimiento = ?,
                programa_sancion = ?,
                codigo_referencia = ?,
                url_referencia = ?,
                comentarios = ?,
                activo = ?,
                fecha_ingesta = ?,
                hash_contenido = ?
            WHERE
                fuente = ?
                AND id_registro = ?
        """

        values = []

        for sanction in sanctions:

            values.append([
                sanction.tipo_sujeto,
                sanction.nombres,
                sanction.apellidos,
                json.dumps(sanction.aliases),
                sanction.fecha_nacimiento,
                json.dumps(sanction.nacionalidad),
                sanction.numero_documento,
                sanction.tipo_sancion,
                sanction.fecha_sancion,
                sanction.fecha_vencimiento,
                sanction.programa_sancion,
                sanction.codigo_referencia,
                sanction.url_referencia,
                sanction.comentarios,
                sanction.activo,
                sanction.fecha_ingesta,
                sanction.hash_contenido,
                sanction.fuente,
                sanction.id_registro,
            ])

        self.connection.executemany(query, values)


    def deactivate_missing( self, fuente: str, ids_presentes: set[str]):
        # Marcar como inactivos los registros que ya no aparecen en la fuente.

        rows = self.connection.execute(
            """
            SELECT id_registro
            FROM sanctions
            WHERE fuente = ?
            AND activo = TRUE
            """,
            [fuente]
        ).fetchall()

        ids_bd = {row[0] for row in rows}
        # Diferencia entre los IDs activos de la BD
        # y los que llegaron en esta ejecución.
        ids_desaparecidos = ids_bd - ids_presentes

        if not ids_desaparecidos:
            return 0

        self.connection.executemany(
            """
            UPDATE sanctions
            SET activo = FALSE
            WHERE fuente = ?
            AND id_registro = ?
            """,
            [
                [fuente, id_registro]
                for id_registro in ids_desaparecidos
            ]
        )

        return len(ids_desaparecidos)
    
    def delete_record(self, fuente: str, id_registro: str):
        """
        Elimina un registro específico.

        Se utiliza principalmente para pruebas automatizadas,
        garantizando que puedan ejecutarse múltiples veces.
        """

        self.connection.execute(
            """
            DELETE FROM sanctions
            WHERE fuente = ?
            AND id_registro = ?
            """,
            [fuente, id_registro]
        )