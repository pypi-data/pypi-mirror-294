from setuptools import setup, find_packages
    
setup(
    name='roop_cache',
    version='0.0.2',
    description='Generic package which can be used for caching purpose locally',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Roopendra',
    author_email='roopendra.naik@informa.com',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
