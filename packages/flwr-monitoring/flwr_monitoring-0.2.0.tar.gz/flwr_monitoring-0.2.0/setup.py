from setuptools import setup, find_packages

setup(
    name='flwr_monitoring',
    version='0.2.0',
    description='A package for monitoring Flower federated learning framework using Prometheus and WandB',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Kandola',
    author_email='vishalsg42@gmail.com',
    url='https://github.com/kandola-network/KanFL',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True, 
    install_requires=[
        'flwr==1.10.0',
        'GPUtil==1.4.0',
        'psutil==6.0.0',
        'prometheus-client==0.20.0',
        'wandb==0.17.7',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.7',
)
