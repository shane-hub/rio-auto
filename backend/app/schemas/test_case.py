from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from datetime import datetime
from enum import Enum

class TestType(str, Enum):
    API = "api"
    UI = "ui"
    PERFORMANCE = "performance"

class AssertionType(str, Enum):
    STATUS_CODE = "status_code"
    JSON_PATH = "json_path"
    RESPONSE_TIME = "response_time"
    TEXT_CONTAINS = "text_contains"

class AssertionRule(BaseModel):
    type: AssertionType
    expression: Optional[str] = None # e.g. $.data.id for JSON_PATH
    operator: str = "eq" # eq, gt, lt, contains
    value: Any

class ExtractionRule(BaseModel):
    name: str
    expression: str # $.data.token
    source: str = "json" # json, header, cookie

class ApiRequestData(BaseModel):
    method: str
    url: str
    headers: Optional[Dict[str, str]] = {}
    body: Optional[Union[Dict[str, Any], str]] = None
    params: Optional[Dict[str, Any]] = None
    assertions: List[AssertionRule] = []
    extractions: List[ExtractionRule] = []

class UiScriptData(BaseModel):
    url: str
    steps: List[Dict[str, Any]] = [] # Recording steps
    browser: str = "chromium"

class TestCaseBase(BaseModel):
    name: str
    description: Optional[str] = None
    type: TestType
    data: Dict[str, Any] = Field(default_factory=dict) # Holds type-specific data

class TestCaseCreate(TestCaseBase):
    project_id: int

class TestCase(TestCaseBase):
    id: int
    project_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
