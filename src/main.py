import argparse
import os
import subprocess
import sys


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
    parser.add_argument("-i", "--input", type=str, help="The input PDF file")
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="The output validation file",
    )
    parser.add_argument(
        "--profile",
        type=str,
        help="Path to the validation profile",
    )

    parser.add_argument(
        "--maxfailuresdisplayed",
        type=int,
        default=-1,
        help="Max failures displayed",
    )

    parser.add_argument(
        "--format",
        type=str,
        default="xml",
        choices=["raw", "xml", "html", "text", "json"],
    )

    args = parser.parse_args()

    if not args.input:
        parser.error("The following arguments are required: -i/--input")

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
                "res/greenfield-apps-1.27.0-SNAPSHOT.jar",
                "--maxfailuresdisplayed",
                str(args.maxfailuresdisplayed),
                "--format",
                args.format,
            ]
            if args.profile:
                command.append("--profile")
                command.append(args.profile)

            command.append(args.input)

            stdout, stderr, return_code = run_validation(" ".join(command))

            if args.output:
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
