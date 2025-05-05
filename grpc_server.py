import grpc
from concurrent import futures
import os
import pipeline_pb2
import pipeline_pb2_grpc
from generate import generate_image
from fuse_face import fuse_faces
from enhance import enhance_image

def load_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()

# 🔐 Load keywords and negative prompt
BANNED_KEYWORDS = set(load_lines("config/banned_keywords.txt"))

def is_safe_prompt(prompt: str) -> bool:
    return not any(word in prompt.lower() for word in BANNED_KEYWORDS)

class ImagePipelineServicer(pipeline_pb2_grpc.ImagePipelineServicer):
    def RunPipeline(self, request, context):
        try:
            log = ""
            prompt = request.prompt
            face_bytes = request.face_image
            face_provided = len(face_bytes) > 0

            # Prompt check
            if not is_safe_prompt(prompt):
                return pipeline_pb2.PipelineReply(
                    status_code=400,
                    status_message="Blocked: Unsafe NSFW prompt",
                    log="❌ NSFW prompt blocked.",
                    result_image=b""
                )

            # Image generation
            log += "🔹 Generating image from prompt...\n"
            generated_path = generate_image(prompt)
            log += f"✅ Image generated: {generated_path}\n"

            if face_provided:
                log += "🔹 Saving face image...\n"
                face_path = "temp_face.jpg"
                with open(face_path, "wb") as f:
                    f.write(face_bytes)
                log += "✅ Face saved.\n"

                log += "🔹 Swapping face...\n"
                swapped_path = fuse_faces(generated_path, face_path)
                log += f"✅ Face swapped: {swapped_path}\n"
            else:
                log += "⚠️ No face provided. Skipping face swap.\n"
                swapped_path = generated_path

            log += "🔹 Enhancing image...\n"
            final_path = enhance_image(swapped_path)
            log += f"✅ Enhanced image: {final_path}\n"

            with open(final_path, "rb") as f:
                result_bytes = f.read()

            return pipeline_pb2.PipelineReply(
                result_image=result_bytes,
                log=log,
                status_code=200,
                status_message="Success"
            )

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return pipeline_pb2.PipelineReply(
                result_image=b"",
                log="❌ Error occurred during processing",
                status_code=500,
                status_message=str(e)
            )


def serve():
    options = [
        ("grpc.max_receive_message_length", 100 * 1024 * 1024),
        ("grpc.max_send_message_length", 100 * 1024 * 1024),
    ]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=os.cpu_count() * 2),
        options=options
    )
    pipeline_pb2_grpc.add_ImagePipelineServicer_to_server(ImagePipelineServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("✅ Robust gRPC server running on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
