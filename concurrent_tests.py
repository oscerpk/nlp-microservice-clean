import grpc
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed
import pipeline_pb2
import pipeline_pb2_grpc

# CONFIG
GRPC_HOST = "localhost:50051"
NUM_REQUESTS = 20
MAX_WORKERS = 5

response_times = []
statuses = []

def send_grpc_request(i):
    try:
        channel = grpc.insecure_channel(GRPC_HOST)
        stub = pipeline_pb2_grpc.ImagePipelineStub(channel)

        request = pipeline_pb2.PipelineRequest(
            prompt=f"a Pakistani man in a kurta test {i}",
            face_image=b""  # Optional image
        )

        start = time.time()
        response = stub.RunPipeline(request)
        elapsed = round(time.time() - start, 2)

        # You can log response.log if needed
        return i, 200, elapsed
    except grpc.RpcError as e:
        print(f"❌ Request #{i} failed: {e}")
        return i, 500, 0

# Start Concurrent Execution
start_time = time.time()
with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
    futures = [executor.submit(send_grpc_request, i) for i in range(NUM_REQUESTS)]
    for future in as_completed(futures):
        i, status, duration = future.result()
        print(f"✅ Request #{i}: Status = {status}, Time = {duration}s")
        response_times.append(duration)
        statuses.append(status)

total_time = round(time.time() - start_time, 2)
print(f"\n🏁 Total Time: {total_time}s for {NUM_REQUESTS} requests")

# Plot Performance Graph
colors = ['green' if s == 200 else 'red' for s in statuses]
plt.figure(figsize=(12, 6))
plt.bar(range(NUM_REQUESTS), response_times, color=colors)
plt.xlabel("Request #")
plt.ylabel("Response Time (s)")
plt.title(f"gRPC Concurrent Performance - {NUM_REQUESTS} Requests, {MAX_WORKERS} Workers")
plt.grid(True)
plt.tight_layout()
plt.savefig("grpc_performance_graph.png")
plt.show()
