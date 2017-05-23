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

    def get_document(self, id):
        """Get the document."""
        pass

    def find_documents(self, tag_ids):
        """Find the documents which are related to the given tags."""
        pass

    def find_document_ids(self, tag_ids):
        """Find the document identifiers which are related to the given tags."""
        pass

    def update_document(self, id, name=None, type=None, path=None):
        """Update the document."""
        pass

    def remove_document(self, id):
        """Remove the document"""
        pass

    def count_documents(self):
        """Count the documents in the database."""
        pass

    def create_tag(self, id, name):
        """Create a new tag."""
        pass

    def get_tag(self, id):
        """Get the tag."""
        pass

    def find_tag_id(self, name):
        """Find the tag identifier from the name."""
        pass

    def find_tags(self, document_ids):
        """Find tags which are related to the given documents."""
        pass

    def find_tag_ids(self, document_ids):
        """Find tag identifiers which are related to the given documents."""
        pass

    def update_tag(self, id, name):
        """Update the tag."""
        pass

    def remove_tag(self, id):
        """Remove the tag."""
        pass

    def count_tags(self):
        """Count the tags in the database."""
        pass

    def create_relation(self, document_id, tag_id):
        """Create relation between the document and the tag."""
        pass

    def remove_relation(self, document_id, tag_id):
        """Remove the relation between the document and the tag."""
        pass

    def count_relations(self):
        """Count the relations in the database."""
        pass
