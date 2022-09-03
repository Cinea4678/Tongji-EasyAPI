from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="easyTongjiapi",
    version="0.1.0a1",
    description="Easy Tongji 1-System API for everyone.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cinea4678/Tongji-EasyAPI",
    author="Cinea Zhan",
    author_email="cinea@cinea.com.cn",
    license="GPL v3.0",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Natural Language :: Chinese (Simplified)"
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=["requests","beautifulsoup4","lxml","fastgm",
    "opencv-python","pycryptodome","pillow","numpy"],
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/Cinea4678/Tongji-EasyAPI/issues",
        "Visit My Homepage": "https://www.cinea.com.cn",
        "Source": "https://github.com/Cinea4678/Tongji-EasyAPI",
    },
)