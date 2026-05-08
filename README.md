# veraPDF Validation

This Docker image includes veraPDF software that validates PDF/A and PDF/UA parts and conformance levels. Users can define further checks to enforce institutional policy.

## Table of Contents

- [veraPDF Validation](#verapdf-validation)
  - [Getting started](#getting-started)
  - [Usage](#usage)
  - [Commands](#commands)
  - [Arguments](#arguments)
  - [Examples](#examples)
  - [Help \& support](#help--support)
  - [Licenses](#licenses)

## Getting started

You need Docker installed. The first run downloads the image and may take longer than later runs.

## Usage

Mount a folder into the container and run a subcommand:

```bash
docker run --rm -v "$(pwd)":/data -w /data pdfix/validate-pdf-verapdf:latest <command> [options]
```

## Commands

- `validate`: Validate a PDF and write or print a report

## Arguments

### `validate`

| Option | Required | Type / expected value | Description |
|---|:---:|---|---|
| `--input`, `-i` | yes | Path to an existing `.pdf` file | Input PDF |
| `--output`, `-o` | no | Path for report file; omit to print to stdout | Output file |
| `--format` | no | One of: `raw`, `xml`, `html`, `text`, `json` (default: `xml`) | Report format |
| `--flavour` | no | String (default: `ua1`) | Validation profile flavour |
| `--profile` | no | Path to an existing validation profile file | Custom profile |
| `--maxfailures` | no | Integer (default **-1**) | Stop after this many failures |
| `--maxfailuresdisplayed` | no | Integer (default **-1**) | Max failures shown per rule |
| `--pass` | no | Flag; include passing checks when present | Show passed checks |

Notes:

- For `--format xml`, if `--output` is set it must end with `.xml`.
- For `--format html`, if `--output` is set it must end with `.html`.

## Examples

Validate and print XML to stdout:

```bash
docker run --rm -v "$(pwd)":/data -w /data pdfix/validate-pdf-verapdf:latest validate -i /data/input.pdf
```

Validate and write HTML:

```bash
docker run --rm -v "$(pwd)":/data -w /data pdfix/validate-pdf-verapdf:latest \
  validate -i /data/input.pdf -o /data/report.html --format html
```

## Help & support

To report an issue, contact `support@pdfix.net`.

## Licenses

- [veraPDF licensing](https://verapdf.org/home/#licensing)
