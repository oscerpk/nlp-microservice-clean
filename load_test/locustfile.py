from locust import User, task, between
import grpc
import image_gen_pb2
import image_gen_pb2_grpc

class GRPCUser(User):
    wait_time = between(1, 3)

    def on_start(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = image_gen_pb2_grpc.ImageGenServiceStub(self.channel)

    @task
    def generate_image(self):
        prompt = "A glowing alien city at night"
        self.stub.GenerateImage(image_gen_pb2.ImageRequest(prompt=prompt))
