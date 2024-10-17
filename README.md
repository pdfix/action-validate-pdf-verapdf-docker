# PDF Validation Docker App using VeraPDF

This Docker application is designed to validate PDF files for compliance with the PDF/A standard using VeraPDF. It allows users to easily perform PDF validation with customizable options and can be executed via command-line arguments.

## Table of Contents

- [PDF Validation Docker App using VeraPDF](#pdf-validation-docker-app-using-verapdf)
  - [Getting Started](#getting-started)
  - [Run using Command Line Interface](#run-using-command-line-interface)
  - [Validation Settings and Configuration](#validation-settings-and-configuration)
    - [Exporting Configuration for Integration](#exporting-configuration-for-integration)
  - [License](#license)
  - [Help & Support](#help--support)

## Getting Started

To use this Docker application, you will need to have Docker installed on your system. If Docker is not installed, please follow the instructions on the [official Docker website](https://docs.docker.com/get-docker/) to install it.

## Run using Command Line Interface

To run the Docker container as a CLI, you need to share the folder with the PDF files you wish to validate using the `-i` parameter. In this example, the current folder is used.

First run will pull the docker image, which may take some time. Make your own image for more advanced use.

```
docker run -v $(pwd):/data --rm pdfix/validation:latest validation -i input.pdf
 
```

For more detailed information about the available command-line arguments, you can run the following command:

```bash
docker run --rm pdfix/validation:latest --help
```

## Run OCR using REST API
Comming soon. Please contact us.

### Exporting Configuration for Integration
To export the configuration JSON file, use the following command:
```bash
docker run -v $(pwd):/data --rm pdfix/validation:latest config -o config.json
```

## License
TBD...

## Help & Support
To obtain a PDFix SDK license or report an issue please contact us at support@pdfix.net.
For more information visit https://pdfix.net

