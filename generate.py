from diffusers import StableDiffusionPipeline
from PIL import Image, ImageEnhance
from torch import Generator
import sys
import os


import torch

def generate_image(prompt):
    
    model_id = "./Realistic_Vision_V5.1_noVAE"

    
    negative_prompt = (
        "deformed iris, deformed pupils, semi-realistic, cgi, 3d, render, sketch, "
        "cartoon, drawing, anime:1.4, text, close up, cropped, out of frame, "
        "worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, "
        "extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, "
        "deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, "
        "cloned face, disfigured, gross proportions, malformed limbs, missing arms, "
        "missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck"
    )

    
    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        use_safetensors=True,
    )
    
    pipe.to("mps")


 

    
    results = pipe(
        prompt,
        negative_prompt=negative_prompt,
        enhance_style="hyperrealism",
        guidance_scale=7.5,
        self_attention="yes",
        upscale=8,
        height=512,
        width=512,
        num_inference_steps=30  
     
    ).images


    filename = f"output_image.png"
    results[0].save(filename)
    return filename
    
   


if __name__ == "__main__":
    prompt = input("Enter your positive prompt: ")
    generate_image(prompt)
