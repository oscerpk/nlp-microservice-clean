import grpc
import image_gen_pb2
import image_gen_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = image_gen_pb2_grpc.ImageGenServiceStub(channel)
    
    prompt = input("Enter a prompt: ")
    response = stub.GenerateImage(image_gen_pb2.ImageRequest(prompt=prompt))
    
    print(f"Status: {response.status}")
    print(f"Image Path: {response.image_path}")
    print(f"Message: {response.message}")

if __name__ == "__main__":
    run()
