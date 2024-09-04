# setup.py

from setuptools import setup, find_packages

setup(
    name='drf-email-auth',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'Django>=3.2',
        'djangorestframework',
        'djangorestframework-simplejwt',

    ],
    include_package_data=True,
    license='MIT License',
    description='A DRF package for email-based authentication',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/aakash-shakya/django-email-auth',
    author='Aakash Shakya',
    author_email='official.aakas@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
