import cv2
import numpy as np
from gfpgan import GFPGANer

# Initialize GFPGAN
restorer = GFPGANer(
    model_path='experiments/pretrained_models/GFPGANv1.3.pth',
    upscale=2,
    arch='clean',
    channel_multiplier=2,
    bg_upsampler=None
)

# Load image
img = cv2.imread('real_swap.jpg', cv2.IMREAD_COLOR)

# Enhance
cropped_faces, restored_faces, restored_img = restorer.enhance(
    img, has_aligned=False, only_center_face=False, paste_back=True
)

# Save output
if isinstance(restored_img, (np.ndarray,)):
    cv2.imwrite('saved.png', restored_img)
    print("✅ Image saved successfully.")
else:
    print("❌ Enhancement failed or no face detected.")
