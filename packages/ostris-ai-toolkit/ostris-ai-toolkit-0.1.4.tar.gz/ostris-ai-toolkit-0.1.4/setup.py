from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
import os

with open("ai-toolkit/README.md", "r", encoding="utf-8") as fh:
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
    name="ostris-ai-toolkit",
    version="0.1.4",
    author="Cozy Creator",
    author_email="teggyg123@gmail.com",
    description="A toolkit for AI-related tasks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cozy-creator/ai-toolkit",
    package_dir={"ostris_ai_toolkit": "ai-toolkit"},
    packages=['ostris_ai_toolkit'] + [f'ostris_ai_toolkit.{pkg}' for pkg in find_packages(where="ai-toolkit")],
    include_package_data=True,
    package_data={'': ['*']},
    exclude_package_data={
        '': ['.venv', '.git', '.github', '__pycache__', '*.pyc', 'repositories', '.gitignore', '.gitmodules', 'LICENSE'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
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
        "python-slugify",
    ],
    dependency_links=[
        "git+https://github.com/Leommm-byte/LECO.git#egg=LECO",
        "git+https://github.com/Leommm-byte/sd-scripts.git#egg=sd-scripts",
        "git+https://github.com/tencent-ailab/IP-Adapter.git#egg=IP-Adapter",
    ],
    cmdclass={
        'develop': DevelopWithSubmodules,
        'install': InstallWithSubmodules,
    },
)