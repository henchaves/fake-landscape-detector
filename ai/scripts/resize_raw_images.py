from PIL import Image
import os
from tqdm import tqdm

IMG_DATA_DIR = os.path.join('..', 'data', 'img')
RAW_IMG_DIR = os.path.join(IMG_DATA_DIR, 'raw')
RESIZED_IMG_DIR = os.path.join(IMG_DATA_DIR, 'raw-resized')
SIZE = 1024

def resize_image(input_image_path, output_image_path, size):
    original_image = Image.open(input_image_path)
    resized_image = original_image.resize((size, size), Image.Resampling.LANCZOS)
    resized_image.save(output_image_path)

if __name__ == '__main__':
    for filename in tqdm(os.listdir(RAW_IMG_DIR)):
        input_path = os.path.join(RAW_IMG_DIR, filename)
        output_path = os.path.join(RESIZED_IMG_DIR, filename)
        resize_image(input_path, output_path, SIZE)