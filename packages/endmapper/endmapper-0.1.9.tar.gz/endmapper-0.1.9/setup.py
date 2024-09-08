from setuptools import setup, find_packages

setup(
    name='endmapper',
    version='0.1.9',
    packages=find_packages(),  # Это автоматически найдет все пакеты в вашем проекте
    include_package_data=True,
    package_data={
        # Указываем, что нужно включить файлы из директории 'bin'
        'endmapper': ['bin/*.py'],
    },
    install_requires=[
        # добавьте зависимости, если есть
    ],
    # Если вы используете README, убедитесь, что файл не пуст
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    # Указываем, что будет включено в дистрибутив
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
