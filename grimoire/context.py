"""
Context of documents and tags
"""

from grimoire.document import Document
from grimoire.tag import Tag


class Context(object):
    """Represents an in-memory data structure for contexts"""

    def __init__(self):
        self._documents = {}
        self._tags = {}
        self._relations = set()

    def create_document(self, id, name, type, path):
        """Create a new document."""
        if id in self._documents:
            raise ValueError('Invalid document identifier!')
        document = Document(id, name, type, path)
        self._documents[id] = document
        return document

    def get_document(self, id):
        """Get the document."""
        try:
            return self._documents[id]
        except KeyError:
            raise ValueError('Invalid document identifier!')

    def find_documents(self, tag_ids):
        """Find the documents which are related to the given tags."""
        return [self.get_document(document_id) for document_id in self.find_document_ids(tag_ids)]

    def find_document_ids(self, tag_ids):
        """Find the document identifiers which are related to the given tags."""
        document_ids = []
        for document_id in self._documents:
            for tag_id in tag_ids:
                if (document_id, tag_id) not in self._relations:
                    break
            else:
                document_ids.append(document_id)
        return document_ids

    def update_document(self, id, name=None, type=None, path=None):
        """Update the document."""
        document = self.get_document(id)
        new_name = document.name
        new_type = document.type
        new_path = document.path
        if name is not None:
            new_name = name
        if type is not None:
            new_type = type
        if path is not None:
            new_path = path
        self._documents[id] = Document(id, new_name, new_type, new_path)

    def destroy_document(self, id):
        """Remove the document from the context."""
        if id in self._documents:
            removable_relations = []
            for relation in self._relations:
                if relation[0] == id:
                    removable_relations.append(relation)
            for relation in removable_relations:
                self._relations.remove(relation)
            self._documents.pop(id)
        else:
            raise ValueError('Invalid document identifier!')

    def count_documents(self):
        """Count the documents in the database."""
        return len(self._documents)

    def create_tag(self, id, name):
        """Create a new tag."""
        if id in self._tags:
            raise ValueError('Invalid tag identifier!')
        for _, tag in self._tags.items():
            if tag.name == name:
                raise ValueError('The tag name already exist!')
        tag = Tag(id, name)
        self._tags[id] = tag
        return tag

    def get_tag(self, id):
        """Get the tag."""
        try:
            return self._tags[id]
        except KeyError:
            raise ValueError('Invalid tag identifier!')

    def find_tag_id(self, name):
        """Find the tag identifier from the name."""
        for tag_id, tag in self._tags.items():
            if tag.name == name:
                return tag_id
        raise ValueError('Invalid tag name!')

    def find_tags(self, document_ids):
        """Find tags which are related to the given documents."""
        return [self.get_tag(tag_id) for tag_id in self.find_tag_ids(document_ids)]

    def find_tag_ids(self, document_ids):
        """Find tag identifiers which are related to the given documents."""
        tag_ids = []
        for tag_id in self._tags:
            for document_id in document_ids:
                if (document_id, tag_id) not in self._relations:
                    break
            else:
                tag_ids.append(tag_id)
        return tag_ids

    def update_tag(self, id, name):
        """Update the tag."""
        if id not in self._tags:
            raise ValueError('Invalid tag identifier!')
        for _, tag in self._tags.items():
            if tag.name == name:
                raise ValueError('The tag name already exist!')
        self._tags[id] = Tag(id, name)

    def destroy_tag(self, id):
        """Remove the tag from the context."""
        if id in self._tags:
            removable_relations = []
            for relation in self._relations:
                if relation[1] == id:
                    removable_relations.append(relation)
            for relation in removable_relations:
                self._relations.remove(relation)
            self._tags.pop(id)
        else:
            raise ValueError('Invalid tag identifier!')

    def count_tags(self):
        """Count the tags in the database."""
        return len(self._tags)

    def create_relation(self, document_id, tag_id):
        """Create relation between the document and the tag."""
        if document_id not in self._documents:
            raise ValueError('Invalid document identifier!')
        if tag_id not in self._tags:
            raise ValueError('Invalid tag identifier!')
        self._relations.add((document_id, tag_id))

    def destroy_relation(self, document_id, tag_id):
        """Remove the relation between the document and the tag."""
        relation = (document_id, tag_id)
        if relation not in self._relations:
            raise ValueError('The destroyable relation does not exists!')
        self._relations.remove(relation)

    def count_relations(self):
        """Count the relations in the database."""
        return len(self._relations)

    def calc_last_document_id(self):
        """
        Calculate the last document identifier of the managed context.
        :return: a positive integer value
        """
        last_id = 0
        for document_id in self._documents:
            if document_id > last_id:
                last_id = document_id
        return last_id

    def calc_last_tag_id(self):
        """
        Calculate the last tag identifier of the managed context.
        :return: a positive integer value
        """
        last_id = 0
        for tag_id in self._tags:
            if tag_id > last_id:
                last_id = tag_id
        return last_id
