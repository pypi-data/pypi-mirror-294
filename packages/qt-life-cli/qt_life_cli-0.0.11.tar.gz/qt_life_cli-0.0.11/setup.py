from setuptools import setup, find_packages

setup(
    name='qt-life-cli',
    version='0.0.11',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click==8.1.3',
        'prompt_toolkit==3.0.38',
        'colorama==0.4.6',
    ],
    entry_points='''
        [console_scripts]
        qt=qt_life_cli.main:cli
    ''',
    author='Anonymous',
    author_email='anonymous@qtlife.com',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)