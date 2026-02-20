import argparse
import os
import subprocess
import sys
import threading
import traceback
from pathlib import Path
from typing import Any, Optional

from constants import CONFIG_FILE
from exceptions import (
    EC_ARG_GENERAL,
    MESSAGE_ARG_GENERAL,
    ArgumentInputMissingException,
    ArgumentInputPdfException,
    ArgumentInputPdfOutputHtmlException,
    ArgumentInputPdfOutputXmlException,
    ExpectedException,
    ValidationFailed,
)
from image_update import DockerImageContainerUpdateChecker


def set_arguments(
    parser: argparse.ArgumentParser,
    names: list,
    output_help: str = "",
) -> None:
    """
    Set arguments for the parser based on the provided names and options.

    Args:
        parser (argparse.ArgumentParser): The argument parser to set arguments for.
        names (list): List of argument names to set.
        output_help (str): Help shown for output argument. Defaults to "".
    """
    for name in names:
        match name:
            case "flavour":
                parser.add_argument("--flavour", type=str, default="ua1", help="Validation Profile flavour")
            case "format":
                parser.add_argument(
                    "--format",
                    type=str,
                    default="xml",
                    choices=["raw", "xml", "html", "text", "json"],
                    help="Format of output",
                )
            case "input":
                parser.add_argument("--input", "-i", type=str, required=True, help="The input PDF file")
            case "maxfailures":
                parser.add_argument("--maxfailures", type=int, default=-1, help="Maximum amount of failed checks")
            case "maxfailuresdisplayed":
                parser.add_argument(
                    "--maxfailuresdisplayed",
                    type=int,
                    default=-1,
                    help="Maximum amount of failed checks displayed for each rule",
                )
            case "output":
                parser.add_argument("--output", "-o", type=str, help=output_help)
            case "pass":
                parser.add_argument(
                    "--pass",
                    dest="pass_flag",
                    nargs="?",
                    const=True,
                    type=bool,
                    default=False,
                    help="Shows successful validation checks",
                )
            case "profile":
                parser.add_argument("--profile", type=str, help="Path to the validation profile")


def str2bool(value: Any) -> bool:
    """
    Helper function to convert argument to boolean.

    Args:
        value (Any): The value to convert to boolean.

    Returns:
        Parsed argument as boolean.
    """
    if isinstance(value, bool):
        return value
    if value.lower() in ("yes", "true", "t", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "0"):
        return False
    else:
        return False


def run_config_subcommand(args) -> None:
    get_pdfix_config(args.output)


def get_pdfix_config(path: str) -> None:
    """
    If Path is not provided, output content of config.
    If Path is provided, copy config to destination path.

    Args:
        path (string): Destination path for config.json file
    """
    config_path: Path = Path(__file__).parent.parent.joinpath(CONFIG_FILE)

    with open(config_path, "r", encoding="utf-8") as file:
        if path is None:
            print(file.read())
        else:
            with open(path, "w") as out:
                out.write(file.read())


def run_validation_subcommand(args) -> None:
    input_file: str = args.input

    if not os.path.isfile(input_file):
        raise ArgumentInputMissingException()

    if not input_file.lower().endswith(".pdf"):
        raise ArgumentInputPdfException()

    output_file: Optional[str] = args.output
    flavour: Optional[str] = args.flavour
    format: str = args.format
    maxfailures: int = args.maxfailures
    maxfailuresdisplayed: int = args.maxfailuresdisplayed
    pass_flag: bool = args.pass_flag
    profile: Optional[str] = args.profile

    if format == "xml" and (output_file is None or not output_file.lower().endswith(".xml")):
        raise ArgumentInputPdfOutputXmlException()

    if format == "html" and (output_file is None or not output_file.lower().endswith(".html")):
        raise ArgumentInputPdfOutputHtmlException()

    returncode: int = run_validation(
        input_file, output_file, flavour, format, maxfailures, maxfailuresdisplayed, pass_flag, profile
    )
    sys.exit(returncode)


