from abc import ABC, abstractmethod

class DatabaseManager(ABC):
    
    @abstractmethod
    def get_credentials(self):
        pass
    
    @abstractmethod
    def get_connection(self):
        pass
    
    @abstractmethod
    def execute_query(self, conn, query):
        pass
    
    @abstractmethod
    def select(self, query):
        pass

    @abstractmethod
    def insert_many(self, table_name, data):
        pass

    @abstractmethod
    def update(self, schema, table_name, data, condition):
        pass

    @abstractmethod
    def delete(self, schema, table_name, condition):
        pass
