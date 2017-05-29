"""
Scope class definition
"""


class Scope(object):
    """Represents a scope in the context"""

    def __init__(self, database):
        """Construct an empty scope for the database."""
        self._database = database
        self._documents = []
        self._tags = []
        self._selected_document_ids = []
        self._selected_tag_ids = []
        self._ordering = None

    def create_document(self, name, type, path):
        """Create a new document in the actual concept."""
        pass

    def copy_document(self, document_id):
        """Copy the document to the actual concept."""
        pass

    def move_document(self, document_id):
        """Move the document to the actual concept."""
        pass

    def destroy_document(self, document_id):
        """Destroy the document of the selected context."""
        pass

    def get_document(self, document_id):
        """Get document by identifier from the context."""
        pass

    def get_documents(self):
        """Get the documents of the scope."""
        pass

    def toggle_document_selection(self, document_id):
        """Toggle the selection state of the document."""
        pass

    def select_document(self, document_id):
        """Add a document to the selection."""
        pass

    def deselect_document(self, document_id):
        """Remove the document from the given selection."""
        pass

    def deselect_all_documents(self):
        """Remove all documents selection."""
        pass

    def collect_documents(self):
        """Collect the documents according to the current tags."""
        pass

    def create_tag(self, name):
        """Create tag for the managed context."""
        pass

    def add_tag(self, tag_id):
        """Add a tag to the query or to the selected documents."""
        pass

    def remove_tag(self, tag_id):
        """Remove the tag from the scope and/or from the selected documents."""
        pass

    def destroy_tag(self, tag_id):
        """Destroy the tag of the managed context."""
        pass

    def get_tags(self):
        """Get the tags of the scope."""
        pass

    def get_query_tags(self):
        """Get the query tags of the scope."""
        pass

    def get_document_only_tags(self):
        """Get the tags of the selected documents which are not in the query."""

    def get_suggested_tags(self, input):
        """Calculate tag suggestions for efficient navigation."""
        pass

    def collect_tags(self):
        """Collect the tags according to the selected documents."""
        pass
