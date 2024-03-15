from abc import ABC, abstractmethod


class IAuthService(ABC):

    @staticmethod
    @abstractmethod
    def authenticate_user(username: str, password: str):
        pass

    @staticmethod
    @abstractmethod
    def create_token_for_user(user: dict):
        pass

    @staticmethod
    @abstractmethod
    def get_current_user(token: str):
        pass
