from setuptools import setup, find_packages
from src import __version__

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='mangokit',
    version=__version__,
    description='测试工具',
    long_description=long_description,
    author='毛鹏',
    author_email='729164035@qq.com',
    url='https://gitee.com/mao-peng/testkit',
    packages=find_packages(),
    install_requires=[
        'jsonpath~=0.82.2',
        'cachetools~=5.3.1',
        'Faker~=19.6.0',
        'diskcache~=5.6.3',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
    ]
)

"""
python -m pip install --upgrade setuptools wheel
python -m pip install --upgrade twine
python setup.py check
python setup.py sdist bdist_wheel
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
"""
