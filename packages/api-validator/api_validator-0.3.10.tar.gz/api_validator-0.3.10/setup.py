"""Setup script"""
import setuptools
import os
import re

HERE = os.path.abspath(os.path.dirname(__file__))
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
TESTS_REQUIRE = ["coverage", "pytest"]


def get_version():
    init = open(os.path.join(HERE, "api_validator", "version.py")).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setuptools.setup(
    name="api-validator",
    include_package_data=True,
    version=get_version(),
    author="Kinnaird McQuade",
    author_email="kinnaird@nightvision.net",
    description="Validate OpenAPI specs by sending traffic",
    package_data={
        "api_validator": [
            "diff_utils/config.yml",
            "diff_utils/job_summary.md.j2",
            "tools/newman_summary.md.j2",
        ]
    },
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/nvsecurity/api-validator",
    packages=setuptools.find_packages(exclude=["test*"]),
    tests_require=TESTS_REQUIRE,
    install_requires=[
        "click",
        "click-option-group",
        "invoke",
        "loguru",
        "PyYAML",
        "Jinja2",
        "pandas",
        "requests"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": "api-validator=api_validator.bin.cli:main"},
    zip_safe=True,
    keywords="openapi",
    python_requires=">=3.11",
)
