import os
from distutils.command.build import build

from django.core import management
from setuptools import find_packages, setup

try:
    with open(
        os.path.join(os.path.dirname(__file__), "README.rst"), encoding="utf-8"
    ) as f:
        long_description = f.read()
except Exception:
    long_description = ""


class CustomBuild(build):
    def run(self):
        management.call_command("compilemessages", verbosity=1)
        build.run(self)


cmdclass = {"build": CustomBuild}


setup(
    name="pretix_net_mail",
    version='1.5.0',
    description="Custom HTML Email Renderer for NETWAYS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/NETWAYS/pretix-email-net",
    author="NETWAYS GmbH",
    author_email="support@netways.de",
    license="Apache",
    install_requires=[],
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    cmdclass=cmdclass,
    entry_points="""
[pretix.plugin]
pretix_net_mail=pretix_net_mail:PretixPluginMeta
""",
)

