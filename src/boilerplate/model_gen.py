import sys
from contextlib import ExitStack
from sqlalchemy.engine import create_engine, Engine
from sqlalchemy.schema import MetaData
from dotenv import load_dotenv
from typing import Optional, Set, Dict, Any
from dqs_logger import logger
from bods_db import BodsDB


try:
    import citext
except ImportError:
    citext = None

try:
    import geoalchemy2
except ImportError:
    geoalchemy2 = None

try:
    import pgvector.sqlalchemy
except ImportError:
    pgvector = None

if sys.version_info < (3, 10):
    from importlib_metadata import entry_points, version
else:
    from importlib.metadata import entry_points, version

load_dotenv()


def selected_tables_for_models() -> Set[str]:
    return set(
        [
            "dqs_checks",
            "dqs_report",
            "otc_inactiveservice",
            "organisation_txcfileattributes",
            "otc_service",
            "dqs_taskresults",
            "dqs_observationresults",
            "transmodel_service",
            "transmodel_service_service_patterns",
            "transmodel_servicepatternstop",
            "transmodel_stopactivity",
            "transmodel_vehiclejourney",
            "naptan_stoppoint",
            "transmodel_operatingprofile",
            "transmodel_operatingdatesexceptions",
            "transmodel_nonoperatingdatesexceptions",
            "transmodel_servicedorganisationvehiclejourney",
            "transmodel_servicedorganisationworkingdays",
            "transmodel_servicedorganisations",
        ]
    )


def generate_model_file(generator: Any, outfile: str) -> None:
    # Open the target file (if given)
    logger.info("Generating model file")
    with ExitStack() as stack:
        with open(outfile, "w", encoding="utf-8") as fpoutfile:
            stack.enter_context(fpoutfile)
            # Write the generated model code to the specified file or standard output
            fpoutfile.write(generator.generate())
    logger.info(f"Model file generated {outfile}")


def open_db_connection() -> Optional[Engine]:
    db: BodsDB = BodsDB()
    connection_details: Dict[str, str] = db._get_connection_details()
    url: Optional[str] = db._generate_connection_string(**connection_details)
    logger.info("Created db connection")
    if not url:
        print("You must supply a url\n", file=sys.stderr)
        return None
    if citext:
        print(f"Using sqlalchemy-citext {version('citext')}")

    if geoalchemy2:
        print(f"Using geoalchemy2 {version('geoalchemy2')}")

    if pgvector:
        print(f"Using pgvector {version('pgvector')}")

    return create_engine(url)


def validate_tables(metadata: MetaData) -> None:
    """Validate if all required tables exist in the database."""
    logger.info("Validating tables")
    required_tables: Set[str] = set(metadata.tables.keys())
    existing_tables: Set[str] = selected_tables_for_models()
    missing_tables: Set[str] = existing_tables - required_tables

    if missing_tables:
        logger.error(f"Tables not found in db: {missing_tables}")
        raise ValueError(f"Tables not found in db: {missing_tables}")
    logger.info("All tables found")


def sqlalchmy_model_generator() -> None:
    """
    Generate SQLAlchemy models for the specified tables.
    If no tables are specified, generate models for all tables.
    """
    generators: Dict[str, Any] = {
        ep.name: ep for ep in entry_points(group="sqlacodegen.generators")
    }
    options: tuple = ("noindexes",)
    generator: str = "declarative"
    outfile: str = "src/boilerplate/models.py"
    # Use reflection to fill in the metadata
    engine: Optional[Engine] = open_db_connection()
    if not engine:
        logger.error("Failed to open db connection")
        return
    metadata: MetaData = MetaData()
    metadata.reflect(bind=engine, only=selected_tables_for_models())
    validate_tables(metadata)
    logger.info("Generating models")
    # Instantiate the generator
    generator_class: Any = generators[generator].load()
    generator_instance: Any = generator_class(metadata, engine, options)
    generate_model_file(generator_instance, outfile)


sqlalchmy_model_generator()
