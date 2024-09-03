from setuptools import setup, find_packages

setup(
    name="kleantrans",
    version="1.0.6",
    packages=find_packages(),
    include_package_data=True,  # Include data files specified in MANIFEST.in
    package_data={
        '': ['app/images/*'],  # Include all files from the images folder
    },
)
