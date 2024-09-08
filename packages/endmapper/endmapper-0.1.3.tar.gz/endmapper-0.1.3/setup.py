from setuptools import setup, find_packages
import glob
import os

scripts = [f for f in glob.glob(os.path.join('bin', '*')) if os.path.isfile(f)]

setup(
    name='endmapper',
    version='0.1.3',
    packages=find_packages(),
    include_package_data=True,
    scripts=scripts,
    install_requires=[
        # добавьте зависимости, если есть
    ],
    test_suite='tests',
)