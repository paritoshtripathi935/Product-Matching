import os

# Create main folders
folders = ['data', 'notebooks', 'src', 'tests']
for folder in folders:
    os.makedirs(folder)

# Create subfolders inside data folder
data_folders = ['raw', 'processed', 'models']
for folder in data_folders:
    os.makedirs(os.path.join('data', folder))

# Create subfolders inside src folder
src_folders = ['models', 'preprocessing', 'utils']
for folder in src_folders:
    os.makedirs(os.path.join('src', folder))

# Create sample files inside the folders
with open(os.path.join('data', 'raw', 'data.csv'), 'w') as f:
    f.write('Sample raw data')

with open(os.path.join('data', 'processed', 'data.csv'), 'w') as f:
    f.write('Sample processed data')

with open(os.path.join('data', 'models', 'model.pkl'), 'wb') as f:
    f.write(b'Sample model pickle file')

with open(os.path.join('src', 'models', 'model.py'), 'w') as f:
    f.write('Sample model source code')

with open(os.path.join('src', 'preprocessing', 'preprocessing.py'), 'w') as f:
    f.write('Sample preprocessing source code')

with open(os.path.join('src', 'utils', 'utils.py'), 'w') as f:
    f.write('Sample utility source code')

with open(os.path.join('notebooks', 'EDA.ipynb'), 'w') as f:
    f.write('Sample Jupyter notebook for EDA')

with open(os.path.join('tests', 'test_models.py'), 'w') as f:
    f.write('Sample unit tests for models')
