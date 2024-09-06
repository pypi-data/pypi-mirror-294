import json
import logging
import os
from argparse import ArgumentParser, Namespace

import structlog

from lsa_cli_smdmrr.models import SourceFileAnnotations

from .annotation_parser import AnnotationParser, export_annotations_to_json
from .annotations_to_entities_converter import AnnotationsToEntitiesConverter
from .config import Config

logger: structlog.BoundLogger = structlog.get_logger()
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.INFO))


def _parse_command(path: str, config: Config) -> None:
    logger.info("Parsing annotations from source code...")
    parser: AnnotationParser = AnnotationParser(
        config.parser_exclude, config.annotation_prefix, config.extensions_map
    )

    model: list[SourceFileAnnotations] = parser.parse(path)
    if not model:
        logger.info("No annotations found to save.")
        return

    output: str = config.output_annotations_file
    logger.info(f"Saving annotations to '{output}'")
    export_annotations_to_json(model, output)


def _convert_command(config: Config, save_annotations: bool) -> None:
    logger.info("Converting annotations to entities...")
    converter = AnnotationsToEntitiesConverter(config.annotations_markers_map)

    if not os.path.exists(config.output_annotations_file):
        logger.error(f"Annotations file not found: '{config.output_annotations_file}'")
        return

    with open(config.output_annotations_file, "r") as f:
        annotations = json.load(f)

    entities = converter.convert(annotations)
    if not save_annotations:
        os.remove(config.output_annotations_file)

    if not entities:
        logger.info("No entities found to save.")
        return

    with open(config.output_entities_file, "w") as f:
        logger.info(f"Saving entities to '{config.output_entities_file}'")
        json.dump(entities, f, indent=4)


def run() -> None:
    # Commands for parse annotations, convert annotations to entities and save entities as enum
    parser: ArgumentParser = ArgumentParser(
        description="Parses annotations from source code and convert them to entities."
    )
    parser.add_argument(
        "path",
        help="Path to file or directory to parse",
        type=str,
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Path to the configuration file",
        type=str,
    )
    parser.add_argument(
        "-a",
        "--annotations",
        help="Parsed annotations will be saved to file if this flag is set",
        action="store_true",
    )

    args: Namespace = parser.parse_args()
    config: Config = Config.from_file(args.config) if args.config else Config.from_default()
    _parse_command(args.path, config)
    _convert_command(config, args.annotations)
