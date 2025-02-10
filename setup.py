from setuptools import setup, find_packages

setup(
    name="rcache_live",
    version="0.1.1",
    description="A simple and efficient Redis caching library with Active TTL support",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/redis-cache-lib",
    packages=find_packages(exclude=["tests"]),  # Exclude tests from packaging
    install_requires=[
        "redis>=4.0.0"
    ],
    extras_require={
        "dev": ["pytest", "mockredispy"]  # Dev dependencies for testing
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT",
    include_package_data=True,
)
