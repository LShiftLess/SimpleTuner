import os
from os import path
import shutil

import numpy as np
from PIL import Image
import torch
import torchvision
from torchvision.transforms import transforms
import torchvision.transforms.functional as F
from PIL import ImageFile
from tqdm import tqdm

ImageFile.LOAD_TRUNCATED_IMAGES = True
device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.mps.is_available() else 'cpu'

root = path.join(path.dirname(__file__), 'datasets')
cache_root = path.join(path.split(root)[0], 'cache', 'datasets')

target_dirs = [
    "anime-girls-r",
]

image_exts = [".png", ".jpg", ".jpeg"]

target_dirs = [path.join(root, dir) for dir in target_dirs]
cache_dirs = []

class SquarePad:
    def __init__(self, fill: int | float = 0x00000000):
        self.fill = fill

    def __call__(self, image: torch.Tensor):
        s = image.size()
        max_wh = np.max([s[-1], s[-2]])
        hp = int((max_wh - s[-1]) / 2)
        vp = int((max_wh - s[-2]) / 2)
        padding = (hp, vp, hp, vp)
        return F.pad(image, padding, 0, 'constant')

     
img_transformer = transforms.Compose([
    transforms.PILToTensor(),
    lambda tensor: tensor.to(device),
    SquarePad(),
    transforms.Resize((1024, 1024)),
    transforms.ToPILImage(),
])

# Rebuild cache root of datasets
shutil.rmtree(cache_root, ignore_errors=True)
os.makedirs(cache_root)


# MOVE TO CACHE
task_name = 'cache'
for target_dir in tqdm(target_dirs, desc=task_name, colour='#dd0000'):

    dataset_name = path.split(target_dir)[1]
    dest_dir = path.join(cache_root, dataset_name)
    cache_dirs.append(dest_dir)

    os.makedirs(dest_dir)

    for file in tqdm(os.listdir(target_dir), desc=f'{task_name} (id={dataset_name})'):
        dest_file = path.join(dest_dir, file)
        file = path.join(target_dir, file)
        shutil.copy(file, dest_file)        


# RESIZE 
task_name = 'resize'
for cache_dir in tqdm(cache_dirs, desc=task_name, colour='#dd0000'):
    dataset_name = path.split(cache_dir)[1]

    for file in tqdm(os.listdir(cache_dir), desc=f'{task_name} (id={dataset_name})'):

        file_ext = path.splitext(file)[1]

        if file_ext in image_exts:
            file = path.join(cache_dir, file)
            img = Image.open(file)
            img = img_transformer(img)
            img.save(file, format="PNG")


# GENERATE TEXTFILES
task_name = 'text files'
for cache_dir in tqdm(cache_dirs, desc=task_name, colour='#dd0000'):
    dataset_name = path.split(cache_dir)[1]

    for file in tqdm(os.listdir(cache_dir), desc=f'{task_name} (id={dataset_name})'):
        ext_splitted_file = path.splitext(file)
        file_name = ext_splitted_file[0]
        file_ext = ext_splitted_file[1]
        if file_ext in image_exts:
            text_file = path.join(cache_dir, f'{file_name}.txt')
    
            with open(text_file, 'w') as f:
                id = '_' + file_name.split('_')[-1]
                content = file_name.removesuffix(id) + '.'
                f.write(content)
        
        elif file_ext in ['.pt', '.json']:
            os.remove(path.join(cache_dir, file))

