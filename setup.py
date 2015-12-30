from setuptools import setup

with open('README.rst') as f:
    desc = f.read()

setup(
    name = "spdx-lookup",
    version = "0.3.0",
    packages = ['spdx_lookup'],
    install_requires = ['spdx'],
    author = "Brendan Molloy",
    author_email = "brendan+pypi@bbqsrc.net",
    description = "SPDX license list query tool",
    license = "BSD-2-Clause",
    keywords = ["spdx", "licenses", "database", "lookup", "query"],
    url = "https://github.com/bbqsrc/spdx-lookup-python",
    long_description=desc,
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5"
    ],
    entry_points = {
        'console_scripts': [
            'spdx-lookup = spdx_lookup.__main__:main'
        ]
    }
)
