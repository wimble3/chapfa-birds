class Logger:
    """Class helper for printing messages."""
    __INFO_PREFIX = "[INFO]"
    __WARNING_PREFIX = "[WARNING]"
    __ERROR_PREFIX = "[ERROR] "

    @staticmethod
    def info(message: object) -> None:
        print(f"{Logger.__INFO_PREFIX} {message}")

    @staticmethod
    def warning(message: object) -> None:
        print(f"{Logger.__WARNING_PREFIX} {message}")

    @staticmethod
    def error(message: object) -> None:
        print(f"{Logger.__ERROR_PREFIX} {message}")
