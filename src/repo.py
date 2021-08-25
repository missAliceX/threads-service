from typing import List

from pylib.postgres import PostgresClient
from pylib.proto.threads_pb2 import ThreadType, Thread


def get_threads(project_id: int, thread_type: ThreadType, limit: int):
    """
    get_threads retrieves threads for a given thread type.
    """
    pass


def update_threads(project_id: int, threads: List[Thread]):
    """
    update_threads inserts a list of threads into the threads table.
    """
    with PostgresClient.repo() as cursor:
        cursor.execute(
            f"insert into threads(project_id, thread_type, message) values {','.join(['%s'] * len(threads))}",
            [(project_id, ThreadType.Name(t.thread_type), t.message) for t in threads]
        )
