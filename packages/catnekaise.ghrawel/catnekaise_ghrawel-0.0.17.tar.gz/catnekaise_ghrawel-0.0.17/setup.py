import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "catnekaise.ghrawel",
    "version": "0.0.17",
    "description": "Use ghrawel to deploy an AWS API Gateway RestAPI capable of returning GitHub App installation access tokens and use AWS IAM to control access to this API.",
    "license": "Apache-2.0",
    "url": "https://github.com/catnekaise/ghrawel.git",
    "long_description_content_type": "text/markdown",
    "author": "Daniel Jonsén<djonser1@gmail.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/catnekaise/ghrawel.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "catnekaise_ghrawel",
        "catnekaise_ghrawel._jsii"
    ],
    "package_data": {
        "catnekaise_ghrawel._jsii": [
            "ghrawel@0.0.17.jsii.tgz"
        ],
        "catnekaise_ghrawel": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.8",
    "install_requires": [
        "aws-cdk-lib>=2.82.0, <3.0.0",
        "catnekaise.cdk-iam-utilities>=0.0.30, <0.0.31",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.103.1, <2.0.0",
        "publication>=0.0.3",
        "typeguard>=2.13.3,<5.0.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
