import os
from diffusers import StableDiffusionPipeline
import torch
from tqdm import tqdm
import numpy as np
import pandas as pd
import json

DATA_PATH = "../data"
IMG_DATA_PATH = os.path.join(DATA_PATH, "img")
JSON_DATA_PATH = os.path.join(DATA_PATH, "json")
CAPTIONS_JSON_PATH = os.path.join(JSON_DATA_PATH, "image_captions.json")
NEW_CAPTIONS_JSON_PATH = os.path.join(JSON_DATA_PATH, "new_image_captions.json")

if __name__ == '__main__':
  df_captions = pd.read_json(CAPTIONS_JSON_PATH, typ='series')
  captions = [caption.replace("a realistic photo of", "photo,") for caption in df_captions.unique().tolist()]

  np.random.seed(42)
  captions_idx = np.arange(len(captions))
  np.random.shuffle(captions_idx)

  remaining_captions = len(df_captions) - len(captions)
  new_captions = []
  copy_captions = captions.copy()

  remaining_captions = len(df_captions) - len(captions)
  new_captions = []
  copy_captions = captions.copy()

  for i in captions_idx:
    current_caption = copy_captions[i]
    for season in ["summer", "spring", "winter", "autumn"]:
      new_captions.append(f"{current_caption}, in the {season}")
    captions = [caption for caption in captions if caption != current_caption]
    remaining_captions -= 3
    if remaining_captions < 0:
      break
  
  captions.extend(new_captions)
  captions = captions[:len(df_captions)]

  with open(NEW_CAPTIONS_JSON_PATH, 'w') as f:
    json.dump(captions, f)

  pipe = StableDiffusionPipeline.from_pretrained("dreamlike-art/dreamlike-photoreal-2.0", torch_dtype=torch.float16)
  pipe = pipe.to("cuda")
  
  for j, prompt in enumerate(tqdm(captions)):
    image = pipe(prompt).images[0]
    filename = f"{str(j+i+1).zfill(4)}.jpg"
    print(f"\nSaving {filename}\n")
    image.save(os.path.join(IMG_DATA_PATH, filename))

