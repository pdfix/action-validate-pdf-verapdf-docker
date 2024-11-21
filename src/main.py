import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def get_config(path: str) -> None:
    if path is None:
        with open(
            os.path.join(Path(__file__).parent.absolute(), "../config.json"),
            "r",
            encoding="utf-8",
        ) as f:
            print(f.read())
    else:
        src = os.path.join(Path(__file__).parent.absolute(), "../config.json")
        dst = path
        shutil.copyfile(src, dst)


def run_validation(command: list) -> tuple:
    """Execute a shell command and capture its output and return code.

    This function runs the validation as shell command using the `subprocess.Popen`
    method, captures the standard output (stdout), standard error (stderr),
    and the return code of the process.

    Args:
    ----
        command (str): The shell command to execute.

    Returns:
    -------
        tuple: A tuple containing:
            - stdout (str): The standard output of the command.
            - stderr (str): The standard error of the command.
            - return_code (int): The return code of the command
              (0 indicates success, non-zero indicates failure).

    """
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )

    stdout, stderr = process.communicate()

    return_code = process.returncode

    return stdout, stderr, return_code


def main():
    parser = argparse.ArgumentParser(
        description="Process a PDF or image file with Tesseract OCR",
    )

    subparsers = parser.add_subparsers(dest="subparser")

    # config subparser
    pars_config = subparsers.add_parser(
        "config",
        help="Extract config file for integration",
    )
    pars_config.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output to save the config JSON file. Application output\
              is used if not provided",
    )

    pars_validate = subparsers.add_parser(
        "validate",
        help="Run alternate text description",
    )

    pars_validate.add_argument("-i", "--input", type=str, help="The input PDF file")
    pars_validate.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output validation file",
    )
    pars_validate.add_argument(
        "--profile",
        type=str,
        help="Path to the validation profile",
    )
    pars_validate.add_argument(
        "--flavour",
        type=str,
        help="Flavour name",
    )

    pars_validate.add_argument(
        "--maxfailuresdisplayed",
        type=int,
        default=-1,
        help="Max failures displayed",
    )

    pars_validate.add_argument(
        "--format",
        type=str,
        default="xml",
        choices=["raw", "xml", "html", "text", "json"],
    )

    try:
        args = parser.parse_args()
    except SystemExit as e:
        if e.code == 0:  # This happens when --help is used, exit gracefully
            sys.exit(0)
        print("Failed to parse arguments. Please check the usage and try again.")
        sys.exit(1)

    if args.subparser == "config":
        get_config(args.output)
        sys.exit(0)

    elif args.subparser == "validate":
        if not args.input:
            pars_validate.error("The following arguments are required: -i/--input")

        input_file = args.input
        output_file = args.output

        if not os.path.isfile(input_file):
            sys.exit(f"Error: The input file '{input_file}' does not exist.")
            return

        if input_file.lower().endswith(".pdf"):
            try:
                command = [
                    "java",
                    "-jar",
                    os.path.join(
                        Path(__file__).parent.absolute(),
                        "../res/greenfield-apps-1.27.0-SNAPSHOT.jar",
                    ),
                    "--maxfailuresdisplayed",
                    str(args.maxfailuresdisplayed),
                    "--format",
                    args.format,
                ]
                if args.profile:
                    command.append("--profile")
                    command.append(args.profile)
                if args.flavour:
                    command.append("--flavour")
                    command.append(args.flavour)

                command.append(args.input)

                stdout, stderr, return_code = run_validation(" ".join(command))

                if output_file:
                    with open(args.output, "w+", encoding="utf-8") as out:
                        out.write(stdout)

                else:
                    print(stdout)

                if stderr:
                    print(stderr, file=sys.stderr)

            except Exception as e:
                sys.exit("Failed to run validation: {}".format(e))

        else:
            print("Input file must be PDF")


if __name__ == "__main__":
    main()
