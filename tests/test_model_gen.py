import runpy
from importlib.metadata import version
from pathlib import Path
from unittest.mock import patch


@patch("sqlalchemy.engine.create_engine", return_value=None)
@patch("bods_db.BodsDB")
def test_model_generator_loads_citext_metadata(mock_db, mock_create_engine, capsys):
    mock_db.return_value._get_connection_details.return_value = {}
    mock_db.return_value._generate_connection_string.return_value = "postgresql://test"

    runpy.run_path(
        str(Path(__file__).resolve().parents[1] / "src/boilerplate/model_gen.py")
    )

    assert (
        f"Using sqlalchemy-citext {version('sqlalchemy-citext')}"
        in capsys.readouterr().out
    )
    mock_create_engine.assert_called_once_with("postgresql://test")
