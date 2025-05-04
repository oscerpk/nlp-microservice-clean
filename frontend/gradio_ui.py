import sys
import os

# Ensure root folder is in Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import gradio as gr
import grpc
import time
import os
import pipeline_pb2
import pipeline_pb2_grpc

def call_grpc(prompt, face_img_path):
    with open(face_img_path, "rb") as f:
        face_bytes = f.read()

    channel = grpc.insecure_channel("localhost:50051")
    stub = pipeline_pb2_grpc.ImagePipelineStub(channel)

    request = pipeline_pb2.PipelineRequest(prompt=prompt, face_image=face_bytes)
    return stub.RunPipeline(request)

def run_pipeline(prompt, face_img_path):
    try:
        face_bytes = b""
        if face_img_path and os.path.exists(face_img_path):
            with open(face_img_path, "rb") as f:
                face_bytes = f.read()

        channel = grpc.insecure_channel("localhost:50051")
        stub = pipeline_pb2_grpc.ImagePipelineStub(channel)

        request = pipeline_pb2.PipelineRequest(prompt=prompt, face_image=face_bytes)
        response = stub.RunPipeline(request)

        output_path = "output/final_from_grpc.jpg"
        with open(output_path, "wb") as f:
            f.write(response.result_image)

        return output_path, response.log

    except grpc.RpcError as e:
        return None, f"❌ ERROR: {e.details() or 'Unknown gRPC error'}"


with gr.Blocks(title="🧠 AI Face Fusion Tool") as demo:
    gr.Markdown("## 🧠 Face Fusion: Prompt + Face → Enhanced Image")
    with gr.Row():
        prompt = gr.Textbox(label="Enter Prompt", placeholder="e.g. a Pakistani girl in studio", scale=2)
        run_btn = gr.Button("✨ Run Full Pipeline", scale=1)

    with gr.Row():
        face = gr.Image(
        label="Upload Face (Optional)",
        type="filepath",
        width=256,
        height=256,
        image_mode="RGB",
    )


    with gr.Row():
        output_img = gr.Image(label="Final Image", width=512, height=512, show_download_button=True)
        logs = gr.Textbox(label="Logs", lines=10)

    run_btn.click(fn=run_pipeline, inputs=[prompt, face], outputs=[output_img, logs])

demo.launch()
