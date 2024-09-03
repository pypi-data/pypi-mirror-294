# setup.py

from setuptools import setup, find_packages

setup(
    name='django-visit-tracker',
    version='0.1.0',
    packages=find_packages(include=['trackproject', 'trackproject.*']),
    include_package_data=True,
    install_requires=[
        'Django>=5.1',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.10',
)
