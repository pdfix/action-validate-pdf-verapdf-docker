EC_VERAPDF_ARG: int = 2
EC_VERAPDF_MEMORY: int = 3
EC_VERAPDF_NO_FILES: int = 4
EC_VERAPDF_IO_EXCEPTION: int = 6
EC_VERAPDF_FAILED_TO_PARSE_FILES: int = 7
EC_VERAPDF_ENCRYPTED_PDFS: int = 8
EC_VERAPDF_VERAPDF_EXCEPTION: int = 9
EC_VERAPDF_JAVA_XML_MARSHALLING_EXCEPTION: int = 10
EC_VERAPDF_VALIDATION_STOPPED: int = 12

EC_ARG_GENERAL: int = 15
EC_ARG_INPUT_MISSING: int = 16
EC_ARG_INPUT_PDF: int = 17
EC_ARG_INPUT_PDF_OUTPUT_XML: int = 18
EC_ARG_INPUT_PDF_OUTPUT_HTML: int = 19

EC_VALIDATION_FAILED: int = 30

MESSAGE_VERAPDF_ARG: str = "Invalid command line parameters."
MESSAGE_VERAPDF_MEMORY: str = "Your system does not have enough available memory to validate the PDF."
MESSAGE_VERAPDF_NO_FILES: str = "The PDF could not be found or opened."
MESSAGE_VERAPDF_IO_EXCEPTION: str = (
    "Could not read or write the file. Check permissions, file security settings or location, and disk space."
)
MESSAGE_VERAPDF_FAILED_TO_PARSE_FILES: str = "The PDF appears damaged or invalid and could not be read."
MESSAGE_VERAPDF_ENCRYPTED_PDFS: str = "The PDF is encrypted. Unlock it or save an unprotected copy first."
MESSAGE_VERAPDF_VERAPDF_EXCEPTION: str = "Validation stopped due to an unexpected error. Try again or contact support."
MESSAGE_VERAPDF_JAVA_XML_MARSHALLING_EXCEPTION: str = (
    "Validation ran, but the report could not be generated. Try again or contact support."
)
MESSAGE_VERAPDF_VALIDATION_STOPPED: str = "Validation was cancelled or interrupted. Try again or contact support."

MESSAGE_ARG_GENERAL: str = "Failed to parse arguments. Please check the usage and try again."
MESSAGE_ARG_INPUT_MISSING: str = "Input file does not exists."
MESSAGE_ARG_INPUT_PDF: str = "Input file must be PDF document."
MESSAGE_ARG_INPUT_PDF_OUTPUT_XML: str = "Input file must be PDF document and output file must be XML."
MESSAGE_ARG_INPUT_PDF_OUTPUT_HTML: str = "Input file must be PDF document and output file must be HTML."

MESSAGE_VALIDATION_FAILED: str = "Validation failed."

EC_VERAPDF: dict[int, str] = {
    EC_VERAPDF_ARG: MESSAGE_VERAPDF_ARG,
    EC_VERAPDF_MEMORY: MESSAGE_VERAPDF_MEMORY,
    EC_VERAPDF_NO_FILES: MESSAGE_VERAPDF_NO_FILES,
    EC_VERAPDF_IO_EXCEPTION: MESSAGE_VERAPDF_IO_EXCEPTION,
    EC_VERAPDF_FAILED_TO_PARSE_FILES: MESSAGE_VERAPDF_FAILED_TO_PARSE_FILES,
    EC_VERAPDF_ENCRYPTED_PDFS: MESSAGE_VERAPDF_ENCRYPTED_PDFS,
    EC_VERAPDF_VERAPDF_EXCEPTION: MESSAGE_VERAPDF_VERAPDF_EXCEPTION,
    EC_VERAPDF_JAVA_XML_MARSHALLING_EXCEPTION: MESSAGE_VERAPDF_JAVA_XML_MARSHALLING_EXCEPTION,
    EC_VERAPDF_VALIDATION_STOPPED: MESSAGE_VERAPDF_VALIDATION_STOPPED,
}


class ExpectedException(BaseException):
    def __init__(self, error_code: int) -> None:
        self.error_code: int = error_code
        self.message: str = ""

    def _add_note(self, note: str) -> None:
        self.message = note


class VeraPDFException(ExpectedException):
    def __init__(self, error_code: int) -> None:
        super().__init__(error_code)
        self.message = EC_VERAPDF[error_code]


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
