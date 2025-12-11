import time
import asyncio
import random
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select
from app.models.workflow import WorkflowTest, WorkflowTestResult
from app.schemas.workflow import WorkflowTestRequest

async def execute_workflow_mock(params: dict) -> dict:
    """
    Simulate workflow execution.
    """
    dur = random.uniform(0.1, 1.0)
    await asyncio.sleep(dur)
    return {
        "status": "success", 
        "echo_params": params, 
        "generated_value": random.randint(1, 1000)
    }

async def run_workflow_test_stream(db: AsyncSession, request: WorkflowTestRequest):
    """
    Generator that runs tests and streams results.
    """
    # Create parent record
    db_test = WorkflowTest(
        title=request.title,
        params=request.params,
        refer_sql=request.refer_sql,
        test_count=request.test_count,
    )
    db.add(db_test)
    await db.commit()
    await db.refresh(db_test)

    for i in range(1, request.test_count + 1):
        start_time = time.time()
        # Execute mock workflow
        result_data = await execute_workflow_mock(request.params)
        end_time = time.time()
        duration = end_time - start_time

        # Save result to DB
        db_result = WorkflowTestResult(
            workflow_test_id=db_test.id,
            test_index=i,
            execute_dur=duration,
            result=result_data,
            is_passed=False
        )
        db.add(db_result)
        await db.commit()

        # Yield response
        yield {
            "title": request.title,
            "test_time": i,
            "execute_dur": duration,
            "result": result_data,
            "is_passed": False
        }

async def get_workflow_history(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(WorkflowTest).order_by(desc(WorkflowTest.created_at)).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_workflow_detail(db: AsyncSession, test_id: int):
    stmt = select(WorkflowTestResult).filter(WorkflowTestResult.workflow_test_id == test_id).order_by(WorkflowTestResult.test_index)
    result = await db.execute(stmt)
    return result.scalars().all()

async def update_test_result_status(db: AsyncSession, result_id: int, is_passed: bool) -> Optional[WorkflowTestResult]:
    stmt = select(WorkflowTestResult).filter(WorkflowTestResult.id == result_id)
    result = await db.execute(stmt)
    db_result = result.scalars().first()
    
    if db_result:
        db_result.is_passed = is_passed
        await db.commit()
        await db.refresh(db_result)
    return db_result