def run_validation(
    input_file: str,
    output_file: Optional[str],
    flavour: Optional[str],
    format: str,
    maxfailures: int,
    maxfailuresdisplayed: int,
    pass_flag: bool,
    profile: Optional[str],
) -> int:
    """
    Runs validation using veraPDF java program in subprocess.

    Args:
        input_file (str): Path to input PDF file.
        output_file (Optional[str]): Either path to output file or None when output goes to standart output.
        flavour (Optional[str]): Optional flavour name.
        format (str): Format of output like json, xml, ...
        maxfailures (int): Maximum amount of failed checks.
        maxfailuresdisplayed (int): Maximum amount of failed checks displayed for each rule.
        pass_flag (bool): Successful checks will be displayed in output.
        profile (Optional[str]): Optional path to validation profile.

    Return:
        Return code of validation process.
    """
    try:
        java_program_path: str = (
            Path(__file__).parent.parent.joinpath("res/greenfield-apps-1.27.0-SNAPSHOT.jar").as_posix()
        )
        command: list[str] = [
            "java",
            "-jar",
            java_program_path,
            "--maxfailures",
            str(maxfailures),
            "--maxfailuresdisplayed",
            str(maxfailuresdisplayed),
            "--format",
            format,
        ]
        if profile:
            command.append("--profile")
            command.append(profile)
        if flavour:
            command.append("--flavour")
            command.append(flavour)
        if pass_flag:
            command.append("--pass")

        command_to_run: str = " ".join(command)
        command_to_run += f' "{input_file}"'

        returncode, stdout, stderr = run_subprocess(command_to_run)

        if output_file:
            with open(output_file, "w+", encoding="utf-8") as out:
                out.write(stdout)
        else:
            print(stdout)

        if stderr:
            print(stderr, file=sys.stderr)

        # 0,1 are valid return codes (0 - no validation errors in document, 1 - there are validation errors in document)
        if returncode > 1:
            raise ValidationFailed()

        return returncode

    except Exception:
        raise ValidationFailed()


def run_subprocess(command: str) -> tuple[int, str, str]:
    """
    Execute a shell command and capture its output and return code.

    This function runs the validation as shell command using the `subprocess.Popen`
    method, captures the standard output (stdout), standard error (stderr),
    and the return code of the process.

    Args:
        command (str): The shell command to execute.

    Returns:
        A tuple containing:
            - returncode (int): The return code of the command.
            - stdout (str): The standard output of the command.
            - stderr (str): The standard error of the command.

    """
    process: subprocess.Popen = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        text=True,
    )
    stdout, stderr = process.communicate()

    return process.returncode, stdout, stderr


def main():
    parser = argparse.ArgumentParser(
        description="Validate a PDF file",
    )

    subparsers = parser.add_subparsers(dest="subparser")

    # Config subcommand
    config_subparser = subparsers.add_parser(
        "config",
        help="Extract config file for integration",
    )
    set_arguments(
        config_subparser,
        ["output"],
        "Output to save the config JSON file. Application output is used if not provided.",
    )
    config_subparser.set_defaults(func=run_config_subcommand)

    # Validate subcommand
    validate_subparser = subparsers.add_parser(
        "validate",
        help="Run validation of PDF document",
    )
    set_arguments(
        validate_subparser,
        ["input", "output", "flavour", "format", "maxfailures", "maxfailuresdisplayed", "pass", "profile"],
        "The output validation file",
    )
    validate_subparser.set_defaults(func=run_validation_subcommand)

    # Parse arguments
    try:
        args = parser.parse_args()
    except ExpectedException as e:
        print(e.message, file=sys.stderr)
        sys.exit(e.error_code)
    except SystemExit as e:
        if e.code != 0:
            print(MESSAGE_ARG_GENERAL, file=sys.stderr)
            sys.exit(EC_ARG_GENERAL)
        # This happens when --help is used, exit gracefully
        sys.exit(0)
    except Exception as e:
        print(traceback.format_exc(), file=sys.stderr)
        print(f"Failed to run the program: {e}", file=sys.stderr)
        sys.exit(2)

    if hasattr(args, "func"):
        # Check for updates only when help is not checked
        update_checker = DockerImageContainerUpdateChecker()
        # Check it in separate thread not to be delayed when there is slow or no internet connection
        update_thread = threading.Thread(target=update_checker.check_for_image_updates)
        update_thread.start()

        # Run subcommand
        try:
            args.func(args)
        except ExpectedException as e:
            print(e.message, file=sys.stderr)
            sys.exit(e.error_code)
        except Exception as e:
            print(traceback.format_exc(), file=sys.stderr)
            print(f"Failed to run the program: {e}", file=sys.stderr)
            sys.exit(2)
        finally:
            # Make sure to let update thread finish before exiting
            update_thread.join()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
