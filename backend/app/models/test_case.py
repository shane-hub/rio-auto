from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
import enum
from app.core.database import Base
from app.models.base import TimestampMixin

class TestType(str, enum.Enum):
    API = "api"
    UI = "ui"
    PERFORMANCE = "performance"

class TestCase(Base, TimestampMixin):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    type = Column(String, nullable=False)  # api, ui, performance
    
    # Store type-specific data (request details, scripts, performance config)
    # For API: { method: "GET", url: "...", headers: {}, body: {}, assertions: [] }
    # For UI: { script: "...", browser: "chromium" }
    # For Performance: { users: 10, duration: 60 }
    data = Column(JSON, nullable=False, default={})
    
    project = relationship("Project", backref="test_cases")
