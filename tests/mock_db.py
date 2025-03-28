from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    Date,
    Boolean,
    Text,
    create_engine,
    ForeignKey,
)
from sqlalchemy.orm import Session, declarative_base, relationship
from types import SimpleNamespace

Base = declarative_base()


class dqs_taskresults(Base):
    __tablename__ = "dqs_taskresults"
    id = Column(Integer, primary_key=True)
    created = Column(TIMESTAMP)
    modified = Column(TIMESTAMP)
    status = Column(String)
    checks_id = Column(Integer)
    dataquality_report_id = Column(Integer)
    transmodel_txcfileattributes_id = Column(Integer)
    observations = relationship("dqs_observationresults", backref="taskresult")
    message = Column(Text)


class dqs_observationresults(Base):
    __tablename__ = "dqs_observationresults"
    id = Column(Integer, primary_key=True)
    details = Column(String)
    taskresults_id = Column(Integer, ForeignKey("dqs_taskresults.id"))
    vehicle_journey_id = Column(Integer)
    service_pattern_stop_id = Column(Integer)
    serviced_organisation_vehicle_journey_id = Column(Integer)
    is_suppressed = Column(Boolean)


class organisation_txcfileattributes(Base):
    __tablename__ = "organisation_txcfileattributes"
    id = Column(Integer, primary_key=True)
    schema_version = Column(String)
    revision_number = Column(Integer)
    creation_datetime = Column(TIMESTAMP)
    modification_datetime = Column(TIMESTAMP)
    filename = Column(String)
    service_ = Column(String)
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


class dqs_report(Base):
    __tablename__ = "dqs_report"
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
        self.session.commit()
        print(Base.metadata.tables.keys())
        self.classes = SimpleNamespace(
            dqs_taskresults=dqs_taskresults,
            dqs_observationresults=dqs_observationresults,
            organisation_txcfileattributes=organisation_txcfileattributes,
            dqs_report=dqs_report,
        )


if __name__ == "__main__":
    DB = MockedDB()
    print(DB.classes)
