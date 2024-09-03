from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name="bc_pulse_krT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    ext_modules=cythonize(
        [
            "src/bc_pulse/**/*.py",  # bc_pulse 내 모든 .py 파일을 컴파일
        ],
        compiler_directives={'language_level': "3"}  # Python 3.x
    ),
    entry_points={
        "console_scripts": [
            "bc_pulse=bc_pulse.__main__:main",
        ],
    },
    include_package_data=True,
)
