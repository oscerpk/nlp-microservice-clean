import grpc
from concurrent import futures
import image_gen_pb2
import image_gen_pb2_grpc
from generate import generate_image  # your model function
import os

class ImageGenServicer(image_gen_pb2_grpc.ImageGenServiceServicer):
    def GenerateImage(self, request, context):
        try:
            if not request.prompt.strip():
                return image_gen_pb2.ImageResponse(
                    status="error",
                    message="Prompt cannot be empty."
                )
            prompt = request.prompt
            print(f"Received prompt: {prompt}")
            image_path = generate_image(prompt)  # modify to return image path
            return image_gen_pb2.ImageResponse(
                status="success",
                image_path=image_path,
                message="Image generated successfully."
            )
        except Exception as e:
            return image_gen_pb2.ImageResponse(
                status="error",
                image_path="",
                message=str(e)
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_gen_pb2_grpc.add_ImageGenServiceServicer_to_server(ImageGenServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("🟢 gRPC Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
