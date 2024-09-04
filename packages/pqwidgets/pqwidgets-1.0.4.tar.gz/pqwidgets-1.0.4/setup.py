from setuptools import setup, find_packages
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='pqwidgets',
    version='1.0.4',
    description='A custom PyQt5 widgets package',
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author='majunggil',
    author_email='majunggil.work@gmailc.om',
    url='https://github.com/majunggil/PyQt5/tree/main/pqwidgets',
    packages=find_packages(),
    install_requires=[
        'PyQt5>=5.15.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
