import setuptools

setuptools.setup(
    author="George",
    author_email="georgelombardi97@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    include_package_data=True,
    install_requires=["httpx", "pynacl"],
    name="sui_python_sdk",
    packages=["sui_python_sdk"],
    python_requires=">=3.7",
    version="0.1.0",
)