from setuptools import setup, find_packages

setup(
    name="alipay_zxw",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "pycryptodomex>=3.15.0",
        "pyOpenSSL>=22.0.0",
        "httpx>=0.20.0",
    ],
    author="薛伟的小工具",
    author_email="",
    description="支付宝支付SDK, 异步",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sunshineinwater/",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
