from setuptools import setup, find_packages

setup(
    name="dbtimer",
    version="0.1.0",
    description="A Django management command to measure and benchmark database query performance.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Django Web Studio",
    author_email="devs@djangowebstudio.com",
    url="https://bitbucket.org/dpater/dbtimer",
    license="GNU",
    packages=[
        "dbtimer",
        "dbtimer.management",
        "dbtimer.management.commands",
        "dbtimer.mixins",
        "dbtimer.migrations",
        "dbtimer.templates",
    ],
    include_package_data=True,
    install_requires=[
        "django>=3.2,<5.0",
        "tqdm>=4.64.0",
        "boto3>=1.18.0",
        "matplotlib>=3.4.0",
        "requests>=2.26.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires='>=3.7',
)
