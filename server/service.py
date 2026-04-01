import asyncio
import time

import grpc

from generated import kvstore_pb2, kvstore_pb2_grpc


class KVStoreService(kvstore_pb2_grpc.KeyValueStoreServicer):
    def __init__(self):
        self.store = {}

    async def _worker(self):
        while True:
            func, fut = await self.queue.get()
            try:
                result = func()
                fut.set_result(result)
            except Exception as e:
                fut.set_exception(e)
            self.queue.task_done()

    async def _run_in_queue(self, func):
        fut = asyncio.get_event_loop().create_future()
        await self.queue.put((func, fut))
        return await fut

    async def Put(self, request, context):
        """Put: добавить или обновить значение. ttl_seconds = 0 означает отсутствие TTL."""

        def job():
            expire = None
            if request.ttl_seconds > 0:
                expire = time.time() + request.ttl_seconds
            self.store[request.key] = {"value": request.value, "ttl_seconds": expire}
            return kvstore_pb2.PutResponse()

        return await self._run_in_queue(job)

    async def Get(self, request, context):
        """Get: получить значение по ключу. NOT_FOUND — если ключ отсутствует или TTL истёк."""

        def job():
            now = time.time()
            if request.key not in self.store:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Key not found")
                return kvstore_pb2.PutResponse()
            result = self.store[request.key]

            if result.get("ttl_seconds") < now:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Key's time is expired")
                return kvstore_pb2.PutResponse()

            return kvstore_pb2.PutResponse(result.get("value"))

        return await self._run_in_queue(job)

    async def Delete(self, request, context):
        """Delete: удалить ключ."""

        def job():
            if request.key not in self.store:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("Key not found")
                return kvstore_pb2.PutResponse()

            del self.store[request.key]
            return kvstore_pb2.PutResponse()

        return await self._run_in_queue(job)

    async def List(self, request, context):
        """List: вернуть все ключи и значения с данным prefix. Истёкшие по TTL не возвращать."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")
