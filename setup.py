from setuptools import setup

requires = [
        'twisted',
        'pyyaml']

setup(
        name="HxIRCD",
        version='0.1.0',
        description="The Helixoide IRCD",
        author='Ross Delinger',
        author_email='rossdylan@csh.rit.edu',
        packages=['hxirc'],
        install_requires=requires)
