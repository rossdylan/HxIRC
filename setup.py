from setuptools import setup

requires = [
        'twisted',
        'pyopenssl',
        'pyyaml']

setup(
        name="HxIRCD",
        version='0.1.0',
        description="The Helixoide IRCD",
        author='Ross Delinger',
        author_email='rossdylan@csh.rit.edu',
        packages=[
            'hxirc',
            'hxirc.irc',
            'hxirc.config',
            ],
        install_requires=requires,
        data_files=[('/etc/hxircd.conf', 'config/hxircd.conf')],
        entry_points="""
        [console_scripts]
        hxircd = hxirc:main
        """)

