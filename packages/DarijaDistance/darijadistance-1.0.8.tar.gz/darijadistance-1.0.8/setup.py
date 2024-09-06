from setuptools import setup

setup(
    name='DarijaDistance',
    version='1.0.8',
    description='A library for finding the closest words and calculating word distances for the Moroccan Dialect Darija',
    author='Aissam Outchakoucht',
    author_email='aissam.outchakoucht@gmail.com',
    url='https://github.com/aissam-out/DarijaDistance',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=['DarijaDistance'],
    include_package_data=True,
    package_data={
        'DarijaDistance': ['data/*'],
    },
    install_requires=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
)
