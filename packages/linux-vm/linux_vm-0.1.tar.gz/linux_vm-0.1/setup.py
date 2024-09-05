from setuptools import setup, find_packages

setup(
    name='linux_vm',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'docker',  # Assuming Docker Python SDK is needed, though it might not be used directly
        'http',
    ],
    entry_points={
        'console_scripts': [
            'create-linux-vm=my_package.linux_vm:create_linux_vm',
            'start-linux-vm=my_package.linux_vm:start_linux_vm',
            'stop-linux-vm=my_package.linux_vm:stop_linux_vm',
            'start-webserver=my_package.webserver:start_webserver',
        ],
    },
    description='A package to manage a Docker-based Linux VM and start a web server.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Souporno Chakraborty',
    author_email='shrabanichakraborty83@gmail.com',
    url='https://github.com/Tirthaboss/linux_vm',
)