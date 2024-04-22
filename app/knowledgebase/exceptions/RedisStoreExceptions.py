class DocumentNotFoundException(Exception):
    """Exception raised when a document cannot be found."""

    def __init__(self, document_id, message="Document not found"):
        self.document_id = document_id
        self.message = message
        super().__init__(f"{message}: ID {document_id}")