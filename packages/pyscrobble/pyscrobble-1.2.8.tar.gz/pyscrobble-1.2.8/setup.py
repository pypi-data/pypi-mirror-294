from setuptools import setup, find_packages

setup(
    name='pyscrobble',
    version='1.2.8',
    description='A Python package for interacting with the Last.fm API',
    long_description=open('README.md').read(),
    url="https://github.com/opexdeveloper/pyscrobble",
    long_description_content_type='text/markdown',
    author='Claqz',
    author_email='lastfm@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'xmltodict>=0.12.0',
    ],
    extras_require={
        'dev': [
            'pytest>=6.2.5',
            'flake8>=3.9.2',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    python_requires='>=3.9',
)
