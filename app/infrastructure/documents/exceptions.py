class InvalidDocumentTypeError(Exception):
    """Exception raised for invalid document types."""

    def __init__(self, document_type: str, valid_types: list[str]):
        self.document_type = document_type
        self.valid_types = valid_types
        super().__init__(f"Invalid document extension: {document_type}. Valid types are: {', '.join(valid_types)}")
