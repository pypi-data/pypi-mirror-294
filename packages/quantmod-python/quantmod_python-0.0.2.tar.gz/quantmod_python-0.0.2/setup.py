# Quantmod Python Package
# https://kannansingaravelu.com/

import pathlib
from setuptools import setup, find_packages
import versioneer

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text(encoding="utf-8")

with open('requirements.txt', 'r', encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="quantmod-python",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Quantmod Python Package",
    long_description=README,
    long_description_content_type="text/markdown", 
    url="https://kannansingaravelu.com/",
    author="Kannan Singaravelu",
    author_email="inquant@outlook.com",
    packages=find_packages(),
    install_requires=requirements,
    keywords=["python", "quant", "quantmod", "quantmod-python"],
    license="Apache License 2.0",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",  
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.9",
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'inquant=quantmod:hello',
        ],
    },
)