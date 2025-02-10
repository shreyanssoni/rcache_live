from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rcache-live",
    version="0.2.4",
    description="A simple and efficient Redis caching library with Active TTL support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Shreyans Soni",
    author_email="sonishreyans01@gmail.com",
    url="https://github.com/shreyanssoni/rcache_live",
    packages=find_packages(),
    install_requires=["redis>=4.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
     extras_require={
        "dev": ["pytest", "mockredispy"]
    },
    license="MIT",
    include_package_data=True,
    entry_points={
    'console_scripts': [
        'rcache-live-stats=rcache_live.cache_stats:get_cache_stats',
        ],
    },
)
