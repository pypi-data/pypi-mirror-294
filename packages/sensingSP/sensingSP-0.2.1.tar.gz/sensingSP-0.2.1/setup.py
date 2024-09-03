from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Define the required dependencies
install_requires = [
    'bpy>=4.0.0',
    'certifi>=2024.7.4',
    'charset-normalizer>=3.3.2',
    'contourpy>=1.2.1',
    'cycler>=0.12.1',
    'Cython>=3.0.11',
    'fonttools>=4.53.1',
    'idna>=3.7',
    'kiwisolver>=1.4.5',
    'llvmlite>=0.43.0',
    'mathutils>=3.3.0',
    'matplotlib>=3.7.1',
    'numba>=0.60.0',
    'numpy>=1.26.4',
    'opencv-python>=4.10.0.84',
    'packaging>=24.1',
    'pillow>=9.4.0',
    'pyparsing>=3.1.2',
    'python-dateutil>=2.8.2',
    'requests>=2.32.3',
    'scipy>=1.13.1',
    'six>=1.16.0',
    'urllib3>=2.0.7',
    'zstandard>=0.23.0',
]

setup(
    name='sensingSP',
    version='0.2.1',
    packages=find_packages(),
    install_requires=install_requires,  # Default includes all dependencies
    url='https://gitlab.com/sparc-snt/sensing-signal-processing',
    license='MIT',
    author='Moein Ahmadi',
    author_email='moein.ahmadi@uni.lu, gmoein@gmail.com',
    description='SensingSP™ is a Blender-based open-source library for simulating electromagnetic-based sensing systems and radar signal processing algorithms implementations.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
    extras_require={
        'no_additional_packages': [],  # This allows installing without additional packages
    },
)
