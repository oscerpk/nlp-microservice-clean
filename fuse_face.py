import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.model_zoo import get_model

# Global Initialization (to avoid repeating in every call)
app = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
app.prepare(ctx_id=0)

swapper = get_model("inswapper_128.onnx", providers=["CPUExecutionProvider"])

def fuse_faces(target_img_path, source_img_path):
    """
    Swaps the face from source_img onto target_img.

    Args:
        target_img_path (str): Path to the generated image.
        source_img_path (str): Path to the user face image.

    Returns:
        str: Path to the swapped output image.
    """
    # Load images
    source_img = cv2.imread(source_img_path)
    target_img = cv2.imread(target_img_path)

    # Detect faces
    source_faces = app.get(source_img)
    target_faces = app.get(target_img)

    if len(source_faces) == 0 or len(target_faces) == 0:
        raise ValueError("❌ Face not detected in one of the images.")

    # Use first detected face from both
    source_face = source_faces[0]
    target_face = target_faces[0]

    # Do the swap
    swapped_img = swapper.get(target_img, target_face, source_face)

    # Save output
    output_path = "output/swapped_face.jpg"
    cv2.imwrite(output_path, swapped_img)
    return output_path
