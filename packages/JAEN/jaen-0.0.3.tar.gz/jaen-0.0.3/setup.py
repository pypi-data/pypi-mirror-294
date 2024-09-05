from setuptools import setup, find_packages
setup(
    name='JAEN',
    version='0.0.3',
    description='차별화된 자체 교육 콘텐츠와 실무 중심 교육',
    author='BAEM1N',
    author_email='baemin.dev@gmail.com',
    url='https://github.com/BAEM1N/JAEN',
    install_requires=['pandas'],
    packages=find_packages(exclude=[]),
    keywords=['AI', 'ML', 'DL'],
    python_requires='>=3',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
)
