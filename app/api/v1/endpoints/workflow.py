import json
import random
import asyncio

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.schemas.workflow import WorkflowTestRequest, WorkflowTestHistoryResponse, WorkflowTestDetailResponse, WorkflowTestResultUpdate, WorkflowTestResultDetail
from app.services import workflow_service
from typing import List

router = APIRouter()

@router.post("/test/stream", summary="请求测试")
async def test_workflow_stream(request: WorkflowTestRequest):
    # Use a queue to decouple processing from streaming response
    queue = asyncio.Queue()

    async def background_task():
        try:
            # Create a new session for the background task
            # Local import to avoid circular dependency issues if any, 
            # but typically standard imports are fine. 
            # Ensuring we use a fresh session that outlives the request.
            from app.db.session import AsyncSessionLocal
            async with AsyncSessionLocal() as db:
                async for item in workflow_service.run_workflow_test_stream(db, request):
                    await queue.put(item)
        except Exception as e:
            print(f"Error in background workflow: {e}")
        finally:
            await queue.put(None) # Sentinel to signal completion

    # Start the background task
    asyncio.create_task(background_task())

    async def event_generator():
        while True:
            item = await queue.get()
            if item is None:
                break
            yield json.dumps(item, ensure_ascii=False) + "\n"

    return StreamingResponse(event_generator(), media_type="application/x-ndjson")

@router.get("/logs", response_model=WorkflowTestHistoryResponse, summary="拉取测试日志")
async def get_logs(page: int = 1, page_size: int = 10, db: AsyncSession = Depends(get_db)):
    skip = (page - 1) * page_size
    history = await workflow_service.get_workflow_history(db, skip=skip, limit=page_size)

    return {
        "code": 0,
        "message": "success",
        "history": history
    }

@router.get("/logs/{test_id}", response_model=WorkflowTestDetailResponse, summary="拉取测试记录详情")
async def get_log_detail(test_id: int, db: AsyncSession = Depends(get_db)):
    results = await workflow_service.get_workflow_detail(db, test_id)
    # Map SQLAlchemy objects to Pydantic models
    mapped_results = []
    for r in results:
        mapped_results.append(WorkflowTestResultDetail(
            id=r.id,
            test_index=r.test_index,
            execute_dur=r.execute_dur,
            result=r.result,
            is_passed=r.is_passed
        ))

    return {"test_result": mapped_results}

@router.put("/results/{result_id}", response_model=dict, summary="更新检查结果是否通过")
async def update_result_status(result_id: int, update_data: WorkflowTestResultUpdate, db: AsyncSession = Depends(get_db)):
    result = await workflow_service.update_test_result_status(db, result_id, update_data.is_passed)
    if not result:
        return {"code": 404, "message": "Result not found"}

    return {"code": 0, "message": "success"}
