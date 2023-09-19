from distutils.core import setup
from setuptools import find_packages

options = {'apk': {'debug': None,  # use None for arguments that don't pass a value
                   'requirements': 'sdl2,pyjnius,kivy,python3',
                   'android-api': 19,
                   'ndk-dir': '/path/to/ndk',
                   'dist-name': 'bdisttest',
                   }}

packages = find_packages()
print('packages are', packages)

setup(
    name='testapp_setup',
    version='1.1',
    description='p4a setup.py example',
    author='Your Name',
    author_email='youremail@address.com',
    packages=find_packages(),
    options=options,
    package_data={'testapp': ['*.py', '*.png']}
)