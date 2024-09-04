from setuptools import setup

setup(
	name='lihp2p_kit_py',
	version='0.0.9',
	packages=[
		'libp2p_kit_py',
	],
	install_requires=[
		'datasets',
		'urllib3',
		'requests',
		'boto3',
        'toml',
	],
    package_data={
        'libp2p_kit_py': [
            'aria2_kit',
			's3_kit',
			'websocket_kit',
			'websocket_kit_lib',
			'libp2p_kit',
        ]
    },
	include_package_data=True,
)