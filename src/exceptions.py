EC_ARG_GENERAL = 10
EC_ARG_INPUT_MISSING = 11
EC_ARG_INPUT_PDF = 12
EC_ARG_INPUT_PDF_OUTPUT_XML = 13
EC_ARG_INPUT_PDF_OUTPUT_HTML = 14

EC_VALIDATION_FAILED = 30

MESSAGE_ARG_GENERAL = "Failed to parse arguments. Please check the usage and try again."
MESSAGE_ARG_INPUT_MISSING = "Input file does not exists."
MESSAGE_ARG_INPUT_PDF = "Input file must be PDF document."
MESSAGE_ARG_INPUT_PDF_OUTPUT_XML = "Input file must be PDF document and output file must be XML."
MESSAGE_ARG_INPUT_PDF_OUTPUT_HTML = "Input file must be PDF document and output file must be HTML."

MESSAGE_VALIDATION_FAILED = "Validation failed."


class ExpectedException(BaseException):
    def __init__(self, error_code: int) -> None:
        self.error_code: int = error_code
        self.message: str = ""

    def _add_note(self, note: str) -> None:
        self.message = note


class ArgumentException(ExpectedException):
    def __init__(self, message: str = MESSAGE_ARG_GENERAL, error_code: int = EC_ARG_GENERAL) -> None:
        super().__init__(error_code)
        self._add_note(message)


class ArgumentInputMissingException(ArgumentException):
    def __init__(self) -> None:
        super().__init__(MESSAGE_ARG_INPUT_MISSING, EC_ARG_INPUT_MISSING)


class ArgumentInputPdfException(ArgumentException):
    def __init__(self) -> None:
        super().__init__(MESSAGE_ARG_INPUT_PDF, EC_ARG_INPUT_PDF)


class ArgumentInputPdfOutputXmlException(ArgumentException):
    def __init__(self) -> None:
        super().__init__(MESSAGE_ARG_INPUT_PDF_OUTPUT_XML, EC_ARG_INPUT_PDF_OUTPUT_XML)


class ArgumentInputPdfOutputHtmlException(ArgumentException):
    def __init__(self) -> None:
        super().__init__(MESSAGE_ARG_INPUT_PDF_OUTPUT_HTML, EC_ARG_INPUT_PDF_OUTPUT_HTML)


class ValidationFailed(ExpectedException):
    def __init__(self) -> None:
        super().__init__(EC_VALIDATION_FAILED)
        self._add_note(MESSAGE_VALIDATION_FAILED)
