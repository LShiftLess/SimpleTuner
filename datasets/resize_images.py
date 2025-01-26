import os
from os import path
from PIL import Image
from torchvision.transforms import transforms
from PIL import ImageFile
from tqdm import tqdm

ImageFile.LOAD_TRUNCATED_IMAGES = True

root = path.dirname(__file__)
cache_dir = path.join(path.split(root)[0], 'cache')
cache_root = path.join(cache_dir, 'datasets')

target_dirs = [
    "anime-girls",
    "anime-girls-r18",
]

image_exts = [".png", ".jpg", ".jpeg"]

target_dirs = [path.join(root, dir) for dir in target_dirs]

transformer = transforms.Compose([
    transforms.Resize((1024, 1024))
])

os.makedirs(cache_dir, exist_ok=True)
os.makedirs(cache_root, exist_ok=True)

for target_dir in tqdm(target_dirs, colour='#ff0000'):

    dataset_name = path.split(target_dir)[1]
    dest_dir = path.join(cache_root, dataset_name)

    os.makedirs(dest_dir, exist_ok=True)

    for file in tqdm(os.listdir(target_dir)):

        file_ext = path.splitext(file)[1]

        if file_ext in image_exts:
            dest_file = path.join(dest_dir, file)
            file = path.join(target_dir, file)

            img = Image.open(file)

            img = transformer(img)

            img.save(dest_file, format="PNG")
            
