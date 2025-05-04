import grpc
from concurrent import futures
import os
import pipeline_pb2
import pipeline_pb2_grpc
from generate import generate_image
from fuse_face import fuse_faces
from enhance import enhance_image

class ImagePipelineServicer(pipeline_pb2_grpc.ImagePipelineServicer):
 def RunPipeline(self, request, context):
    try:
        log = ""

        prompt = request.prompt
        face_bytes = request.face_image
        face_provided = len(face_bytes) > 0

        log += "🔹 Generating image from prompt...\n"
        generated_path = generate_image(prompt)
        log += f"✅ Image generated: {generated_path}\n"

        if face_provided:
            log += "🔹 Saving face image...\n"
            face_path = "temp_face.jpg"
            with open(face_path, "wb") as f:
                f.write(face_bytes)
            log += "✅ Face image saved.\n"

            log += "🔹 Performing face swap...\n"
            swapped_path = fuse_faces(generated_path, face_path)
            log += f"✅ Face swapped: {swapped_path}\n"
        else:
            log += "⚠️ No face image provided. Skipping face swap.\n"
            swapped_path = generated_path

        log += "🔹 Enhancing image...\n"
        final_path = enhance_image(swapped_path)
        log += f"✅ Enhancement complete: {final_path}\n"

        with open(final_path, "rb") as f:
            result_bytes = f.read()

        return pipeline_pb2.PipelineReply(result_image=result_bytes, log=log)

    except Exception as e:
        context.set_details(str(e))
        context.set_code(grpc.StatusCode.INTERNAL)
        return pipeline_pb2.PipelineReply()



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
