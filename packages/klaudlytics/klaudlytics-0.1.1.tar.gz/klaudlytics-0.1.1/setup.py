from setuptools import setup, find_packages

setup(
    name='klaudlytics',                   
    version='0.1.1',                      
    author='Omoleye Julius',              
    author_email='your.email@example.com',
    description='Cloud cost optimization tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/your_username/klaudlytics',
    packages=find_packages(),             
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',              
    install_requires=[
        'boto3', 
        'pyyaml',
        'termcolor'  
    ],
)
