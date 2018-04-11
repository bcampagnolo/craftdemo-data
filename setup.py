from setuptools import setup, find_packages

setup(
    name='indecision',
    version='1.7',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
