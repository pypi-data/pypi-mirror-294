from setuptools import setup, find_packages

setup(
    name='elatentlpips',
    version='0.0.1',
    description='LatentLPIPS Similarity metric"',
    author='mingukkang',
    author_email='mgkang@postech.ac.kr',
    url='https://github.com/mingukkang/e-latentlpips',
    install_requires=['tqdm', 'pandas', 'scikit-learn', "torch>=0.4.0", "torchvision>=0.2.1", "numpy>=1.14.3", "scipy>=1.0.1", "scikit-image>=0.13.0", "opencv-python>=2.4.11", "matplotlib>=1.5.1", "tqdm>=4.28.1", "diffusers"],
    packages=['elatentlpips'],
    keywords=['elatentlpips', 'latentlpips', 'perceptual_metric'],
    python_requires='>=3.6',
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
