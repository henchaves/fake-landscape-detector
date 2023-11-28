import os
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from tqdm import tqdm
import concurrent.futures
import json

# Images data
RAW_DATA_PATH = "../data/img/raw"
RAW_IMAGE_FILENAMES = os.listdir(RAW_DATA_PATH)

# Captions data
CAPTIONS_DATA_DIR = "../data/json"
CAPTIONS_FILENAME = "image_captions.json"
CAPTIONS_PATH = os.path.join(CAPTIONS_DATA_DIR, CAPTIONS_FILENAME)

# Captions model
TEXT_CONDITION = "a realistic photo of"
NUM_THREADS = 8

def get_caption(raw_image_filename):
    raw_image_path = os.path.join(RAW_DATA_PATH, raw_image_filename)
    raw_image = Image.open(raw_image_path).convert("RGB")
    inputs = processor(raw_image, TEXT_CONDITION, return_tensors="pt")
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return raw_image_filename, caption


if __name__ == '__main__':
  image_captions = {}

  processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
  model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

  with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_THREADS) as executor:
    # Start the load operations and mark each future with its URL
    future_to_filename = {executor.submit(get_caption, filename): filename for filename in RAW_IMAGE_FILENAMES}
    for future in tqdm(concurrent.futures.as_completed(future_to_filename), total=len(future_to_filename), desc='Processing Images'):
        filename = future_to_filename[future]
        try:
            image_captions[filename] = future.result()[1]
        except Exception as exc:
            print(f'An exception occurred while processing {filename}: {exc}')
  
  with open(CAPTIONS_PATH, 'w') as f:
    json.dump(image_captions, f)