"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pyatcoder',
    version='0.2.0',
    description='AtCoder Python Tools',
    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    # keywords='sample setuptools development',
    packages=find_packages(exclude=('tests',)),
    python_requires='>=3.6, <4',
    install_requires=['pythran', 'requests', 'beautifulsoup4', 'toml'],  # Optional
    entry_points={
        'console_scripts': [
            'pyatcoder=pyatcoder.main:main',
        ],
    },
)