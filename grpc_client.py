import grpc
import pipeline_pb2
import pipeline_pb2_grpc
from google.protobuf.json_format import MessageToJson
import sys
import os

def is_valid_file(path):
    return os.path.exists(path) and os.path.isfile(path)

def test_grpc(prompt, face_img_path=None):
    face_bytes = b""
    if face_img_path and is_valid_file(face_img_path):
        with open(face_img_path, "rb") as f:
            face_bytes = f.read()

    # Setup gRPC
    channel = grpc.insecure_channel("localhost:50051")
    stub = pipeline_pb2_grpc.ImagePipelineStub(channel)

    request = pipeline_pb2.PipelineRequest(prompt=prompt, face_image=face_bytes)
    response = stub.RunPipeline(request)

    # Show as JSON
    json_output = MessageToJson(response)
    print("📦 gRPC Response as JSON:\n")
    print(json_output)

    # Optionally save image if success
    if response.status_code == 200:
        output_path = "client_output.jpg"
        with open(output_path, "wb") as f:
            f.write(response.result_image)
        print(f"\n✅ Image saved to {output_path}")
    else:
        print(f"\n❌ Failed: {response.status_message}")

if __name__ == "__main__":
    prompt = input("📝 Enter prompt: ")
    use_face = input("📷 Add face image? (y/n): ").lower()

    face_path = None
    if use_face == "y":
        face_path = input("📁 Enter path to face image: ").strip()

    test_grpc(prompt, face_path)
