from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_desciption = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="katiag_image_processing",
    version="0.0.1",
    author="Katia",
    description="Image Processing Package using Skimage",
    long_description=page_desciption,
    long_description_content_type="text/markdown",
    url="https://github.com/kriskacg/katiag-image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.12.5',
)