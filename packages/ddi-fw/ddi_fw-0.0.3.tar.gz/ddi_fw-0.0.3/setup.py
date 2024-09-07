from setuptools import setup, find_packages
setup(
name='ddi_fw',
version='0.0.3',
author='Kıvanç Bayraktar',
author_email='bayraktarkivanc@gmail.com',
description='Do not use :)',
# packages=find_packages(),
packages=['ddi_fw/datasets','ddi_fw/drugbank','ddi_fw/experiments','ddi_fw/ner','ddi_fw/utils'],
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
)