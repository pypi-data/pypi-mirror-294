from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import os

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def init_submodules():
    """Initialize git submodules"""
    try:
        check_call(['git', 'submodule', 'update', '--init', '--recursive'])
    except Exception as e:
        print(f"An error occurred while initializing submodules: {e}")
        print("Continuing with installation...")

class DevelopWithSubmodules(develop):
    def run(self):
        init_submodules()
        develop.run(self)

class InstallWithSubmodules(install):
    def run(self):
        init_submodules()
        install.run(self)

setup(
    name="lora-train",
    version="0.1.0",
    author="Cozy Creator",
    author_email="teggyg123@gmail.com",
    description="A toolkit for AI-related tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cozy-creator/ai-toolkit",
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.pyc', '*.pyo', '*.pyd', '__pycache__', '*.so', '*.dll', '*.egg-info'],
        'tests': ['*'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "torch",
        "torchvision",
        "safetensors",
        "diffusers",
        "transformers",
        "lycoris-lora==1.8.3",
        "flatten_json",
        "pyyaml",
        "oyaml",
        "tensorboard",
        "kornia",
        "invisible-watermark",
        "einops",
        "accelerate",
        "toml",
        "albumentations",
        "pydantic",
        "omegaconf",
        "k-diffusion",
        "open_clip_torch",
        "timm",
        "prodigyopt",
        "controlnet_aux==0.0.7",
        "python-dotenv",
        "bitsandbytes",
        "hf_transfer",
        "lpips",
        "pytorch_fid",
        "optimum-quanto",
        "sentencepiece",
        "huggingface_hub",
        "peft",
        "gradio",
        "python-slugify"
    ],
    cmdclass={
        'develop': DevelopWithSubmodules,
        'install': InstallWithSubmodules,
    },
)