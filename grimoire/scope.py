"""
Scope class definition
"""


class Scope(object):
    """Represents a scope in the context"""

    def __init__(self, database):
        """
        Construct an empty scope for the database.
        :param database: the managed database
        :return: None
        """
        self._database = database
        self._documents = []
        self._tags = []
        self._selected_document_ids = []
        self._selected_tag_ids = []
        self._ordering = None

    def create_document(self, name, type, path):
        """
        Create a new document in the actual concept.
        :param name: the name of the document, practically the filename
        :param type: the type of the document, similar to MIME type
        :param path: the path of the document file in the filesystem
        :return: the created document object
        """
        pass

    def copy_document(self, document_id):
        """
        Copy the document to the actual concept.
        It extends the tags of the document with the query tags of the scope.
        :param document_id: the identifier of the copied document
        :return: None
        :raises ValueError: for invalid document identifier
        """
        pass

    def move_document(self, document_id):
        """
        Move the document to the actual concept.
        It replaces the tags of the document to the query tags.
        :param document_id: the identifier of the movable document
        :return: None
        :raises ValueError: for invalid document identifier
        """
        pass

    def clone_document(self, document_id):
        """
        Creates an exact copy of the document.
        :param document_id: the identifier of the cloneable document
        :return: a document object
        :raises ValueError: for invalid document identifier
        """
        pass

    def destroy_document(self, document_id):
        """
        Destroy the document of the selected context.
        It removes the document from the context.
        It removes the relations to the tags.
        :param document_id: the identifier of the destroyable document
        :return: None
        :raises ValueError: for invalid document identifier
        """
        pass

    def get_document(self, document_id):
        """
        Get document by identifier from the context.
        :param document_id: the identifier of the required document
        :return: a document object with the given identifier
        :raises ValueError: for invalid document identifier
        """
        pass

    def get_documents(self):
        """
        Get the documents of the scope.
        :return: the list of document objects
        """
        pass

    def toggle_document_selection(self, document_id):
        """
        Toggle the selection state of the document.
        :param document_id: the identifier of the selected document
        :return: None
        :raises ValueError: for invalid document identifier
        """
        pass

    def select_document(self, document_id):
        """
        Add a document to the selection.
        :param document_id: the identifier of the selected document
        :return: None
        :raises ValueError: for invalid document identifier
        """
        pass

    def deselect_document(self, document_id):
        """
        Remove the document from the given selection.
        :param document_id: the identifier of the selected document
        :return: None
        :raises ValueError: for invalid document identifier
        """
        pass

    def deselect_all_documents(self):
        """
        Remove all documents selection.
        :return: None
        """
        pass

    def collect_documents(self):
        """
        Collect the documents according to the current tags.
        It is necessary after any query modification.
        :return: None
        """
        pass

    def create_tag(self, name):
        """
        Create tag for the managed context.
        :param name: the name of the tag
        :return: the created tag object
        :raises ValueError: for existing tag name
        """
        pass

    def add_tag(self, tag_id):
        """
        Add a tag to the query or to the selected documents.
        :param tag_id: the identifier of the required tag
        :return: None
        :raises ValueError: for invalid tag identifier
        """
        pass

    def remove_tag(self, tag_id):
        """
        Remove the tag from the scope and/or from the selected documents.
        :param tag_id: the identifier of the removable tag
        :return: None
        :raises ValueError: for invalid tag identifier
        """
        pass

    def destroy_tag(self, tag_id):
        """
        Destroy the tag of the managed context.
        It removes all relation to the tagged documents.
        :param tag_id: the identifier of the destroyable tag
        :return: None
        :raises ValueError: for invalid tag identifier
        """
        pass

    def get_tag(self, tag_id):
        """
        Get tag by identifier from the context.
        :param tag_id: the identifier of the destroyable tag
        :return: a tag object with the given tag identifier
        :raises ValueError: for invalid tag identifier
        """
        pass

    def get_tags(self):
        """
        Get the tags of the scope.
        :return: the list of tag objects
        """
        pass

    def get_query_tags(self):
        """
        Get the query tags of the scope.
        :return: the list of tag objects
        """
        pass

    def get_document_only_tags(self):
        """
        Get the tags of the selected documents which are not in the query.
        :return: the list of tag objects
        """

    def get_suggested_tags(self, input):
        """
        Calculate tag suggestions for efficient navigation.
        :param input: the content of actual text input
        :return: the list of tag names as strings
        """
        pass

    def collect_tags(self):
        """
        Collect the tags according to the selected documents.
        It is necessary after any document selection event.
        :return: None
        """
        pass
