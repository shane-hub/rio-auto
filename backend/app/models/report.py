from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.base import TimestampMixin

class TestReport(Base, TimestampMixin):
    __tablename__ = "test_reports"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("test_tasks.id"), nullable=False)
    
    total_cases = Column(Integer, default=0)
    passed_cases = Column(Integer, default=0)
    failed_cases = Column(Integer, default=0)
    skipped_cases = Column(Integer, default=0)
    
    # Detailed results
    details = Column(JSON, default=[]) # List of result objects per case
    
    # Performance metrics
    avg_response_time = Column(Float, nullable=True)
    error_rate = Column(Float, nullable=True)
    
    task = relationship("TestTask", backref="report")
