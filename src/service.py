from sanic import Sanic
from sanic.log import logger as log
from src import repo

from pylib.service.grpc import GRPCService
from pylib.postgres import PostgresClient
from pylib.proto.threads_pb2 import UpdateThreadsRequest, UpdateThreadsResponse, GetProjectThreadsRequest, GetSubThreadsRequest
from pylib.proto.threads_pb2_grpc import ThreadsServiceServicer, add_ThreadsServiceServicer_to_server


class Service(ThreadsServiceServicer, GRPCService):
    def __init__(self, cfg={}):
        # Calls __init__ of the GRPCService class
        super().__init__("threads-service", add_ThreadsServiceServicer_to_server)

        # Sets up the connection to the database, add tables and types if necessary
        PostgresClient.migrate('up')
        PostgresClient.connect(cfg)

    def UpdateThreads(self, req: UpdateThreadsRequest):
        """
        UpdateThreads adds a new thread for the given project.
        """
        repo.update_threads(req.project_id, req.threads)
        return UpdateThreadsResponse()

    def GetProjectThreads(self, req: GetProjectThreadsRequest):
        """
        GetProjectThreads retrieves threads for the given project.
        """
        pass

    def GetSubThreads(self, req: GetSubThreadsRequest):
        """
        GetSubThreads gets threads related to the given thread.
        """
        pass

