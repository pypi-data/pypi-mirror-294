from setuptools import setup, find_packages

setup(
    name="switch-java-version",
    version="0.1.0",
    description="A script to switch between Java versions on Windows",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Gamertoky1188",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/switch-java",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'switch-java=switch_java.main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)
