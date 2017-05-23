"""
Simple in-memory database implementation for tagging
"""


class Database(object):
    """Database for tagging"""

    def __init__(self):
        self._documents = {}
        self._tags = {}
        self._relations = []

    def create_document(self, id, name, type, path):
        """Create a new document."""
        pass

    def find_documents(self, tag_ids):
        """Find the documents which related to the given tags."""
        pass

    def update_document(self, id, name=None, type=None, path=None):
        """Update the document."""
        pass

    def remove_document(self, id):
        """Remove the document"""
        pass

    def create_tag(self, name):
        """Create a new tag."""
        pass

    def find_tags(self, document_ids):
        """Find tags which related to the given documents."""
        pass

    def update_tag(self, id, name):
        """Update the tag."""
        pass

    def remove_tag(self, id):
        """Remove the tag."""
        pass

    def create_relation(self, document_id, tag_id):
        """Create relation between the document and the tag."""
        pass

    def remove_relation(self, document_id, tag_id):
        """Remove the relation between the document and the tag."""
        pass
