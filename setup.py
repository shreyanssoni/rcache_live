from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rcache-live",
    version="0.2.2",
    description="A simple and efficient Redis caching library with Active TTL support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/rcache-live",
    packages=find_packages(),  # Automatically finds `rcache_live`
    install_requires=["redis>=4.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
     extras_require={
        "dev": ["pytest", "mockredispy"]  # Dev dependencies for testing
    },
    license="MIT",
    include_package_data=True,
)
