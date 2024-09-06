from setuptools import setup, find_packages

setup(
    name="gmlp_tinygrad",
    version="0.9.1",
    packages=find_packages(),
    install_requires=[
        "tinygrad",
        "einops",
        "numpy"
    ],
    description="An implementation of gated MLPs in tinygrad, as an alternative to transformers.",
    author="Ethan Bennett"
)