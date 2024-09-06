import logging
import json
from logging_commons.utils import MDC


class JsonFormatter(logging.Formatter):
    """
    Formatter that outputs JSON strings after parsing the LogRecord.

    @param dict format_dict: Key:
    logging format attribute pairs. Defaults to {"message": "message"}.
    @param str time_format: time.strftime() format string.
    Default: "%Y-%m-%dT%H:%M:%S"
    @param str msec_format: Microsecond formatting.
    Appended at the end. Default: "%s.%03dZ"
    """

    def __init__(
        self,
        format_dict: dict = None,
        time_format: str = "%Y-%m-%dT%H:%M:%S",
        msec_format: str = "%s.%03dZ",
    ):
        self.format_dict = (
            format_dict if format_dict is not None else {"message": "message"}
        )
        self.default_time_format = time_format
        self.default_msec_format = msec_format
        self.datefmt = None
        super().__init__(datefmt=None)

    def usesTime(self) -> bool:
        """
        Overwritten to look for the attribute in the format dict values instead of the fmt string.
        """
        return "asctime" in self.format_dict.values()

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        KeyError is raised if an unknown attribute is provided in the format_dict.
        """
        record.__dict__["mdc"] = MDC.get_context_data()
        message_dict = {}
        for fmt_key, fmt_val in self.format_dict.items():
            message_dict[fmt_key] = record.__dict__[fmt_val]
        return message_dict

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method,
        the difference being that a dict is manipulated and dumped as JSON
        instead of a string.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        return json.dumps(message_dict, default=str)
