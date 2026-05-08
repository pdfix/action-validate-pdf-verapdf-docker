# veraPDF Validation

This Docker image includes the veraPDF software that validates all PDF/A and PDF/UA parts & conformance levels. Users can define further checks in order to enforce institutional policy.

## Table of Contents

- [Getting Started](#getting-started)
- [Run using Command Line Interface](#run-using-command-line-interface)
- [Command Line Arguments for Validation](#command-line-arguments-for-validation)
- [Exporting Configuration for Integration](#exporting-configuration-for-integration)
- [License](#license)
- [Help & Support](#help--support)

## Getting Started

To use this Docker application, you will need to have Docker installed on your system. If Docker is not installed, please follow the instructions on the [official Docker website](https://docs.docker.com/get-docker/) to install it.

## Run using Command Line Interface

To run the Docker container as a CLI, you need to share the folder with the PDF files you wish to validate using the `-v` parameter. In this example, the current folder is used.

The first run will pull the docker image, which may take some time. Make your own image for more advanced use.

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest validate -i <input>.pdf
```

Output as HTML

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest validate -i <input>.pdf -o index.html --format html
```

For more detailed information about the available command-line arguments, you can run the following command:

```bash
docker run --rm pdfix/validate-pdf-verapdf:latest --help
docker run --rm pdfix/validate-pdf-verapdf:latest validate --help
docker run --rm pdfix/validate-pdf-verapdf:latest config --help
```

## Command Line Arguments for Validation

This image exposes a small command-line interface (CLI) implemented by `main.py` inside the container.

### CLI shape (recommended pattern)

Use this mental model (and it scales well if you have many images, each with 1–3 subcommands):

```bash
docker run [docker options] <image> <command> [command options]
```

- **docker options**: container/runtime settings such as `--rm`, `-v`, `-w`
- **command**: a subcommand implemented by `main.py` (here: `validate`, `config`)
- **command options**: arguments for that specific subcommand

### `validate` command

Validates a PDF file using veraPDF and writes a report.

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest validate --input <input>.pdf
```

#### Options

| Option | Required | Value / Allowed values | Meaning |
|---|:---:|---|---|
| `--input`, `-i` | yes | path | Input PDF file to validate |
| `--output`, `-o` | no | path | Output report file. If omitted, the tool prints to stdout (recommended for CI logs). |
| `--format` | no | `raw` \| `xml` \| `html` \| `text` \| `json` | Output format |
| `--flavour` | no | string | Validation profile flavour (veraPDF profile selector) |
| `--profile` | no | path | Path to a validation profile file |
| `--maxfailures` | no | integer | Maximum number of failed checks before stopping |
| `--maxfailuresdisplayed` | no | integer | Maximum number of failed checks displayed per rule |
| `--pass` | no | `true` \| `false` | Whether to include successful validation checks in the output |

#### Examples

Output to HTML file:

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest validate -i <input>.pdf -o index.html --format html
```

Print JSON to stdout (easy to pipe into other tools):

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest validate -i <input>.pdf --format json
```

Include passing checks:

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest validate -i <input>.pdf --pass true
```

### Exporting Configuration for Integration

To export the configuration JSON file, use the following command:

```bash
docker run -v "$(pwd)":/data --rm -w /data/ pdfix/validate-pdf-verapdf:latest config -o config.json
```

## License

- veraPDF - `https://verapdf.org/home/#licensing`

## Help & Support

To obtain a PDFix SDK license or report an issue please contact us at support@pdfix.net.
For more information visit https://pdfix.net
