from setuptools import setup

name = "types-Jetson.GPIO"
description = "Typing stubs for Jetson.GPIO"
long_description = '''
## Typing stubs for Jetson.GPIO

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`Jetson.GPIO`](https://github.com/NVIDIA/jetson-gpio) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`Jetson.GPIO`.

This version of `types-Jetson.GPIO` aims to provide accurate annotations
for `Jetson.GPIO==2.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/Jetson.GPIO. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit
[`4101e742366e5e1f79168fba8d97503b047dfd5b`](https://github.com/python/typeshed/commit/4101e742366e5e1f79168fba8d97503b047dfd5b) and was tested
with mypy 1.11.1, pyright 1.1.378, and
pytype 2024.4.11.
'''.lstrip()

setup(name=name,
      version="2.1.0.20240903",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/Jetson.GPIO.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['Jetson-stubs'],
      package_data={'Jetson-stubs': ['GPIO/__init__.pyi', 'GPIO/gpio.pyi', 'GPIO/gpio_cdev.pyi', 'GPIO/gpio_event.pyi', 'GPIO/gpio_pin_data.pyi', '__init__.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
