from setuptools import setup, find_packages

setup(
    name='terraform-chart',
    version='0.1',
    packages=find_packages(),  # Automatically find all packages
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'terraform-chart=terraform_chart.terraform_cli:cli',
        ],
    },
    package_data={
        'terraform_chart': ['terraform.sh'],  # Include terraform.sh in the package
    },
    include_package_data=True,
)