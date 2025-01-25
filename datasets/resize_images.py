import os
from os import path
from PIL import Image
from torchvision.transforms import transforms
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True

root = path.dirname(__file__)

target_dirs = [
    "anime-girls",
    "anime-girls-r18",
]

image_exts = [".png", ".jpg", ".jpeg"]

target_dirs = [path.join(root, dir) for dir in target_dirs]

transformer = transforms.Compose([transforms.Resize((1024, 1024))])

for target_dir in target_dirs:

    dest_folder = f"{target_dir}-resized"
    os.makedirs(dest_folder, exist_ok=True)

    for file in os.listdir(target_dir):

        file_ext = path.splitext(file)[1]

        if file_ext in image_exts:
            dest_file = path.join(dest_folder, file)
            file = path.join(target_dir, file)

            img = Image.open(file)

            img = transformer(img)

            img.save(dest_file, format="PNG")
            print(f"Save resized image as {dest_file}")
            
