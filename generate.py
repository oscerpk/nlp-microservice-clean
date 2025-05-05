from diffusers import StableDiffusionPipeline
from PIL import Image
import torch
import os
from threading import Lock
import platform

# --- Load Files ---
def load_lines(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

def load_text(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return f.read().strip()

# 🔐 Load keywords and negative prompt
BANNED_KEYWORDS = set(load_lines("config/banned_keywords.txt"))
negative_prompt = load_text("config/negative_prompt.txt")

# --- Safety Check ---
def is_safe_prompt(prompt: str) -> bool:
    return not any(word in prompt.lower() for word in BANNED_KEYWORDS)

# --- Prompt Enhancer ---
def prepare_prompt(user_prompt: str) -> str:
    base = user_prompt.strip()
    if len(base.split()) < 20:
        base += ", fully clothed, modest attire, professional outfit"
    return base.strip()

# --- Load Model Once ---
print("🔁 Loading model...")
model_id = "Realistic_Vision_V5.1_noVAE"

# Use CPU inside Docker (no GPU/MPS available)
if os.environ.get("DOCKER_ENV") == "1":
    device = "cpu"
    dtype = torch.float32
elif platform.system() == "Darwin" and torch.backends.mps.is_available():
    device = "mps"
    dtype = torch.float16 
else:
    device = "cpu"
    dtype = torch.float32

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=dtype,
    use_safetensors=True,
    local_files_only=True  
)


pipe.to(device)




generation_lock = Lock()
print("✅ Model is ready.")

# --- Generate Function ---
def generate_image(prompt):
    if not is_safe_prompt(prompt):
        raise ValueError("❌ Unsafe prompt blocked. Please revise your input.")
    
    final_prompt = prepare_prompt(prompt)

    with generation_lock:
        result = pipe(
            final_prompt,
            negative_prompt=negative_prompt,
            guidance_scale=7.5,
            num_inference_steps=30,
            height=512,
            width=512
        ).images

    filename = "output/output_image.png"
    result[0].save(filename)
    return filename

# --- CLI Mode ---
if __name__ == "__main__":
    prompt = input("📝 Enter your image prompt: ")
    try:
        path = generate_image(prompt)
        print(f"✅ Image saved: {path}")
    except ValueError as ve:
        print(str(ve))
