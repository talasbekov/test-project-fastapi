class BaseAutoTagHandler:
    __handler__ = None

    def handle(self, *args, **kwargs):
        raise NotImplementedError("handle method not implemented")
