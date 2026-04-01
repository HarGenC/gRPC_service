import grpc
from app.generated import kvstore_pb2, kvstore_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:8000")
    stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)

    stub.Put(kvstore_pb2.PutRequest(key="foo", value="bar"))

    res = stub.Get(kvstore_pb2.GetRequest(key="foo"))
    print(res.value)
    stub.Delete(kvstore_pb2.DeleteRequest(key="foo"))
    res = stub.Get(kvstore_pb2.GetRequest(key="foo"))


if __name__ == "__main__":
    run()