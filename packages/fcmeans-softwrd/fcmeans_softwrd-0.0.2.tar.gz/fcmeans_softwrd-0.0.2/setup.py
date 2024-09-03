from setuptools import setup, find_packages

setup(
    name="fcmeans_softwrd",
    version="0.0.2",
    author="Kazi Ferdous Mahin, Proshanta Kumer Das",
    author_email="mahin@softwrd.ai, proshanto@softwrd.ai",
    description="A Python package of Fuzzy-C-means algorithm for softwrd data and ml team.",
    long_description=open('README.md').read(),  # Ensure you have a README.md file
    long_description_content_type="text/markdown",
    url="https://github.com/softwrdai/ml-fuzzy-c-means",  # Replace with your repo URL
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.9',
    install_requires=[
        "boto3",
        "pydantic",
        "tqdm",
        "typer"
    ]
)