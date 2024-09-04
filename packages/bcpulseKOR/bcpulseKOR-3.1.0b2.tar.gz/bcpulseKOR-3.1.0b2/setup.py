from setuptools import setup, find_packages

setup(
    name="bcpulseKOR",
    version="3.1.0b2",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "bc_pulse=bc_pulse.__main__:main",
        ],
    },
    install_requires=[
        "aenum",
        "colored==1.4.4",
        "pyjwt",
        "requests",
        "pyyaml",
        "beautifulsoup4",
        "colorama",
    ],
)
