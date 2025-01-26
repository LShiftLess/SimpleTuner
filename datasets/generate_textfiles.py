import os
from os import path

from tqdm import tqdm


root = path.dirname(__file__)
cache_dir = path.join(path.split(root)[0], 'cache')
cache_root = path.join(cache_dir, 'datasets')

target_dirs = [
    'anime-girls',
    'anime-girls-r18',
]

image_exts = ['.png', '.jpg', '.jpeg']

target_dirs = [path.join(cache_root, dir) for dir in target_dirs]

for target_dir in tqdm(target_dirs, colour='#ff0000'):
    for file in tqdm(os.listdir(target_dir)):
        ext_splitted_file = path.splitext(file)
        file_name = ext_splitted_file[0]
        file_ext = ext_splitted_file[1]
        if file_ext in image_exts:
            text_file = path.join(target_dir, f'{file_name}.txt')
    
            with open(text_file, 'w') as f:
                id = '_' + file_name.split('_')[-1]
                content = file_name.removesuffix(id)
                f.write(content)
        
        elif file_ext in ['.pt', '.json']:
            os.remove(path.join(target_dir, file))
