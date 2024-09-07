from setuptools import setup, find_packages

setup(
    name="Kannadafy",                # The name of your PyPI package
    version="0.1.0",                 # Version of your package
    author="MithunGowda.B",
    author_email="mithungowda.b7411@gmail.com",
    description="A tool to obfuscate Python scripts using Kannada letters",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # This indicates README.md is markdown
    url="https://github.com/mithun50/Kannadafy",    # URL to your project's repository
    packages=find_packages(),        # Automatically find the `Kannadafy` package
    entry_points={
    'console_scripts': [
        'kannadafy = Kannadafy.kannadafy:main',  # Create CLI tool `kannadafy`
    ],
},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",         # Minimum Python version required
)