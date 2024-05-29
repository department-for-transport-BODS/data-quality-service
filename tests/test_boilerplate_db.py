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
    "POSTGRES_PASSWORD_ARN": "my_password_location_arn",
    "ENV": "local",
    "AWS_REGION": "eu-west-2"
}

ENVIRONMENT_OUTPUT_TEST_VALUES = {
    "POSTGRES_HOST": "host",
    "POSTGRES_DB": "db",
    "POSTGRES_USER": "user",
    "POSTGRES_PORT": "5432",
    "POSTGRES_PASSWORD": "my_password",
}


@patch("src.boilerplate.common.client")
@patch.dict(environ, ENVIRONMENT_INPUT_TEST_VALUES)
def test_connection_details_valid(mocked_client):
    mocked_client.return_value.get_secret_value.return_value = {
        "SecretString": "my_password"
    }
    db = BodsDB()
    assert db._get_connection_details() == ENVIRONMENT_OUTPUT_TEST_VALUES


environment_missing_test_values = dict(ENVIRONMENT_INPUT_TEST_VALUES)
environment_missing_test_values.pop("POSTGRES_HOST")


@patch("src.boilerplate.common.client")
@patch.dict(environ, environment_missing_test_values)
def test_connection_details_missing(mocked_client, caplog):
    mocked_client.return_value.get_secret_value.return_value = {
        "SecretString": "my_password"
    }
    db = BodsDB()
    with raises(ValueError):
        print(db._get_connection_details())
    assert "POSTGRES_HOST" in caplog.text


@patch(
    "src.boilerplate.common.BodsDB._get_connection_details",
    return_value=ENVIRONMENT_OUTPUT_TEST_VALUES,
)
@patch("src.boilerplate.common.create_engine")
@patch("src.boilerplate.common.automap_base")
@patch("src.boilerplate.common.Session")
def test_database_initialisation(
    connection_details, create_engine, automap_base, session
):
    # connection_details.return_value = ENVIRONMENT_INPUT_TEST_VALUES
    automap_base.prepare.return_value = True
    db = BodsDB()
    db._initialise_database()
    assert connection_details.called
    assert create_engine.called_with(
        f"postgresql+psycopg2://{ENVIRONMENT_INPUT_TEST_VALUES['POSTGRES_USER']}:"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_PASSWORD']}@"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_HOST']}:"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_PORT']}/"
        f"{ENVIRONMENT_OUTPUT_TEST_VALUES['POSTGRES_DB']}"
    )
    assert automap_base.called
    assert session.called_with(create_engine)
    assert db.session is not None
    assert db.classes is not None


@patch(
    "src.boilerplate.common.BodsDB._get_connection_details",
    return_value=ENVIRONMENT_OUTPUT_TEST_VALUES,
)
@patch("src.boilerplate.common.create_engine")
@patch("src.boilerplate.common.automap_base")
@patch("src.boilerplate.common.Session", side_effect=OperationalError())
def test_database_initialisation_failed(
    connection_details, create_engine, automap_base, session, caplog
):
    # connection_details.return_value = ENVIRONMENT_INPUT_TEST_VALUES
    automap_base.prepare.return_value = True
    db = BodsDB()
    with raises(OperationalError):
        db._initialise_database()
        assert "Failed to connect to DB" in caplog.text
