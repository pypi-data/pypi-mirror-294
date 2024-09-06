from setuptools import setup, find_packages

setup(
    name='dong_library_ddfdfafddfdfafd111',
    version='0.3.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='A short description of your library',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/my_library',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'antlr4-python3-runtime',
        'pydot',
        'pyyaml',
    ],
)