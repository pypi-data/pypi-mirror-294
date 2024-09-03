from setuptools import setup

setup(
	name='ipfs_model_manager_py',
	version='0.0.13',
	packages=[
		'ipfs_model_manager_py',
	],
	install_requires=[
        'ipfs_kit_py',
        'orbitdb_kit_py',
        'libp2p_kit_py',
        'ipfs_datasets_py',
		'datasets',
		'urllib3',
		'requests',
		'boto3',
        'toml',
	],
    package_data={
		'ipfs_model_manager_py': [
		's3_kit/s3_kit.py',
        'test/test_fio.py',
        'test/test_hf_ipfs.py',
        'config/config.py',
        'aria2/aria2.py',
        'aria2/aria2c',
        'config/config_template.toml',
        'config/config.toml',
        'config/__init__.py',
        'config/config.py',
		]
	},
	include_package_data=True,
)