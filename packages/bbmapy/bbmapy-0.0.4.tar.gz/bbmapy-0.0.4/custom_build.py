import os
import subprocess
import shutil
from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Run the original install command first
        install.run(self)

        # Change to vendor directory
        vendor_dir = os.path.join(self.install_lib, 'bbmapy', 'vendor')
        os.makedirs(vendor_dir, exist_ok=True)
        os.chdir(vendor_dir)
        
        # Remove existing BBTools files
        for item in os.listdir('.'):
            if item.startswith('bb'):
                if os.path.isdir(item):
                    shutil.rmtree(item)
                else:
                    os.remove(item)
        
        # Download and extract BBTools
        subprocess.run(['wget', 'https://pilotfiber.dl.sourceforge.net/project/bbmap/BBMap_39.08.tar.gz', '-O', 'bbtools.tar.gz'], check=True)
        subprocess.run(['tar', '-xf', 'bbtools.tar.gz'], check=True)
        os.remove('bbtools.tar.gz')  # Clean up the tarball
        
        # Change back to root directory
        os.chdir(self.install_lib)
        
        # Generate commands
        subprocess.run(['generate-bbmapy-commands'], check=True)

setup(
    name='bbmapy',
    version='0.0.4',  # Update this as needed
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'rich>=10.0.0',
    ],
    entry_points={
        'console_scripts': [
            'generate-bbmapy-commands=bbmapy.scanner:main',
        ],
    },
    cmdclass={
        'install': CustomInstallCommand,
    },
)