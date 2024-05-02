from sqlalchemy import Column, Integer, String, TIMESTAMP, Date, Boolean, create_engine
from sqlalchemy.orm import Session, declarative_base
from types import SimpleNamespace

Base = declarative_base()

class data_quality_taskresult(Base):
    __tablename__ = 'data_quality_taskresult'
    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP)
    modified = Column(TIMESTAMP)
    status = Column(String)
    checks_id = Column(Integer)
    dataquality_report_id = Column(Integer)
    transmodel_txcfileattributes_id = Column(Integer)


class data_quality_observationresults(Base):
    __tablename__ = 'data_quality_observationresults'
    id = Column(Integer, primary_key=True)
    details = Column(String)
    dataquality_report_id = Column(Integer)
    taskresults_id = Column(Integer)
    vehicle_journey_id = Column(Integer)


class organisation_txcfileattributes(Base):
    __tablename__ = 'organisation_txcfileattributes'
    id = Column(Integer, primary_key=True)
    schema_version = Column(String)
    revision_number = Column(Integer)
    creation_datetime = Column(TIMESTAMP)
    modification_datetime = Column(TIMESTAMP)
    filename = Column(String)
    service_= Column(String)
    revision_id = Column(Integer)
    modification = Column(String)
    national_operator_code = Column(String)
    licence_number = Column(String)
    operating_period_end_date = Column(Date)
    operating_period_start_date = Column(Date)
    public_use = Column(Boolean)
    line_names = Column(String)
    destination = Column(String)
    origin = Column(String)
    hash = Column(String)

class data_quality_report(Base):
    __tablename__ = 'data_quality_report'
    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP)
    file_name = Column(String)
    revision_id = Column(Integer)
    status = Column(String)


class MockedDB:
    def __init__(self):
        engine = create_engine("sqlite:///:memory:")
        self.session = Session(engine)
        Base.metadata.create_all(engine)
        self.classes = SimpleNamespace(
            data_quality_taskresult = data_quality_taskresult,
            data_quality_observationresults = data_quality_observationresults,
            organisation_txcfileattributes = organisation_txcfileattributes,
            data_quality_report = data_quality_report
        )


if __name__ == "__main__":
    DB = MockedDB()
    print(DB.classes)
