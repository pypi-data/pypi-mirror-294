from pathlib import Path

from ictasks.session import Session
from ictasks.environment import Environment
from ictasks.worker_collection import WorkerCollection
from ictasks.tasks import TaskCollection, TaskLauncher, TaskfarmFile


def test_taskfarm_session():

    workers = WorkerCollection()

    env = Environment(workers)
    env.job_id = "1234"
    env.nodelist = "localhost"

    work_dir = Path().resolve()

    taskfarm_file = TaskfarmFile(work_dir)
    tasklist = "echo 'hello from task 1'\necho 'hello from task 2'"
    num_grouped, tasks = taskfarm_file.load(tasklist)
    
    task_collection = TaskCollection(work_dir)
    task_collection.num_grouped_tasks = num_grouped
    task_collection.tasks = tasks

    launcher = TaskLauncher()
    
    session = Session(env, tasks, launcher, keep_finished_tasks=True)



