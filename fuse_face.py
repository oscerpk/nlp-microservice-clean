import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

# Initialize face analysis
app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

# Load images
source_img = cv2.imread("in.png")  # face to inject
target_img = cv2.imread("output_image.png")    # where to inject

# Detect faces
source_faces = app.get(source_img)
target_faces = app.get(target_img)

if len(source_faces) == 0 or len(target_faces) == 0:
    print("❌ Face not detected!")
    exit()

# Use first detected faces
source_face = source_faces[0]
target_face = target_faces[0]

# Load InsightFace Swapper Model
swapper = get_model("inswapper_128.onnx", providers=["CPUExecutionProvider"])

# Do the swap
swapped_img = swapper.get(target_img, target_face, source_face)

# Save output
cv2.imwrite("real_swap.jpg", swapped_img)
print("✅ Real face swap completed and saved as real_swap.jpg")
