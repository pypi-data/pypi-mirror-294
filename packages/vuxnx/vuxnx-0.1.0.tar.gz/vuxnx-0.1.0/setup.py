from setuptools import setup, find_packages

setup(
    name="vuxnx",  # Tên package mà bạn muốn đăng lên PyPI
    version="0.1.0",  # Phiên bản hiện tại của package
    author="Vuxnx",  # Tên của bạn
    author_email="trongnghiavu649@gmail.com",  # Email của bạn
    description="A simple AI console package",  # Mô tả ngắn gọn về package
    long_description=open("README.md").read(),  # Nội dung đầy đủ từ file README
    long_description_content_type="text/markdown",  # Định dạng của README (thường là Markdown)
    packages=find_packages(),  # Tự động tìm và bao gồm tất cả các package con
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Yêu cầu phiên bản Python
)
