from setuptools import setup, find_packages

setup(
    name="abdutils",  # Package name
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="A bag of utility functions.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/abdkhanstd/abdutils",
    author="ABD",
    author_email="abdkhan@163.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Pillow',
        'opencv-python',
        'matplotlib',
        'numpy',
        'GPUtil'
    ],
)

