#!/usr/bin/env python

from setuptools import find_packages, setup

import os
import time

version_file = 'version.py'


def readme():
    with open('README.md', encoding='utf-8') as f:
        content = f.read()
    return content


def get_version():
    with open(version_file, 'r') as f:
        exec(compile(f.read(), version_file, 'exec'))
    return locals()['__version__']


def write_version_py():
    content = """# GENERATED VERSION FILE
# TIME: {}
__version__ = '{}'
__gitsha__ = '{}'
version_info = ({})
"""
    sha = 'unknown'  # 你可以修改为获取git hash的函数
    with open('VERSION', 'r') as f:
        SHORT_VERSION = f.read().strip()

    # 格式化 version_info
    VERSION_INFO = ', '.join([x if x.isdigit() else f'"{x}"' for x in SHORT_VERSION.split('.')])

    version_file_str = content.format(time.asctime(), SHORT_VERSION, sha, VERSION_INFO)

    # 确保文件正确写入到 version.py
    with open(version_file, 'w') as f:
        f.write(version_file_str)


def get_requirements(filename='requirements.txt'):
    here = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(here, filename), 'r') as f:
        requires = [line.replace('\n', '') for line in f.readlines()]
    return requires


if __name__ == '__main__':
    write_version_py()
    setup(
        name='NWUcellsr',
        version=get_version(),
        description='Your SDK description',
        long_description=readme(),
        long_description_content_type='text/markdown',
        author='Your Name',
        author_email='your.email@example.com',
        keywords='your, keywords, here',
        url='https://github.com/yourusername/yourrepo',
        include_package_data=True,
        packages=find_packages(exclude=('tests', 'docs')),
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
        license='MIT',
        setup_requires=['torch', 'flask'],  # List any build dependencies here
        install_requires=get_requirements(),
        zip_safe=False,
    )
