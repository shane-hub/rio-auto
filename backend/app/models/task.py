from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from app.core.database import Base
from app.models.base import TimestampMixin

class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class TestTask(Base, TimestampMixin):
    __tablename__ = "test_tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    # Can be linked to a suite or specific cases, for simplicity we store a list of case_ids in execution_data or similar
    # Or just run all cases in a project for now, or use a many-to-many. 
    # Let's assume we pass a list of case_ids to run.
    trigger_type = Column(String, default="manual") # manual, scheduled, ci
    status = Column(String, default=TaskStatus.PENDING)
    
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    
    project = relationship("Project", backref="tasks")
