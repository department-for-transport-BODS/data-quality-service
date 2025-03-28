import sys
import os
from sqlalchemy import (
    MetaData,
    create_engine,
)

# Add the parent directory of 'data_quality_service' to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sqlalchemy.orm import Session
from types import SimpleNamespace
from src.boilerplate.models import DataQualityTaskresults, DataQualityObservationresults, OrganisationTxcfileattributes, DataQualityReport

class MockedDB:
    def __init__(self):
        engine = create_engine("sqlite:///:memory:")
        self.session = Session(engine)
        metadata = MetaData()
        metadata.reflect(bind=engine)
        metadata.create_all(engine)
        self.classes = SimpleNamespace(
            dqs_taskresults=DataQualityTaskresults,
            dqs_observationresults=DataQualityObservationresults,
            organisation_txcfileattributes=OrganisationTxcfileattributes,
            data_quality_report=DataQualityReport
        )


if __name__ == "__main__":
    DB = MockedDB()
    print(DB.classes)
