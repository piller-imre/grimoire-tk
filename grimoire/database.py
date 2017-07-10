"""
Simple in-memory database implementation for tagging
"""

from grimoire.context import Context
from grimoire.logger import Logger


class Database(Context):
    """Database for tagging"""

    def __init__(self, path='/tmp/grimoire.log'):
        super(Database, self).__init__()
        self._logger = Logger(path)
        self._logger.disable_logging()
        self._last_document_id = 0
        self._last_tag_id = 0
        self._logger.restore_context(self)
        self._last_document_id = self.calc_last_document_id()
        self._last_tag_id = self.calc_last_tag_id()
        self._logger.enable_logging()

    def generate_document_id(self):
        """
        Generate new document identifier.
        :return: a positive integer value
        """
        self._last_document_id += 1
        return self._last_document_id

    def generate_tag_id(self):
        """
        Generate a new tag identifier.
        :return: a positive integer value
        """
        self._last_tag_id += 1
        return self._last_tag_id

    def save_operation(self, method, **arguments):
        """
        Save the operation to file via the logger.
        :param method: name of the called method
        :param arguments: arguments of the given method
        :return: None
        """
        arguments['method'] = method
        self._logger.save_operation(arguments)

    def create_document(self, **arguments):
        """
        Create a new document for the database.
        :return: the created document object
        """
        document_id = self.generate_document_id()
        arguments['id'] = document_id
        document = super(Database, self).create_document(**arguments)
        self.save_operation('create_document', **arguments)
        return document

    def update_document(self, **arguments):
        """
        Update an existing document.
        :return: None
        """
        super(Database, self).update_document(**arguments)
        self.save_operation('update_document', **arguments)

    def destroy_document(self, **arguments):
        """
        Destroy the given document.
        :return: None
        """
        super(Database, self).destroy_document(**arguments)
        self.save_operation('destroy_document', **arguments)

    def create_tag(self, **arguments):
        """
        Create a new tag.
        :return: None
        """
        tag_id = self.generate_tag_id()
        arguments['id'] = tag_id
        tag = super(Database, self).create_tag(**arguments)
        self.save_operation('create_tag', **arguments)
        return tag

    def update_tag(self, **arguments):
        """
        Update an existing tag.
        :return: None
        """
        super(Database, self).update_tag(**arguments)
        self.save_operation('update_tag', **arguments)

    def destroy_tag(self, **arguments):
        """
        Destroy the given tag.
        :return: None
        """
        super(Database, self).destroy_tag(**arguments)
        self.save_operation('destroy_tag', **arguments)

    def create_relation(self, **arguments):
        """
        Create a new relation.
        :return: None
        """
        super(Database, self).create_relation(**arguments)
        self.save_operation('create_relation', **arguments)

    def destroy_relation(self, **arguments):
        """
        Destroy an existing relation.
        :return: None
        """
        super(Database, self).destroy_relation(**arguments)
        self.save_operation('destroy_relation', **arguments)
