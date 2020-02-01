import abc

class BaseResource(abc.ABC):

    @property
    def name(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    @property
    def type(self):
        raise NotImplementedError

    @property
    def client(self):
        raise NotImplementedError

    @property
    def dry_run(self):
        raise NotImplementedError

    @property
    def configuration(self):
        raise NotImplementedError

    @property
    def resources(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_resources(self):
        pass

    @abc.abstractmethod
    def list_resources(self):
        pass

    @abc.abstractmethod
    def delete_resources(self):
        pass
