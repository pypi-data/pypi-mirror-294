from setuptools import setup, find_packages

setup(
    name='douroucoulisay',
    version='0.1.1.6',
    packages=find_packages(),
    entry_points={
    'console_scripts': [
        'douroucoulisay=douroucoulisay.douroucoulisay:main',  # main function should handle argparse and call douroucoulisay
        ],
    },
    install_requires=["playsound"],
    include_package_data=True,
    package_data={
        '': ['assets/*.txt'],
    },
    author='Aotus Parisinus',
    author_email='douroucoulis-fr@gmail.com',
    description='A package to print messages with douroucouli ASCII art.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/douroucoulis-fr/douroucoulisay.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
