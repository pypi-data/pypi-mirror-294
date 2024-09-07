from setuptools import setup, find_packages

setup(
    name='klaudlytics',                   
    version='0.1.5',                      
    author='Omoleye Julius',              
    author_email='julius.omoleye@outlook.com',
    description='Cloud cost optimization tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/geek0ps/klaudlytics',
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
    entry_points={                           # Add this section
        'console_scripts': [
            'klaudlytics=klaudlytics.main:main',  # Command:module:function
        ],
    },
)
