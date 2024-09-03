from setuptools import setup, find_packages

setup(
    name='tempdb-py',
    version='1.0.0',
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
    description='A Python client for interacting with TempDB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Thembinkosi Mkhonta',
    author_email='thembinkosimkhonta01@gmail.com',
    url='https://github.com/ThembinkosiThemba/tempdb-py', 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    license='MIT',
    python_requires=">=3.6",
)
