import logging 
import sys
from pathlib import Path
from .task_queue import TaskQueue
from .receiver import TaskReceiver
from .sources.generator_source import GeneratedTaskSource
from .sources.api_source import ApiTaskSource
from .sources.file_source import FileTaskSource

logger=logging.getLogger(__name__)

def _example_fetcher():
    return [
        {"id": "api-1", "description": "from api 1", "priority": 5, "status": "ready", "created_at": "2024-01-01T12:00:00"},
        {"id": "api-2", "description": "from api 2", "priority": 0, "status": "pending", "created_at": "2024-01-02T12:00:00"},
    ]

def main(argv:list[str] |None =None)->int:
    source=GeneratedTaskSource(count=8,base_priority=1)
    receiver=TaskReceiver(source)
    queue=TaskQueue()
    for task in receiver.load_tasks():
        queue.add(task)

    print("================All tasks, try 1:")
    logger.info(("================All tasks, try 1:"))
    for task in queue:
        print(task.id, task.status, task.priority)
    print("================All tasks, try 2")
    logger.info(("================All tasks, try 2"))
    for task in queue:
        print(task.id)
    print("=========priority=3:")
    logger.info(("=========priority=3:"))
    for task in queue.filter_by_priority(3):
        print(task.id)



# def main(argv:list[str] |None =None)->int:
#     argv=argv or sys.argv[1:]
#     if argv and argv[0]=="file":
#         source=FileTaskSource(Path("data/tasks.json"))
#     elif argv and argv[0] == "api":
#         source = ApiTaskSource(_example_fetcher)
#     else:
#         source = GeneratedTaskSource(count=8, base_priority=1)

#     receiver=TaskReceiver(source)
#     for task in receiver.load_tasks():
#         logger.info(f"Loaded tasks:{task},{task.is_ready}")
#         print(f"{task.id} | {task.description[:60]} | pr={task.priority} | status={task.status} | ready={task.is_ready}")

if __name__=="__main__":
    main()