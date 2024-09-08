import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyplas",
    version="0.2.0",
    author="Julian Held",
    author_email="julian.held@umn.edu",
    license='MIT',
    platforms=['any'],
    description="Basic library for low-temperature plasmas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mimurrayy/pyplas",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy>=1.23.5', 'scipy>=1.13.0', 'mendeleev>=0.13.0'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.9',
)