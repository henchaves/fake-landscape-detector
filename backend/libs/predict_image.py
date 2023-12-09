import os
import numpy as np
from PIL import Image
from transformers import ViTForImageClassification, ViTImageProcessor
import requests
import json
import torch


def load_image(image_filename, image_dir, H=264, W=264):
    image_path = os.path.join(image_dir, image_filename)

    x = Image.open(image_path)
    if x.mode != "RGB":
        x = x.convert("RGB")
    x = x.resize((224, 224), Image.Resampling.LANCZOS)
    return x

def request_model(x):
    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224-in21k')
    model = ViTForImageClassification.from_pretrained("models/vit_binary_classifier_20231205")
    classes = ["REAL", "FAKE"]

    x = torch.tensor(processor(x, return_tensors="pt")['pixel_values'])

    outputs = model(x)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1).detach().numpy()

    predictions = outputs.logits.argmax(dim=-1).numpy()

    return classes[predictions[0]], probabilities[0][predictions[0]]

