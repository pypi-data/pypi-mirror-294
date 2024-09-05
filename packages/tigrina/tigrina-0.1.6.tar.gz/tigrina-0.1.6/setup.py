from setuptools import setup, find_packages
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setup(
    name='tigrina',
    version='0.1.6',
    author='Gide Segid',
    author_email='gidesegid@gmail.com',
    packages=find_packages(),
    description="Tigrina alphabet manipulator, which helps to write Tigrina by Tigrina alphabets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        'tigrina': ['data/*'],
        'tigrina': ['tigrina/data/*'],
    },
    install_requires=[
        "pandas"
    ],
    entry_points={
        'console_scripts': [
            'tigrina_words=tigrina.Tigrinya_alphabet_coder_decoder:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    license="MIT",
    python_requires='>=3.6'
)
