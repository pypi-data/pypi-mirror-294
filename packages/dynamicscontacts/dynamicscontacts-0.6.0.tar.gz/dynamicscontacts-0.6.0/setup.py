from setuptools import setup
setup(
    name='dynamicscontacts',
    version='0.6.0',
    description='This library provides developers with a simplified way to authenticate, search contact, add contact, and update contact in Dynamics Customer Insights - Journeys ',
    author='Dr. Mustafa Abusalah',
    author_email='muabusalah@gmail.com',
    url='https://github.com/mabusalah/Dynamics',
    packages=['dynamics'],
    install_requires=['requests'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)