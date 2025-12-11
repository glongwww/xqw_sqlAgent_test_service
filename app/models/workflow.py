from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class WorkflowTest(Base):
    __tablename__ = "workflow_tests"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    params = Column(JSON)
    refer_sql = Column(String)
    test_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.now)

    results = relationship("WorkflowTestResult", back_populates="workflow_test")

class WorkflowTestResult(Base):
    __tablename__ = "workflow_test_results"

    id = Column(Integer, primary_key=True, index=True)
    workflow_test_id = Column(Integer, ForeignKey("workflow_tests.id"))
    test_index = Column(Integer)
    execute_dur = Column(Float)
    result = Column(JSON)
    is_passed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    workflow_test = relationship("WorkflowTest", back_populates="results")
