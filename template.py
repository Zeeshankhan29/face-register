from pathlib import Path
import os
import logging





while True:
    project_name = input('Enter the project name  :  ')
    if project_name !='':
        break




list_of_files =[

    '.github/workflows/.gitkeep',
    '.github/workflows/main.yaml',
    f'src/{project_name}/__init__.py',
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/entity/__init__.py',
    f'src/{project_name}/constants/__init__.py',
    f'src/{project_name}/config/__init__.py',
    f'src/{project_name}/utils/__init__.py',
    f'src/{project_name}/pipeline/__init__.py',
    'configs/config.yaml',
    'requirements.txt',
    'setup.py',
    'main.py',
    '.gitignore',
    'README.md'

    
]


for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    
    if filedir !='':
        os.makedirs(filedir,exist_ok=True)
        logging.info(f'creating directory {filedir} for file {filename}')
    
    if not os.path.exists(filepath) or os.path.getsize(filepath)==0:
        with open(filepath,'w') as f:
            pass
        logging.info(f'Creating a empty {filename}')
    else:
        logging.info(f'file {filename} already exists')