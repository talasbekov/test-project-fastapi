from exceptions import NotSupportedException


class BaseHandler:
    __handler__ = "base_handler"

    def handle_action(self, *args, **kwargs):
        raise NotSupportedException(
            f"This handler: {self.__handler__} does not support any actions"
        )
