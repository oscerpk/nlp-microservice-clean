from diffusers import StableDiffusionPipeline
from PIL import Image
import torch
import os

# --- Prompt Filter ---
BANNED_KEYWORDS = {
    "nude", "naked", "nsfw", "porn", "sex", "boobs", "cleavage",
    "lingerie", "erotic", "sensual", "topless", "underwear", "bikini", "explicit"
}

def is_safe_prompt(prompt: str) -> bool:
    return not any(word in prompt.lower() for word in BANNED_KEYWORDS)

# --- Smart Prompt Enhancer ---
def prepare_prompt(user_prompt: str) -> str:
    base = user_prompt.strip()

    # Inject safe attire tag only if user prompt is short
    if len(base.split()) < 20:
        base += ", fully clothed, modest attire, professional outfit"

    return base.strip()

# --- Short Negative Prompt (NSFW + Quality Filter) ---
negative_prompt = (
    "nude, naked, nsfw, porn, sex, boobs, cleavage, lingerie, topless, "
    "worst quality, low quality, blurry, jpeg artifacts, extra limbs"
)

# --- Main Generator ---
def generate_image(prompt):
    if not is_safe_prompt(prompt):
        raise ValueError("❌ Unsafe prompt blocked. Please avoid NSFW or sensitive words.")

    # Prepare enhanced prompt safely
    final_prompt = prepare_prompt(prompt)

    model_id = "./Realistic_Vision_V5.1_noVAE"

    pipe = StableDiffusionPipeline.from_pretrained(
        model_id,
        torch_dtype=torch.float16,
        use_safetensors=True
    )
    pipe.to("mps")

    result = pipe(
        final_prompt,
        negative_prompt=negative_prompt,
        guidance_scale=7.5,
        num_inference_steps=30,
        height=512,
        width=512
    ).images

    filename = "output_image.png"
    result[0].save(filename)
    return filename

# --- CLI Mode (Optional) ---
if __name__ == "__main__":
    prompt = input("📝 Enter your image prompt: ")
    try:
        path = generate_image(prompt)
        print(f"✅ Image saved: {path}")
    except ValueError as ve:
        print(str(ve))
