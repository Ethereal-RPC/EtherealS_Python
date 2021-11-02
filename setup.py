import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="com-ethereal-server",
    version="0.0.2",
    author="BaiYang",
    author_email="839336369@qq.com",
    description="Ethereal PythonServer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ethereal-RPC/EtherealS_Python",
    project_urls={
        "Bug Tracker": "https://github.com/Ethereal-RPC/EtherealS_Python",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)