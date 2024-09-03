from setuptools import setup, find_packages

setup(
    name="bc_pulse_krT",
    # version="3.0.0b14",  # 필요하다면 버전을 명시적으로 추가하세요/
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "bc_pulse=bc_pulse.__main__:main",
        ],
    },
    include_package_data=True,
)
