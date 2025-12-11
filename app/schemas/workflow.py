from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime

# Request Schema
class WorkflowTestRequest(BaseModel):
    title: str = Field(..., description="标题")
    params: Dict[str, Any] = Field(..., description="调用参数对象")
    refer_sql: str = Field(..., description="参考sql语句")
    test_count: int = Field(..., description="测试次数", ge=1, le=20)

# Stream Response Schema
class WorkflowTestStreamItem(BaseModel):
    title: str = Field(..., description="标题")
    test_time: int = Field(..., description="测试次数")
    execute_dur: float = Field(..., description="执行时间")
    result: Dict[str, Any] = Field(..., description="执行结果对象")
    is_passed: Optional[bool] = Field(False, description="测试结果是否通过标记")

# History/Log List Schemas
class WorkflowTestHistoryItem(BaseModel):
    id: int = Field(..., description="测试日志id")
    title: str = Field(..., description="测试日志标题")
    created_at: datetime = Field(..., description="测试日志开始时间")

    class Config:
        from_attributes = True

class WorkflowTestHistoryResponse(BaseModel):
    code: int = Field(..., description="响应状态码，非0表示异常")
    message: str = Field(..., description="响应消息")
    history: List[WorkflowTestHistoryItem] = Field(..., description="测试历史日志")

# Detail Schemas
class WorkflowTestResultDetail(BaseModel):
    id: int = Field(..., description="测试内容id")
    test_index: int = Field(..., description="测试次数")
    execute_dur: float = Field(..., description="测试执行时长")
    result: Dict[str, Any] = Field(..., description="测试执行结果")
    is_passed: Optional[bool] = Field(False, description="测试结果是否通过标记")

class WorkflowTestDetailResponse(BaseModel):
    test_result: List[WorkflowTestResultDetail] = Field(..., description="测试结果列表")

class WorkflowTestResultUpdate(BaseModel):
    is_passed: bool = Field(..., description="测试是否通过")
