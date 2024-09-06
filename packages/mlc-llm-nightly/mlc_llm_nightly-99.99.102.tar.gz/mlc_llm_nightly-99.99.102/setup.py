from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install
import __main__

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)

setup(
    name="mlc-llm-nightly",
    version="99.99.102",
    description="PoC. Contact RedYetiHacks@wearehackerone.com for information.",
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    },
)