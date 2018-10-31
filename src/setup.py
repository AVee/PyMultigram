import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyMultigram",
    version="0.0.1",
    author="AVee",
    author_email="pymultigram@avee.org",
    description="Framework for multi-client Pyrogram programs with flexible plugin support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AVee/PyMultigram",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
    ],
    keywords='telegram pyrogram',
    install_requires=['pyrogram>=0.8']
)