import sys
sys.path.append(".")

import image_gen_pb2
import image_gen_pb2_grpc

import gradio as gr
import grpc

from PIL import Image


def generate_from_grpc(prompt):
    try:
        channel = grpc.insecure_channel("localhost:50051")
        stub = image_gen_pb2_grpc.ImageGenServiceStub(channel)
        response = stub.GenerateImage(image_gen_pb2.ImageRequest(prompt=prompt))
        if response.status == "success":
            return Image.open(response.image_path)
        else:
            return f"❌ Error: {response.message}"
    except Exception as e:
        return f"⚠️ Failed to connect to gRPC server: {str(e)}"


iface = gr.Interface(
    fn=generate_from_grpc,
    inputs=gr.Textbox(label="Enter your image prompt"),
    outputs=gr.Image(label="Generated Image"),
    title="Text-to-Image gRPC Demo",
)

if __name__ == "__main__":
    iface.launch()
