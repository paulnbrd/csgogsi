import setuptools
import csgogsi

print("CSGOGSI Installation")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csgogsi", # Replace with your own username
    version=csgogsi.__version__,
    author=csgogsi.__author__,
    author_email="python-project@paulinux.fr",
    description="Counter-Strike: Global Offensive Game State Integration in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paulnbrd/csgogsi",
    project_urls={
        "Bug Tracker": "https://github.com/paulnbrd/csgogsi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)
