from distutils.core import setup

setup(
    name='CsvToArff',
    version='0.1.0',
    author='Gonzalo Almeida',
    author_email='flecox#gmail.com',
    packages=[],
    scripts=['csv_to_arff.py'],
    license='LICENSE.txt',
    description='Turn csv files to .arff used with weka.',
    long_description=open('README.rst').read(),
    install_requires=['liac-arff'],
)
