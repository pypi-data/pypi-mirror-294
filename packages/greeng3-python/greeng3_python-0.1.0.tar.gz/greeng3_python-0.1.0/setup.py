from setuptools import setup, find_packages

setup(
    name='greeng3_python',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'bs4',
        'docker',
        'ebooklib',
        'isbn',
        'nltk',
        'requests',
    ],
    author='Gordon Greene',
    author_email='greeng3@obscure-reference.com',
    description='A library of things I find useful.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.com/greeng3/greeng3_python',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
)
