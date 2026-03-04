import requests
import base64
import os
import random
import zipfile

API_KEY = os.environ.get("API_KEY", "YOUR_API_KEY")
URL = "https://ai.hackclub.com/proxy/v1/chat/completions"

OUTPUT_DIR = "radha_krishna_holi_images"
ZIP_NAME = "radha_krishna_holi_dataset.zip"
NUM_IMAGES = 100

os.makedirs(OUTPUT_DIR, exist_ok=True)

prompt_variations = [
    "Radha and Krishna playing Holi in Vrindavan, colorful powder everywhere, joyful atmosphere",
    "Lord Krishna teasing Radha with gulal during Holi festival, vibrant Indian art style",
    "Radha Krishna Holi celebration, traditional attire, flowers and colors in the air",
    "Krishna splashing colors on Radha, Holi festival in Vrindavan, cinematic lighting",
    "Radha Krishna dancing during Holi, bright powders, festive crowd",
    "Divine Radha Krishna Holi celebration, pastel colors, temple background",
    "Radha Krishna throwing gulal, spring festival of Holi, joyful scene",
    "Krishna playing flute while Radha throws colors during Holi",
]

def generate_image(prompt, index):
    payload = {
        "model": "google/gemini-3.1-flash-image-preview",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "modalities": ["image", "text"],
        "image_config": {
            "aspect_ratio": "1:1"
        }
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    try:
        image_base64 = data["choices"][0]["message"]["images"][0]["b64"]
        image_bytes = base64.b64decode(image_base64)

        filename = os.path.join(OUTPUT_DIR, f"holi_{index}.png")

        with open(filename, "wb") as f:
            f.write(image_bytes)

        print(f"Saved {filename}")

    except Exception as e:
        print(f"Failed to process image {index}: {e}", data)


# Generate images
for i in range(NUM_IMAGES):
    prompt = random.choice(prompt_variations)
    generate_image(prompt, i)


# Zip images
with zipfile.ZipFile(ZIP_NAME, 'w') as zipf:
    for file in os.listdir(OUTPUT_DIR):
        zipf.write(os.path.join(OUTPUT_DIR, file), file)

print(f"\nZip created: {ZIP_NAME}")
