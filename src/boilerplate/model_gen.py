import boto3
import os
import sys
from contextlib import ExitStack
from typing import TextIO
from os import environ
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData
from dotenv import load_dotenv
import logging
import urllib

logger = logging.getLogger(__name__)

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


def _get_connection_details():
    """
    Method to get the connection details for the database from the environment variables
    """
    connection_details = {}
    connection_details["host"] = environ.get("POSTGRES_HOST")
    connection_details["dbname"] = environ.get("POSTGRES_DB")
    connection_details["user"] = environ.get("POSTGRES_USER")
    connection_details["port"] = environ.get("POSTGRES_PORT")
    try:
        if environ.get("PROJECT_ENV") != "local":
            logger.debug("Getting DB token")
            connection_details["password"] = _generate_rds_iam_auth_token(
                connection_details["host"],
                connection_details["port"],
                connection_details["user"],
            )
            logger.debug("Got DB token")
            connection_details["sslmode"] = "disable"
            # connection_details["sslmode"] = "require"
        else:
            logger.debug(
                "No password ARN found in environment variables, getting DB password direct"
            )
            connection_details["password"] = environ.get("POSTGRES_PASSWORD")
            logger.debug("Got DB password")
            connection_details["sslmode"] = "disable"

        for key, value in connection_details.items():
            if value is None:
                logger.error(f"Missing connection details value: {key}")
                raise ValueError
        return connection_details
    except Exception as e:
        logger.error("Failed to get connection details for database")
        raise e


def _generate_connection_string(**kwargs) -> str:
    """
    Generates an AWS RDS IAM authentication token for a given RDS instance.

    Parameters:
    - **kwargs (any): A dictionary of key/value pairs that correspond to the expected values below

    Returns:
    - str: The generated connection string from parsed key/value pairs
    """
    if "application_name" not in kwargs:
        lambda_function_name = os.environ.get("AWS_LAMBDA_FUNCTION_NAME")
    if lambda_function_name:
        kwargs["application_name"] = lambda_function_name

    user_password = ""
    if kwargs.get("user"):
        user_password += kwargs.get("user")
        if kwargs.get("password"):
            user_password += ":" + kwargs.get("password")
        user_password += "@"

    # Construct other parts
    other_parts = ""
    for key, value in kwargs.items():
        if key not in ["host", "port", "user", "password", "dbname"] and value:
            other_parts += f"{key}={value}&"

    # Construct the final connection string
    connection_string = f"postgresql+psycopg2://{user_password}{kwargs.get('host', '')}"
    if kwargs.get("port"):
        connection_string += f":{kwargs.get('port')}"
    connection_string += f"/{kwargs.get('dbname', '')}"
    if other_parts:
        connection_string += f"?{other_parts[:-1]}"

    return connection_string


def _generate_rds_iam_auth_token(host, port, username) -> str:
    """
    Generates an AWS RDS IAM authentication token for a given RDS instance.

    Parameters:
    - hostname (str): The endpoint of the RDS instance.
    - port (int): The port number for the RDS instance.
    - username (str): The database username.

    Returns:
    - str: The generated IAM authentication token if successful.
    - None: If an error occurs during token generation.
    """
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name="rds", region_name=environ.get("AWS_REGION")
        )
        token = client.generate_db_auth_token(
            DBHostname=host, DBUsername=username, Port=port
        )
        return urllib.parse.quote_plus(token)
    except Exception as e:
        logger.error(f"An error occurred while generating the IAM auth token: {e}")
        return None


def sqlalchmy_model_generator() -> None:
    generators = {ep.name: ep for ep in entry_points(group="sqlacodegen.generators")}
    connection_details = _get_connection_details()
    url = _generate_connection_string(**connection_details)
    options = ("noindexes",)
    generator = "declarative"
    outfile = "src/boilerplate/models.py"

    if not url:
        print("You must supply a url\n", file=sys.stderr)
        return

    if citext:
        print(f"Using sqlalchemy-citext {version('citext')}")

    if geoalchemy2:
        print(f"Using geoalchemy2 {version('geoalchemy2')}")

    if pgvector:
        print(f"Using pgvector {version('pgvector')}")

    # Use reflection to fill in the metadata
    engine = create_engine(url)
    metadata = MetaData()
    metadata.reflect(bind=engine)
    # Instantiate the generator
    generator_class = generators[generator].load()
    generator = generator_class(metadata, engine, options)

    # Open the target file (if given)
    with ExitStack() as stack:
        outfile: TextIO
        if outfile:
            outfile = open(outfile, "w", encoding="utf-8")
            stack.enter_context(outfile)
        else:
            outfile = sys.stdout

        # Write the generated model code to the specified file or standard output
        outfile.write(generator.generate())


sqlalchmy_model_generator()
