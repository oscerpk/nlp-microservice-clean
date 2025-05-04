import sys
sys.path.append(".")

import grpc
import image_gen_pb2
import image_gen_pb2_grpc

def test_valid_prompt():
    channel = grpc.insecure_channel("localhost:50051")
    stub = image_gen_pb2_grpc.ImageGenServiceStub(channel)
    response = stub.GenerateImage(image_gen_pb2.ImageRequest(prompt="A fantasy castle at sunset"))
    assert response.status == "success"
    assert response.image_path.endswith(".png")

def test_empty_prompt():
    channel = grpc.insecure_channel("localhost:50051")
    stub = image_gen_pb2_grpc.ImageGenServiceStub(channel)
    response = stub.GenerateImage(image_gen_pb2.ImageRequest(prompt=""))
    assert response.status == "error"
    assert "empty" in response.message.lower()
