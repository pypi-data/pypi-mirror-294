import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="NLIF",
    version="0.0.5",
    author="marmot8080",
    author_email="marmot8080@gmail.com",
    description="using natural language as condition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marmot8080/NLIF",
    project_urls={
        "Bug Tracker": "https://github.com/marmot8080/NLIF/issues",
    },
    install_requires=[
        "openai"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
)