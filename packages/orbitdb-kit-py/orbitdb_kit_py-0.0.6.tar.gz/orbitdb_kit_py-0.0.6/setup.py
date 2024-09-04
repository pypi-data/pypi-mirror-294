from setuptools import setup

setup(
	name='orbitdb_kit_py',
	version='0.0.6',
	packages=[
		'orbitdb_kit_py',
	],
	install_requires=[
		'datasets',
		'urllib3',
		'requests',
		'boto3',
        'toml',
        'websocket'
	],
    package_data={
        'orbitdb_kit': [
            'orbitv3-slave-swarm.js',
        	'package.json',
            'yarn.lock'
        ]
    },
	include_package_data=True,
)