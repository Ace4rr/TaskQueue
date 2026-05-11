from src.task_queue import TaskQueue
from src.models import Task
from datetime import datetime
import pytest

@pytest.fixture
def sample_tasks():
    task1=Task(id="1", description="Task 1", priority=1, status="todo", created_at=datetime.now())
    task2=Task(id="2", description="Task 2", priority=2, status="in-progress", created_at=datetime.now())
    task3=Task(id="3", description="Task 3", priority=3, status="todo", created_at=datetime.now())
    task4=Task(id="4", description="Task 4", priority=1, status="done", created_at=datetime.now())
    return [task1, task2, task3, task4]

def test_task_queue_add_and_len(sample_tasks):
    queue=TaskQueue()
    assert len(queue)==0
    queue.add(sample_tasks[0])
    assert len(queue)==1
    queue.add(sample_tasks[1])
    assert len(queue)==2

def test_task_queue_iter(sample_tasks):
    queue=TaskQueue()
    queue.add(sample_tasks[0])
    queue.add(sample_tasks[1])
    retrieved_tasks=list(queue)
    assert len(retrieved_tasks)==2
    assert retrieved_tasks[0]==sample_tasks[0]
    assert retrieved_tasks[1]==sample_tasks[1]

def test_task_queue_filter_by_status(sample_tasks):
    queue=TaskQueue()
    for task in sample_tasks:
        queue.add(task)
    todo_tasks=list(queue.filter_by_status("todo"))
    assert len(todo_tasks)==2
    assert todo_tasks[0].id=="1"
    assert todo_tasks[1].id=="3"
    done_tasks=list(queue.filter_by_status("done"))
    assert len(done_tasks)==1
    assert done_tasks[0].id=="4"
    empty_tasks=list(queue.filter_by_status("blocked"))
    assert len(empty_tasks)==0

def test_task_queue_filter_by_priority(sample_tasks):
    queue=TaskQueue()
    for task in sample_tasks:
        queue.add(task)
    high_priority_tasks=list(queue.filter_by_priority(2))
    assert len(high_priority_tasks)==2
    assert high_priority_tasks[0].id=="2"
    assert high_priority_tasks[1].id=="3"
    min_priority_1_tasks=list(queue.filter_by_priority(1))
    assert len(min_priority_1_tasks)==4
    min_priority_5_tasks=list(queue.filter_by_priority(5))
    assert len(min_priority_5_tasks)==0

def test_task_queue_filter_by_status_and_priority(sample_tasks):
    queue=TaskQueue()
    for task in sample_tasks:
        queue.add(task)

    todo_high_priority_tasks=list(queue.filter_by_status_and_priority("todo", 2))
    assert len(todo_high_priority_tasks)==1
    assert todo_high_priority_tasks[0].id=="3"

    in_progress_tasks=list(queue.filter_by_status_and_priority("in-progress", 1))
    assert len(in_progress_tasks)==1
    assert in_progress_tasks[0].id=="2"

    no_match_tasks=list(queue.filter_by_status_and_priority("done", 3))
    assert len(no_match_tasks)==0 
