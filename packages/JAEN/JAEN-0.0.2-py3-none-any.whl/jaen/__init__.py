from setuptools import setup, find_packages

setup(
    name='JAEN',
    version='0.0.2',
    description='차별화된 실무중심 교육',
    author='baem1n',
    author_email='baemin.dev@gmail.com',
    url='https://www.jaen.kr/',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'IPython'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
