from setuptools import setup, find_packages

required_packages = ['numpy==1.23.5', 'tensorflow', 'opencv-python', 'spams-bin',
                     'scikit-image', 'scipy', 'torchvision', 'dominate', 
                     'visdom', 'pillow', 'imageio', 'tqdm', 'lmdb', 'staintools', 
                     'fitter', 'pyyaml'
                     ]

setup(
    name='LBBNorm',
    version='1.6.0',
    packages=find_packages('src'),
    author='Laboratory of Systems Biology and Bioinformatics (LBB)',
    author_email='amasoudin@ut.ac.ir',
    description='Empower Your Tomorrow, Conquer the Future!',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',
    package_dir={'': 'src'},
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Medical Science Apps.',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
    ],
    keywords='Healthcare Bio-Informatics',
    install_requires=required_packages,
)
