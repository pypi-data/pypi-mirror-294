from setuptools import setup, find_packages

setup(
    name='dahood',
    version='0.0.2',
    packages=find_packages(),
    description='Dahood is used for LuaU implementation into Python projects, used by celex and howl',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Minimum Python version required
)