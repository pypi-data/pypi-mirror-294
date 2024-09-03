from setuptools import setup, find_packages

setup(
    name="bc_pulse_krT",
    version="3.0.0b35",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "bc_pulse=bc_pulse.__main__:main",
        ],
    },
)
