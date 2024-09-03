from setuptools import setup, find_packages

setup(
    name="bc_pulse_krT",
    version="3.0.0b36",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aenum",
        "colored==1.4.4",
        "pyjwt",
        "requests",
        "pyyaml",
        "beautifulsoup4",
        "colorama"
    ],
)
