import os
from os import path


root = path.dirname(__file__)

subfolders = [
    'anime-girls',
    'anime-girls-r18'
]

image_exts = [
    '.png', '.jpg', '.jpeg'
]

subfolders = [path.join(root, subfolder) for subfolder in subfolders]

for subfolder in subfolders:
    for file in os.listdir(subfolder):
        ext_splitted_file = path.splitext(file)
        file_name = ext_splitted_file[0]
        file_ext = ext_splitted_file[1]
        if file_ext in image_exts:
            text_file = path.join(subfolder, f'{file_name}.txt')
    
            with open(text_file, 'w') as f:
                id = '_' + file_name.split('_')[-1]
                content = file_name.removesuffix(id)
                f.write(content)
        
        elif file_ext in ['.pt', '.json']:
            os.remove(path.join(subfolder, file))
