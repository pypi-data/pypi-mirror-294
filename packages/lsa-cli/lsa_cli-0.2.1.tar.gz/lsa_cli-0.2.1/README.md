# LSA (Linking Software Artifacts) CLI

[![Version](https://img.shields.io/pypi/v/lsa-cli?logo=pypi)](https://pypi.org/project/lsa-cli)
[![Python Version](https://img.shields.io/pypi/pyversions/lsa-cli?logo=python&logoColor=white)](https://pypi.org/project/lsa-cli)

A part of [LSA](https://github.com/MarkSeliverstov/MFF-bachelor-work) project,
this CLI tool is used to parse `annotations` from source code and convert them
to `entities`. Entities are then used to visualize the codebase on the
[webpage](https://markseliverstov.github.io/MFF-bachelor-work).

## Installation

```bash
pip install lsa-cli
```

## Usage

```bash
lsa-cli <path-to-source-code>
```

**Options:**

```bash
-a, --annotations  Save intermediate annotations model as JSON
-c, --config       Path to the configuration file
```

## Configuration file

Default configuration file is `.lsa-config.json` in the current working directory.
You can specify the path to the configuration file using the `-c` option.

```bash
lsa-cli -c <path-to-config-file> <path-to-source-code>
```

If the file is not found, default configuration is used:

```json
{
  "markers": {
    "prefix": "@lc-",
    "identifier": "identifier",
    "name": "name",
    "type": "type",
    "description": "description",
    "entity": "entity",
    "property": "property",
    "method": "method",
    "source": "source"
  },
  "output": {
    "entities": "entities.json",
    "annotations": "annotations.json"
  },
  "parser": {
    "exclude": [],
    "extend": {}
  },
}
```

#### markers

In the `markers` section you can specify the names of the fields that are used
in the annotations.

#### output

In the `output` section you can specify the names of the files where the
entities and annotations will be saved.

#### parser

In the `parser` section you can specify the file extensions that should be
parsed and the files that should be excluded from the parsing.

**Example:**

```bash
...
"parser": {
  "exclude": ["node_modules"],
  "extend": {
    "cjs": "application/javascript",
    "mjs": "application/javascript",
    "jsx": "application/javascript"
  }
}
...
```

## Development

<details>

### Installation

```bash
poetry install
```

### Usage

```bash
poetry run lsa-cli
```

### Testing

```bash
pytest -c pyproject.toml
```

### Formatting

```bash
poetry run poe format-code
```

### Pre-commit

```bash
poetry shell
pre-commit install
```

</details>
