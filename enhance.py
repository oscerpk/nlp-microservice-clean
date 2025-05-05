import cv2
import numpy as np
from gfpgan import GFPGANer
import os

# Initialize GFPGAN once globally
restorer = GFPGANer(
    model_path='experiments/pretrained_models/GFPGANv1.3.pth',
    upscale=2,
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=None
)

def enhance_image(image_path):
    """
    Enhances the given image using GFPGAN.

    Args:
        image_path (str): Path to the image to be enhanced.

    Returns:
        str: Path to the enhanced output image.
    """
    # Load input image
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)

    # Perform enhancement
    cropped_faces, restored_faces, restored_img = restorer.enhance(
        img, has_aligned=False, only_center_face=False, paste_back=True
    )

    # Save output if enhancement succeeded
    output_path = "output/enhanced_image.jpg"
    if isinstance(restored_img, np.ndarray):
        cv2.imwrite(output_path, restored_img)
        return output_path
    else:
        raise ValueError("❌ Enhancement failed or no face detected.")


