## Development setup

In a Python ≥ 3.8 virtual environment, run:

    pip install -e .[test]

These linters should be installed with the system package manager or `pipx`:

- black
- flake8
- isort (might be packaged as: python3-isort)
- reuse

To run all the tests and linters, run:

    make check


### Cutting a new release

1.  Assign a new version number,
    creating a version bump commit with an annotated tag:

    ```
    contrib/new-release 0.1.2
    ```

2.  Push the new version upstream:

    ```
    git push --follow-tags
    ```

3.  Compile the package into a wheel and upload it to the forge:

    ```
    make upload
    ```

4.  Publish the source dist and wheel to PyPI:

    ```
    make publish
    ```
