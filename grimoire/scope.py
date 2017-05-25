"""
Scope class definition
"""


class Scope(object):
    """Represents a scope in the context"""

    def __init__(self, database):
        """Construct an empty scope for the database."""
        self._database = database
        self._documents = []
        self._selected_documents = []
        self._tags = []
        self._selected_tags = []
        self._ordering = None

    def add_document(self, document):
        """Add a document to the scope."""
        pass

    def remove_document(self, document):
        """Remove the document from the scope."""
        pass

    def set_documents(self, documents):
        """Set the documents of the scope."""
        pass

    def select_document(self, document_id):
        """Add a document to the selection."""
        pass

    def deselect_document(self, document_id):
        """Remove the document from the given selection."""
        pass

    def deselect_all_documents(self):
        """Remove all documents from the selection."""
        pass

    def update_documents(self):
        """Update the documents according to the current tags."""
        pass

    def add_tag(self, tag):
        """Add a tag to the scope."""
        pass

    def remove_tag(self, tag):
        """Remove the tag from the scope."""
        pass

    def set_tags(self, tags):
        """Set the tags of the scope."""
        pass

    def update_tags(self):
        """Update the tags according to the selected documents."""
        pass

    def select_tag(self, tag_id):
        """Add a tag to the selection."""
        pass

    def deselect_tag(self, tag_id):
        """Remove the tag from the given selection."""
        pass

    def deselect_all_tags(self):
        """Remove all tags from the selection."""
        pass

    def find_selected_tags(self):
        """Find the selected tags of the scope."""
        pass

    def find_selected_documents(self):
        """Find the selected documents of the scope."""
        pass

    def find_suggested_tags(self, input):
        """Calculate tag suggestions for efficient navigation."""
        pass
