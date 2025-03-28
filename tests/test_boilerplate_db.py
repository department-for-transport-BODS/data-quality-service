from src.boilerplate.common import BodsDB
from unittest.mock import patch
from pytest import raises
from psycopg2.errors import OperationalError

ENVIRONMENT_INPUT_TEST_VALUES = {
    "POSTGRES_HOST": "host",
    "POSTGRES_DB": "db",
    "POSTGRES_USER": "user",
    "POSTGRES_PORT": "5432",
    "POSTGRES_PASSWORD": "my_password",
}

ENVIRONMENT_OUTPUT_TEST_VALUES = {
    "POSTGRES_HOST": "host",
    "POSTGRES_DB": "db",
    "POSTGRES_USER": "user",
    "POSTGRES_PORT": "5432",
    "POSTGRES_PASSWORD": "my_password",
}


@patch(
    "src.boilerplate.bods_db.BodsDB._get_connection_details",
    return_value=ENVIRONMENT_OUTPUT_TEST_VALUES,
)
@patch("src.boilerplate.bods_db.create_engine")
@patch("src.boilerplate.bods_db.Session")
def test_database_initialization(mock_session, mock_create_engine, mock_connection_details):
    """Test successful database initialization."""
    db = BodsDB()
    db._initialise_database()

    # Assert connection details were fetched
    mock_connection_details.assert_called_once()

    # Assert create_engine was called with the correct connection string
    mock_create_engine.assert_called_once_with(
        f"postgresql+psycopg2://{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_USER']}:"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_PASSWORD']}@"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_HOST']}:"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_PORT']}/"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_DB']}"
    )

    # Assert session was initialized
    mock_session.assert_called_once_with(bind=mock_create_engine())
    assert db.session is not None


@patch(
    "src.boilerplate.bods_db.BodsDB._get_connection_details",
    return_value=ENVIRONMENT_OUTPUT_TEST_VALUES,
)
@patch("src.boilerplate.bods_db.create_engine")
@patch("src.boilerplate.bods_db.Session", side_effect=OperationalError())
def test_database_initialisation_failed(mock_session, mock_create_engine, mock_connection_details, caplog):
    """Test database initialization failure."""
    db = BodsDB()
    with raises(OperationalError):
        db._initialise_database()

    # Assert the error message is logged
    assert "Failed to connect to DB" in caplog.text


@patch(
    "src.boilerplate.bods_db.BodsDB._get_connection_details",
    return_value=None,
)
def test_missing_connection_details(mock_connection_details):
    """Test database initialization with missing connection details."""
    db = BodsDB()
    with raises(ValueError, match="Missing connection details"):
        db._initialise_database()


@patch(
    "src.boilerplate.bods_db.BodsDB._get_connection_details",
    return_value={
        "POSTGRES_HOST": "host",
        "POSTGRES_DB": "db",
        "POSTGRES_USER": "user",
        "POSTGRES_PORT": "invalid_port",  # Invalid port
        "POSTGRES_PASSWORD": "my_password",
    },
)
@patch("src.boilerplate.bods_db.create_engine")
def test_invalid_connection_details(mock_create_engine, mock_connection_details):
    """Test database initialization with invalid connection details."""
    db = BodsDB()
    with raises(ValueError, match="Invalid connection details"):
        db._initialise_database()