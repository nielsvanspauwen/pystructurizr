from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='pystructurizr',
    version='0.1.0',
    description='A Python DSL inspired by Structurizr, intended for generating C4 diagrams',
    author='Niels Vanspauwen',
    author_email='niels.vanspauwen@gmail.com',
    packages=find_packages(),
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