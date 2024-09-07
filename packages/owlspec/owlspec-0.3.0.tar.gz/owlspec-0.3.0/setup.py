import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="owlspec",
    version="0.3.0",
    author="Julian Held",
    author_email="julian.held@umn.edu",
    license='MIT',
    platforms=['any'],
    description="Library for optical emission spectroscopy of low-temperature plasmas.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mimurrayy/owl",
    packages=setuptools.find_packages(),
    install_requires=[
          'numpy>=1.23.5', 'scipy>=1.13.0', 'mendeleev>=0.13.0', 'astroquery>=0.4.5', 'roman>=4.0', 'platformdirs>=4.2.0', 'pyplas>=0.2.0'
      ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10.9',
)
