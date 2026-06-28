import logging
from pipeline.runner.pipeline_runner import PipelineRunner
from pipeline.registry.source_registry import SourceRegistry


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

def main():
    runner = PipelineRunner()
    for source in SourceRegistry.get_sources():
        runner.run(source)

if __name__ == "__main__":
    main()