from setuptools import setup, find_packages

setup(
    name="ai_tools_zxw",
    version="2.8.9",
    packages=find_packages(),
    install_requires=[
        'xlwt',
        'psutil',
    ],
    author="xue wei zhang",
    author_email="",
    description="常用的人工智能操作的中文工具包。",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunshineinwater/",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
