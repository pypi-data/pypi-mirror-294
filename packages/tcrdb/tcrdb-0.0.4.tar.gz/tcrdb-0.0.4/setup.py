import os
import pathlib as p
import re as regex

import setuptools

PACKAGE_NAME = 'tcrdb'

version_file = p.Path(f'./{PACKAGE_NAME}/version.py')
version_pattern = r"__version__\s*=\s*[\"'](.*?)[\"']"

__version__ = regex.search(version_pattern, version_file.read_text()).group(1)


if __name__ == '__main__':
  setuptools.setup(
    name=PACKAGE_NAME,
    version=__version__,
    description='Base classes and utilities for simple python databases.',
    long_description=p.Path('./README.md').read_text(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/anamoyee/{PACKAGE_NAME}',
    author='anamoyee',
    license='GPL-3.0 license',
    project_urls={
      'Source': f'https://github.com/anamoyee/{PACKAGE_NAME}',
    },
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3.11',
      'Programming Language :: Python :: 3.12',
      'Topic :: Utilities',
    ],
    python_requires='>=3.11,<3.13',
    install_requires=p.Path('./requirements.txt').read_text().strip().split(),
    packages=setuptools.find_packages(),
    include_package_data=True,
  )
