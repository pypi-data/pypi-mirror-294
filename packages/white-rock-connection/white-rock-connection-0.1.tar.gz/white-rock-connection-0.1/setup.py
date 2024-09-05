from setuptools import setup, find_packages

setup(
    name='white-rock-connection',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'redis',
        'telepot',
        'requests',
        'pyyaml'
    ],
    author='Baoba investimentos - White rock project',
    author_email='baoba.whiterock@gmail.com',
    description='Library to connect modules whith broker and message apps',
    url='https://github.com/Baoba-Investimentos/white-rock-connection',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
