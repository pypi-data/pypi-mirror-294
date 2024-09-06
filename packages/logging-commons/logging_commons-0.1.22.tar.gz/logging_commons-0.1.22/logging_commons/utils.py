import threading


class MDCContext(threading.local):
    """MDC context class

    Keyword arguments:
    No arguments
    Return: None
    """

    def __init__(self) -> None:
        self.__context_data: dict[str, any] = {}

    def set(self, key: str, value: any) -> None:
        """set

        Keyword arguments:
        key -- Key
        value -- Value
        Return: None
        """

        self.__context_data[key] = value

    @property
    def context_data(self) -> dict[str, any]:
        """Get context data

        Keyword arguments:
        No arguments
        Return: dict
        """

        return self.__context_data

    def clear(self) -> None:
        """Clear context

        Keyword arguments:
        No arguments
        Return: None
        """
        self.context_data.clear()


class MDC:
    """MDC class

    Keyword arguments:
    kwargs -- Key value pairs
    Return: None
    """

    __context: MDCContext = MDCContext()

    def __init__(self, **kwargs):
        self.__data = kwargs

    def __enter__(self):
        for key, value in self.__data.items():
            MDC.__context.set(key, value)

    def __exit__(self, exc_type, exc_value, traceback):
        MDC.__context.clear()

    @staticmethod
    def get_context_data():
        """Get context data

        Keyword arguments:
        No arguments
        Return: Context data
        """
        if hasattr(MDC.__context, "context_data"):
            return MDC.__context.context_data
        return {}
