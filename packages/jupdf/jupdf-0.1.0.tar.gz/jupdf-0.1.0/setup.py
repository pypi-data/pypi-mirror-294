from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    description = f.read()

setup(
    name='jupdf',
    version='0.1.0',
    packages=find_packages(),
    package_data={
        'jupdf': ['tex/*.tex'],
    },
    include_package_data=True,
    install_requires=[
        'PyMuPDF>=1.24.10',
        'PyMuPDFb>=1.24.10',
        'pandocfilters>=1.5.1'
    ],
    long_description=description,
    long_description_content_type='text/markdown',
)