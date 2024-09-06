# Python Logging Tools

## Usage

### Logging Config

```python
config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging_commons.formatter.JsonFormatter",
            "format_dict": {
                "level": "levelname",
                "timestamp": "asctime",
                "logger_name": "name",
                "module": "module",
                "line": "lineno",
                "message": "message",
                "context": "mdc",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}
```

Example Output

```json
{
    "level": "INFO",
    "timestamp": "2024-08-19T20:57:12.998Z",
    "logger_name": "main",
    "module": "main",
    "line": 22,
    "message": "Hello world!",
    "context": {
        "process_id": "fa0fb339-6bac-4b4b-ab17-3812689c71e4"
    }
}
```

### MDC Usage

```python
import logging
from logging_commons.utils import MDC

LOGGER = logging.getLogger(__name__)

with MDC(process_id=):
    LOGGER.info("Hello world!")
```

## Special Thanks:

- [Bogdan Mircea](https://stackoverflow.com/users/11971654/bogdan-mircea) for the `JsonFormatter` code given in [Stackoverflow](https://stackoverflow.com/a/70223539)