import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ok-script",
    version="0.0.186",
    author="ok-oldking",
    author_email="firedcto@gmail.com",
    description="Automation with Computer Vision for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ok-oldking/ok-script",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    install_requires=[
        'pywin32>=306',
        'typing-extensions>=4.11.0',
        'PySide6>=6.7.0',
        'PySide6-Fluent-Widgets>=1.5.6'
    ],
    python_requires='>=3.6',
)
