from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db, AsyncSessionLocal
from app.models.task import TestTask, TaskStatus
from app.models.test_case import TestCase
from app.models.project import Project
from app.services.task_runner import TaskRunner
from app.models.report import TestReport

router = APIRouter()

class ExecutionRequest(BaseModel):
    project_id: int
    case_ids: Optional[List[int]] = None
    env: str = "dev"

async def execute_task_background(task_id: int, case_ids: List[int]):
    async with AsyncSessionLocal() as db:
        # Fetch cases within the new session
        if not case_ids:
            return

        result = await db.execute(select(TestCase).where(TestCase.id.in_(case_ids)))
        cases = result.scalars().all()
        
        runner = TaskRunner(task_id, cases)
        await runner.run(db)

@router.post("/project", status_code=202)
async def run_project_tests(
    req: ExecutionRequest, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    # Verify project exists
    project = await db.get(Project, req.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # Determine cases to run
    query = select(TestCase).where(TestCase.project_id == req.project_id)
    if req.case_ids:
        query = query.where(TestCase.id.in_(req.case_ids))
    
    result = await db.execute(query)
    cases = result.scalars().all()
    
    if not cases:
        raise HTTPException(status_code=400, detail="No test cases found to run")

    case_ids = [c.id for c in cases]

    # Create Task Record
    task = TestTask(
        project_id=req.project_id,
        trigger_type="manual",
        status=TaskStatus.PENDING
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)

    # Trigger Background Execution
    background_tasks.add_task(execute_task_background, task.id, case_ids)

    return {"message": "Task queued", "task_id": task.id}

@router.get("/", response_model=List[dict])
async def list_tasks(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TestTask).order_by(TestTask.created_at.desc()).offset(skip).limit(limit)
    )
    tasks = result.scalars().all()
    # Simple serialization (or use Pydantic schema)
    return [
        {
            "id": t.id, 
            "project_id": t.project_id, 
            "status": t.status, 
            "created_at": t.created_at,
            "completed_at": t.completed_at
        } 
        for t in tasks
    ]

@router.get("/reports", response_model=List[dict])
async def list_reports(skip: int = 0, limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(TestReport).order_by(TestReport.created_at.desc()).offset(skip).limit(limit)
    )
    reports = result.scalars().all()
    return [
        {
            "id": r.id,
            "task_id": r.task_id,
            "total_cases": r.total_cases,
            "passed": r.passed,
            "failed": r.failed,
            "duration": r.duration,
            "created_at": r.created_at
        }
        for r in reports
    ]
