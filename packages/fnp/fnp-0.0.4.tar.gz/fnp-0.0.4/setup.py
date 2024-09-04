from setuptools import setup

classifierss=[
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 11',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='fnp',
    version='0.0.4',
    description='A module that lets you extract column from an excel file and plot it.',
    long_description='A module that lets you extract column from an excel file and plot it.',
    author='Sushruta Das',
    author_email='sushrutadas0@gmail.com',
    classifiers=classifierss,
    packages=['fnp'],
    install_requires=['pandas','matplotlib','numpy']
)