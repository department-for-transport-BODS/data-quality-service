from src.boilerplate.common import BodsDB
from unittest.mock import patch
from os import environ
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

# TODO: Remove - there is no boilerplate client, are we testing secrets manager because it's not in use?
# @patch("src.boilerplate.common.client")
# @patch.dict(environ, ENVIRONMENT_INPUT_TEST_VALUES)
# def test_connection_details_valid(mocked_client):
#     mocked_client.return_value.get_secret_value.return_value = {
#         "SecretString": "my_password"
#     }
#     db = BodsDB()
#     assert db._get_connection_details() == ENVIRONMENT_OUTPUT_TEST_VALUES
#
#
# environment_missing_test_values = dict(ENVIRONMENT_INPUT_TEST_VALUES)
# environment_missing_test_values.pop("POSTGRES_HOST")

# TODO: Remove - there is no boilerplate client, are we testing secrets manager because it's not in use?
# @patch("src.boilerplate.common.client")
# @patch.dict(environ, environment_missing_test_values)
# def test_connection_details_missing(mocked_client, caplog):
#     mocked_client.return_value.get_secret_value.return_value = {
#         "SecretString": "my_password"
#     }
#     db = BodsDB()
#     with raises(ValueError):
#         print(db._get_connection_details())
#     assert "POSTGRES_HOST" in caplog.text


@patch(
    "src.boilerplate.common.BodsDB._get_connection_details",
    return_value=ENVIRONMENT_OUTPUT_TEST_VALUES,
)
@patch("src.boilerplate.common.create_engine")
@patch("src.boilerplate.common.Session")
def test_database_initialization(
    session, create_engine, connection_details
):
    """Test database initialization."""
    connection_details.return_value = ENVIRONMENT_INPUT_TEST_VALUES
    db = BodsDB()
    db._initialise_database()
    assert connection_details.called
    create_engine.assert_called_with(
        f"postgresql+psycopg2:///?POSTGRES_HOST={ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_HOST']}&"
        f"POSTGRES_DB={ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_DB']}&"
        f"POSTGRES_USER={ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_USER']}&"
        f"POSTGRES_PORT={ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_PORT']}&"
        f"POSTGRES_PASSWORD={ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_PASSWORD']}"
    )
    session.assert_called_with(create_engine())
    assert db.session is not None


@patch(
    "src.boilerplate.common.BodsDB._get_connection_details",
    return_value=ENVIRONMENT_OUTPUT_TEST_VALUES,
)
@patch("src.boilerplate.common.create_engine")
@patch("src.boilerplate.common.Session", side_effect=OperationalError())
def test_database_initialisation_failed(
    _, __, ___, caplog
):
    """Test database initialization failure."""
    db = BodsDB()
    with raises(OperationalError):
        db._initialise_database()
    assert "Failed to connect to DB" in caplog.text
