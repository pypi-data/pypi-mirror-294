import setuptools

with open("README.md", 'r', encoding="utf-8") as f:
  readme = f.read()

setuptools.setup(
  name="inkpylib",
  version="0.0.1",
  author="inksha",
  author_email="inksha@inksha.com",
  description="python develop library for inksha",
  long_description=readme,
  long_description_content_type="text/markdown",
  url="https://github.com/InkSha/pylib",
  packages=setuptools.find_packages(),
  classifiers={
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  }
)
