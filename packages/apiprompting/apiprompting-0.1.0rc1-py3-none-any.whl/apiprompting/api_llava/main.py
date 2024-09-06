## Imports
import os, time, argparse, base64, requests, os, json, sys, datetime
from itertools import product
import warnings
warnings.filterwarnings("ignore")

# import cv2
from PIL import Image

import numpy as np
import torch
from torch.nn import functional as F
from torch.utils.data import DataLoader
from torchvision.datasets import ImageNet
import torchvision.transforms as T

from .functions import getmask, get_model
from .hook import hook_logger

def readImg(p):
    return Image.open(p)

def toImg(t):
    return T.ToPILImage()(t)

def invtrans(mask, image, method = Image.BICUBIC):
    return mask.resize(image.size, method)

def merge(mask, image, grap_scale = 200):
    gray = np.ones((image.size[1], image.size[0], 3))*grap_scale
    image_np = np.array(image).astype(np.float32)[..., :3]
    mask_np = np.array(mask).astype(np.float32)
    mask_np = mask_np / 255.0
    blended_np = image_np * mask_np[:, :, None]  + (1 - mask_np[:, :, None]) * gray
    blended_image = Image.fromarray((blended_np).astype(np.uint8))
    return blended_image

def normalize(mat, method = "max"):
    if method == "max":
        return (mat.max() - mat) / (mat.max() - mat.min())
    elif method == "min":
        return (mat - mat.min()) / (mat.max() - mat.min())
    else:
        raise NotImplementedError

def enhance(mat, coe=10):
    mat = mat - mat.mean()
    mat = mat / mat.std()
    mat = mat * coe
    mat = torch.sigmoid(mat)
    mat = mat.clamp(0,1)
    return mat

def revise_mask(patch_mask, kernel_size = 3, enhance_coe = 10):

    patch_mask = normalize(patch_mask, "min")
    patch_mask = enhance(patch_mask, coe = enhance_coe)

    assert kernel_size % 2 == 1
    padding_size = int((kernel_size - 1) / 2)
    conv = torch.nn.Conv2d(1,1,kernel_size = kernel_size, padding = padding_size, padding_mode = "replicate", stride = 1, bias = False)
    conv.weight.data = torch.ones_like(conv.weight.data) / kernel_size**2
    conv.to(patch_mask.device)

    patch_mask = conv(patch_mask.unsqueeze(0))[0]

    mask = patch_mask

    return mask

def blend_mask(image_path_or_pil_image, mask, enhance_coe, kernel_size, interpolate_method, grayscale):
    mask = revise_mask(mask.float(), kernel_size = kernel_size, enhance_coe = enhance_coe)
    mask = mask.detach().cpu()
    mask = toImg(mask.reshape(1,24,24))

    if isinstance(image_path_or_pil_image, str):
        image = readImg(image_path_or_pil_image)
    elif isinstance(image_path_or_pil_image, Image.Image):
        image = image_path_or_pil_image
    else:
        raise NotImplementedError

    mask = invtrans(mask, image, method = interpolate_method)
    merged_image = merge(mask.convert("L"), image.convert("RGB"), grayscale).convert("RGB")
    return merged_image

def llava_api(images, queries, model_name, batch_size = 1, layer_index = 20, enhance_coe = 10, kernel_size = 3, interpolate_method_name = "LANCZOS", grayscale = 0):

    """
    Generates image masks and blends them using the specified model and parameters.

    Parameters:
    images (list): list of images. Each item can be a path to image (str) or a PIL.Image. 
    queries (list): list of queries. Each item is a str. 
    batch_size (int): Batch size for processing images. Only support 1.
    model_name (str): Name of the model to load the pretrained model. One of "llava-v1.5-7b" and "llava-v1.5-13b".
    layer_index (int): Index of the layer in the model to hook. Default is 20.
    enhance_coe (int): Enhancement coefficient for mask blending. Default is 10.
    kernel_size (int): Kernel size for mask blending. Should be odd numbers. Default is 3.
    interpolate_method_name (str): Name of the interpolation method for image processing. Can be any interpolation method supported by PIL.Image.resize. Default is "LANCZOS".
    grayscale (float): Whether to convert the image to grayscale. Default is 0.

    Returns:
    list: A list containing the masked images. Should only contains one image. Each item is a PIL.Image.
    """

    tokenizer, model, image_processor, context_len, inner_model_name = get_model(model_name)
    hl = hook_logger(model, model.device, layer_index = layer_index)

    interpolate_method = getattr(Image, interpolate_method_name)
    masked_images = []

    for image_path_or_pil_image, question in zip(images, queries):
        with torch.no_grad():
            mask_args = type('Args', (), {
                    "hl":      hl,
                    "model_name": model_name,
                    "model": model,
                    "tokenizer": tokenizer,
                    "image_processor": image_processor,
                    "context_len": context_len,
                    "query": question,
                    "conv_mode": None,
                    "image_file": image_path_or_pil_image,
                    "sep": ",",
                    "temperature": 0,
                    "top_p": None,
                    "num_beams": 1,
                    "max_new_tokens": 20,
                })()
            mask, output = getmask(mask_args)
            merged_image = blend_mask(image_path_or_pil_image, mask, enhance_coe, kernel_size, interpolate_method, grayscale)
            masked_images.append(merged_image)

    return masked_images