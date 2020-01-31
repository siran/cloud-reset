import abc

class BaseResource(abc.ABC):

    @abc.abstractmethod
    def get_resources(self):
        pass

    @abc.abstractmethod
    def list_resources(self):
        pass

    @abc.abstractmethod
    def delete_resources(self):
        pass
