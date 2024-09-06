from setuptools import setup, find_packages

setup(
    name='odoo_designer_scaffold',
    version='0.1',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'create-scaffold = odoo_designer_scaffold: create_scaffold',
        ],
    }
)