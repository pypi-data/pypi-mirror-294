from setuptools import setup, find_packages
import os

# Define the current working directory
cwd = os.path.abspath(os.path.dirname(__file__))

setup(
    name="crystalpy_barno",
    version="1.0.13",
    description="Python integration with crystal report",
    long_description=open(os.path.join(cwd, "README.md")).read(),
    long_description_content_type="text/markdown",
    author="barno1994",
    author_email="barno.baptu@gmail.com",
    maintainer="barno.baptu",
    maintainer_email="barno.baptu@gmail.com",
    url="https://github.com/barno1994/RPT_PY",
    project_urls={
        "Homepage": "https://github.com/barno1994/RPT_PY",
        "Issues": "https://github.com/barno1994/RPT_PY/issues",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["crystal report", "python integration"],
    python_requires=">=3.6",
    license="MIT",
    packages=find_packages(where=os.path.join(cwd, 'src')),  # Find packages in the src directory
    package_dir={'crystalpy_barno': os.path.join(cwd, 'src')},  # Tell setuptools where the crystalpy_barno package is
    package_data={
        'crystalpy_barno': [
            'ReportsClasses/CR/*.py', 
            'ReportsClasses/Helper/*.py', 
            'ReportsClasses/Sales/*.py', 
            'ReportsClasses/Stock/*.py', 
            'rpt/*.rpt'
        ],
    },
    include_package_data=True,
    install_requires=[],  # Add required dependencies here if any
    extras_require={
        "dev": [
            "cffi==1.17.0",
            "clr-loader==0.2.6",
            "pycparser==2.22",
            "pythonnet==3.0.3",
        ],
    },
)
