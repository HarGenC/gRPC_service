import asyncio
from concurrent import futures

import grpc

from generated import kvstore_pb2_grpc
from server.service import KVStoreService


async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

    kvstore_pb2_grpc.add_KeyValueStoreServicer_to_server(KVStoreService(), server)

    server.add_insecure_port("[::]:8000")
    server.start()

    server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
