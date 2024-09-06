package_path  = "/Users/prabhatkumar/Downloads/feature_engineering_package"
package_name = package_path.split("/")[-1]


import os
from setuptools import find_packages, setup

from pip._internal.network.session import PipSession
from pip._internal.req import parse_requirements
__version__  = "0.0.1"


if __name__ == '__main__':
    # parse_requirements() returns generator of pip.req.InstallRequirement objects
    os.environ['VERSION']=__version__
    with open(f'{package_path}/requirements.txt') as fd:
        data = fd.read()
        data = os.path.expandvars(data)

    with open(f'{package_path}/requirements.txt','w') as fd:
        fd.write(data)

    install_reqs = parse_requirements(f'{package_path}/requirements.txt', session=PipSession())

    reqs = [str(ir.requirement) for ir in install_reqs]

    setup(
        name=package_name,
        version=__version__,
        packages=find_packages(include=[f'{package_path}/{package_name}',f'{package_path}/{package_name}.*']),
        # package_data={'rule_engine': ['default_rule_engine_settings.yaml'], 'pipelining.settings': ['default_pipelining_settings.yaml'], 'asgard.resources': ['asgard_serving_settings.yaml'], 'asgard.store.job_template': ['owner_info.json']},
        install_requires=reqs,
        license='',
        author='MLOps Group',
        author_email='ml-dev@zeptonow.com',
        description="Zepto MLOps Services",
        long_description="test_package_distribution",
        long_description_content_type='text/markdown',
        classifiers=[
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
        ],
        include_package_data=True,
        python_requires='>=3.8'
    )


