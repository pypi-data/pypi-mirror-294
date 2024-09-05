import setuptools
from os import path

version = {}
here = path.abspath(path.dirname(__file__))

with open( path.join(here, 'README.md'), 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    
with open(path.join(here, 'mixnet/version.py'), encoding='utf-8') as (
        version_file):
    exec(version_file.read(), version)

setuptools.setup(
    name='mixnet-eeg',
    version=version['__version__'],
    author='Phairot Autthasan',
    author_email='phairot.a_s17@vistec.ac.th',
    description='MixNet: Joining Force of Classical and Modern Approaches toward The Comprehensive Pipeline in Motor Imagery EEG Classification',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Max-Phairot-A/MixNet',
    download_url='https://github.com/Max-Phairot-A/MixNet/releases',
    project_urls={
        'Bug Tracker': 'https://github.com/Max-Phairot-A/MixNet/issues',
        'Documentation': 'https://github.com/Max-Phairot-A/MixNet',
        'Source Code': 'https://github.com/Max-Phairot-A/MixNet'
    },
    license="Apache Software License",
    keywords=[
        'Brain-computer Interfaces',
        'BCI',
        'Deep learning',
        'DL'
        'Motor Imagery',
        'MI', 
        'Multi-task Learning',
        'Deep Metric Learning',
        'DML', 
        'Autoencoder',
        'AE',
        'Adaptive Gradient Blending',
        'EEG Classifier'        
    ],
    
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    install_requires = [
        # 'tensorflow-gpu==2.7.0' or 'tensorflow-gpu==2.8.2', not support tensorflow-gpu via pip
        'tensorflow-addons==0.16.1', 
        'scikit-learn>=1.2.2',
        'wget>=3.2',
        'ray>=1.11.0',
        'pandas'
    ],
    package_data= {
        # all .csv files at any package depth
        '': ['**/*.csv']
    },
    packages=setuptools.find_packages(),
    python_requires='>=3.7, <=3.10.4',

)

# tensorflow-gpu==2.7.0 # not support tensorflow-gpu via pip

