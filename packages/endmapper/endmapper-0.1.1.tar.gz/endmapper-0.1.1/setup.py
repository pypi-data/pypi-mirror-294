from setuptools import setup, find_packages

setup(
    name='endmapper',
    version='0.1.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # добавьте зависимости, если есть
    ],
    package_data={
        'endmapper': ['config/default_config.yaml'],
    },
    test_suite='tests',
)