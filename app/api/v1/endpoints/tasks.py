from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.api.v1.endpoints.auth import get_current_user
from app.db.session import get_db
from app.models.models import User, Task, TaskStatus, TaskPriority
from app.schemas.schemas import TaskCreate, Task as TaskSchema

router = APIRouter()

def calculate_user_workload(db: Session, user_id: int) -> float:
    """Calculate the current workload of a user based on their active tasks."""
    active_tasks = db.query(Task).filter(
        Task.assignee_id == user_id,
        Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])
    ).all()
    
    workload_score = 0
    for task in active_tasks:
        # Higher priority tasks contribute more to workload
        priority_weights = {
            TaskPriority.LOW: 1,
            TaskPriority.MEDIUM: 2,
            TaskPriority.HIGH: 3,
            TaskPriority.URGENT: 4
        }
        workload_score += priority_weights[task.priority]
    
    return workload_score

def find_optimal_assignee(db: Session, task: TaskCreate) -> User:
    """Find the optimal user to assign a task to based on workload and expertise."""
    # Get all users who are members of the project's team
    team_members = db.query(User).join(
        User.team_memberships
    ).filter(
        User.team_memberships.any(team_id=task.project_id)
    ).all()
    
    if not team_members:
        raise HTTPException(
            status_code=400,
            detail="No team members found for this project"
        )
    
    # Calculate workload scores for each team member
    member_scores = []
    for member in team_members:
        workload = calculate_user_workload(db, member.id)
        member_scores.append((member, workload))
    
    # Sort by workload (ascending) and return the user with the lowest workload
    member_scores.sort(key=lambda x: x[1])
    return member_scores[0][0]

@router.post("/", response_model=TaskSchema)
def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Create new task with intelligent assignment.
    """
    # If no assignee is specified, find the optimal one
    if not task_in.assignee_id:
        optimal_assignee = find_optimal_assignee(db, task_in)
        task_in.assignee_id = optimal_assignee.id
    
    task = Task(**task_in.dict())
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=List[TaskSchema])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Retrieve tasks.
    """
    tasks = db.query(Task).offset(skip).limit(limit).all()
    return tasks

@router.get("/{task_id}", response_model=TaskSchema)
def read_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Get task by ID.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskSchema)
def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Update task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    for field, value in task_in.dict().items():
        setattr(task, field, value)
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", response_model=TaskSchema)
def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    """
    Delete task.
    """
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    db.delete(task)
    db.commit()
    return task 