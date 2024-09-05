# setup.py
from setuptools import setup, find_packages

setup(
    name="rate_table_images",
    version="0.0.1",
    packages=find_packages(),
    install_requires=['pandas','xlsxwriter', 'matplotlib', 'dataframe-image'],
    entry_points={
        'console_scripts': [
            'create_images=rate_table_images.rate_table_images:main',
        ],
    },
    author="Aviral Srivastava",
    author_email="aviralsrivastava284@gmail.com",
    description="Get the Rate Table Images",
    long_description_content_type='text/markdown',
    url="https://github.com/A284viral/protections_v1",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)