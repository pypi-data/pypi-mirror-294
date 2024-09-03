from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='tmark',
    version='0.0.2',
    author='OnisOris',
    author_email='onisoris@yandex.ru',
    description='Time marking package in code.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/OnisOris/tmark',
    packages=find_packages(),
    install_requires=['matplotlib', 'numpy', 'pandas'],
    classifiers=[
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent'
    ],
    keywords='time marks plot',
    project_urls={
        'GitHub': 'https://github.com/OnisOris/tmark'
    },
    python_requires='>=3.10'
)
