<!--
README for Text-to-Image & Image-to-Image App
This document explains setup, usage, architecture, models, credits, and limitations.
-->
# Text-to-Image & Image-to-Image App Documentation
> **Note:**  
> This README provides comprehensive instructions for installing, running, and understanding the architecture of the app.
---
## Introduction
<!--
Brief overview of the application's purpose and capabilities.
-->
This application is an advanced AI-powered tool that allows users to generate images from textual prompts (Text-to-Image) or modify existing images by fusing new faces and enhancing details (Image-to-Image). The app leverages state-of-the-art models in generative AI and facial recognition to deliver high-quality, realistic images based on user input. Users can seamlessly switch between text-to-image and image-to-image workflows, offering flexibility and creativity in image generation and editing.
---
## Setup
<!--
Step-by-step instructions for preparing the environment.
-->
To run this application, follow these steps:
### 1. Create a Python Virtual Environment
python3 -m venv venv310
> *Creates an isolated Python environment named `venv310`.*
### 2. Activate the Virtual Environment
source venv310/bin/activate
> *Activates the virtual environment so dependencies install locally.*
### 3. Install Required Dependencies
Make sure you have a `requirements.txt` file in your project directory, then run:
pip install -r requirements.txt
> *Installs all necessary Python packages for the project.*
---
## Usage
<!--
How to use each main feature of the application.
-->
The application provides several command-line scripts for different functionalities:
### 1. Generate an Image from Text
Generate an image based on a textual prompt:
python generate.py --prompt "a young man sitting confidently in a modern office"
> *Uses the text-to-image model to create a new image from your description.*
### 2. Face Fusion (Image-to-Image)
Fuse a user-provided face onto a generated or existing base image:
python fuse_face.py --base_image output_image.png --face_image user_face.jpg
> *Swaps the face in the base image with the user’s face for personalization.*
### 3. Image Enhancement
Enhance the quality of an image, especially after face fusion, for improved realism:
python enhance.py --input swapped_image.png --output enhanced_image.png
text
> *Applies super-resolution and face enhancement to the final image.*
---
## Architecture
<!--
High-level overview of the workflow and modular design.
-->
### Overview
The app is modular, with each core function handled by a dedicated script and model. The workflow typically follows these steps:
1. **Text-to-Image Generation:** Uses a diffusion model to create a base image from a prompt.
2. **Face Swapping:** Swaps the face in the generated image with a user-provided face for personalization.
3. **Image Enhancement:** Uses a super-resolution model to improve the final image quality.
### Models Used
- **Realistic_Vision_V5.1_noVAE/**  
  *A diffusion-based model for generating high-quality, realistic images from text prompts.*
- **inswapper_128.onnx**  
  *A face-swapping model for accurate and seamless facial feature transfer.*
- **GFPGANv1.3.pth**  
  *A generative model for face restoration and enhancement, improving image clarity and details.*
- **buffalo_l/** (InsightFace)  
  *A facial recognition and alignment model used to ensure accurate face swapping.*
---
## Model Sources
<!--
Attribution and references for the models used.
-->
- **Stable Diffusion:**  
  Used for text-to-image generation.  
  [GitHub - CompVis/stable-diffusion](https://github.com/CompVis/stable-diffusion)
- **InsightFace:**  
  Used for face detection, alignment, and swapping.  
  [GitHub - deepinsight/insightface](https://github.com/deepinsight/insightface)
- **GFPGAN:**  
  Used for face restoration and enhancement.  
  [GitHub - TencentARC/GFPGAN](https://github.com/TencentARC/GFPGAN)
---
## Credits
<!--
Acknowledgement of the open-source projects and contributors.
-->
- **Stable Diffusion** for the text-to-image model.
- **InsightFace** for facial recognition and swapping.
- **GFPGAN** for image enhancement.
---
## Limitations
<!--
Known issues and ethical considerations.
-->
- **Privacy Concerns:**  
  The app is designed with privacy in mind and restricts the use of real-world celebrity or famous individuals’ images to prevent misuse and protect personal integrity.
- **Generalization:**  
  The model may not always perfectly generalize to all input images, especially those with unusual poses, lighting, or occlusions.
---
<!--
-->
