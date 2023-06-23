from setuptools import setup, find_packages

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pystructurizr',
    version='0.1.2',
    description='A Python DSL inspired by Structurizr, intended for generating C4 diagrams',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Niels Vanspauwen',
    author_email='niels.vanspauwen@gmail.com',
    license='MIT',
    url='https://github.com/nielsvanspauwen/pystructurizr',
    data_files=[('', ['LICENSE.txt'])],
    packages=find_packages(),
    package_data={
        'pystructurizr': ['index.html'],
    },
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'pystructurizr = pystructurizr.cli:cli'
        ]
    },
)
