from setuptools import setup, find_packages

setup(
    name='douroucoulisay',
    version='0.1.1.8.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'douroucoulisay=douroucoulisay.douroucoulisay:main',  # Main CLI for ASCII art and message
            'tonal_hoot=douroucoulisay.douroucoulisay:tonal_hoot',  # CLI for tonal hoot
            'gruff_hoot=douroucoulisay.douroucoulisay:gruff_hoot',  # CLI for gruff hoot
            'whoop=douroucoulisay.douroucoulisay:whoop',  # CLI for whoop
        ],
    },
    install_requires=["pydub"],  # Corrected package name
    include_package_data=True,
    package_data={
        '': ['assets/*.txt', 'assets/*.wav'],  # Including both text and sound files
    },
    author='Aotus Parisinus',
    author_email='douroucoulis-fr@gmail.com',
    description='A package to print messages with douroucouli ASCII art and sounds.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/douroucoulis-fr/douroucoulisay.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
