from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.core.database import get_db
from app.models.test_case import TestCase as TestCaseModel
from app.schemas.test_case import TestCase, TestCaseCreate

router = APIRouter()

@router.post("/", response_model=TestCase)
async def create_test_case(test_case: TestCaseCreate, db: AsyncSession = Depends(get_db)):
    # Verify project exists
    # For brevity skipping explicit project check, but normally would do it.
    
    db_test_case = TestCaseModel(**test_case.model_dump())
    db.add(db_test_case)
    await db.commit()
    await db.refresh(db_test_case)
    return db_test_case

@router.get("/", response_model=List[TestCase])
async def read_test_cases(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(TestCaseModel).offset(skip).limit(limit))
    test_cases = result.scalars().all()
    return test_cases
