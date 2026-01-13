from setuptools import setup, find_packages

setup(
    name="skill-seekers",
    version="1.0.0",
    packages=find_packages(where="."),
    package_dir={"": "."},
    install_requires=[
        "mcp>=1.0.0",
        "fastmcp",
        "requests>=2.31.0",
        "beautifulsoup4>=4.12.0",
        "uvicorn",
        "httpx>=0.25.0",
    ],
    extras_require={
        "playwright": ["playwright>=1.40.0"],
        "all": ["playwright>=1.40.0"],
    },
    entry_points={
        'console_scripts': [
            'skill-seekers=skill_seekers.cli.main:main',
        ],
    },
    python_requires=">=3.10",
)
