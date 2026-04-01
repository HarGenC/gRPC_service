import grpc

from app.generated import kvstore_pb2, kvstore_pb2_grpc


def run():
    channel = grpc.insecure_channel("localhost:8000")
    stub = kvstore_pb2_grpc.KeyValueStoreStub(channel)

    for i in range(10):
        stub.Put(kvstore_pb2.PutRequest(key=f"foo{i}", value="bar"))

    res = stub.List(kvstore_pb2.ListRequest(prefix="oo"))
    print(res)


if __name__ == "__main__":
    run()
