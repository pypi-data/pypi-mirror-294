from setuptools import setup, find_packages

setup(
    name='IdentificationOfClaims',           
    version='0.1.1',
    packages=find_packages(),
    author='Manav',
    description='Identifies Claims from Text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=['google-generativeai','pandas','scikit-learn','numpy','nltk','rouge','scipy','python-dotenv'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
