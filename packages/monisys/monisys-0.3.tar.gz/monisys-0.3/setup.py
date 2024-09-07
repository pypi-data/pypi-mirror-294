from setuptools import setup, find_packages
# for test fix
setup(
    name="monisys",
    version="0.3",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "monisys = monisys.monicli:main",
        ],
    },
    install_requires=[
        "rich",
    ],
    python_requires=">=3.6",
    author="Prasaanth Sakthivel",
    author_email="prasaanth@gmail.com",
    description="Monisys with tool we can able to moniter entire os",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/prasaanth2k/monisys",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
)
