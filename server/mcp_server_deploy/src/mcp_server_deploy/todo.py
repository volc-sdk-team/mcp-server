import uuid

from typing import Dict, List, Optional
from enum import Enum
from pydantic import BaseModel

from .models import ApiResponse


class TodoStatus(Enum):
    NEW = "new"
    DONE = "done"


class TodoItem(BaseModel):
    content: str
    number: int
    status: TodoStatus = TodoStatus.NEW


class Todo(BaseModel):
    todo_list: List[TodoItem]
    todo_id: str


# 全局存储todo items的字典，每个todo_id对应一个TodoItem数组
todo_storage: Dict[str, List[TodoItem]] = {}


def create_or_update(todos: List[str], todo_id: Optional[str] = None) -> Todo:
    found = False
    if todo_id and todo_id in todo_storage:
        max_number = len(todo_storage[todo_id])
        found = True
    else:
        todo_id = str(uuid.uuid4())
        max_number = 0

    tmp_todo_items = []
    for _, content in enumerate(todos):
        todo_item = TodoItem(content=content, number=max_number)
        tmp_todo_items.append(todo_item)
        max_number += 1

    if found:
        todo_storage[todo_id].extend(tmp_todo_items)
    else:
        todo_storage[todo_id] = tmp_todo_items

    return ApiResponse.success(Todo(todo_list=todo_storage[todo_id], todo_id=todo_id))


def update_status(todo_id: str, number: int, status: TodoStatus) -> Todo:
    if todo_id not in todo_storage:
        return ApiResponse.error(code="failed",message=f"todo_id {todo_id} not exist")

    # 获取todo列表
    todo_items = todo_storage[todo_id]
    found = False
    # 遍历查找对应number的todo项
    for todo_item in todo_items:
        if todo_item.number == number:
            # 更新状态
            todo_item.status = status
            found = True
            break
    
    if not found:
        return ApiResponse.error(code="failed", message=f"todo number {number} not exist")
    
    return ApiResponse.success(Todo(todo_list=todo_storage[todo_id], todo_id=todo_id))


def get_list(todo_id: Optional[str] = None) -> Todo:
    if todo_id and todo_id in todo_storage:
        return ApiResponse.success(
            Todo(todo_list=todo_storage[todo_id], todo_id=todo_id)
        )
    return ApiResponse.error(code="failed",message=f"todo_id {todo_id} not exist")
