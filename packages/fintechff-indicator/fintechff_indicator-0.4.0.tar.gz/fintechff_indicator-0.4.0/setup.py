from setuptools import setup, find_packages

setup(
    name="fintechff_indicator",  # 你的包的名称
    version="0.4.0",  # 包的版本
    description="A python package for providing fintech indicators",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Jonathan Lee",
    author_email="lihuapinghust@gmail.com",
    url="https://github.com/lihuapinghust/fintechff_indicator",  # 项目的URL
    packages=find_packages(),  # 自动发现包
    install_requires=[  # 你的包依赖的库
        "backtrader",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
