from colorama import Fore, Style


class Logger:
    def __init__(self):
        self.__colors = {
            "info": Fore.BLUE,
            "warning": Fore.YELLOW,
            "error": Fore.RED,
            "success": Fore.GREEN,
            "debug": Fore.MAGENTA
        }

    def __log(self, message, color):
        print(f"[{self.__colors[color]}{color}{Style.RESET_ALL}] {message}")

    def info(self, message):
        self.__log(message, "info")

    def warning(self, message):
        self.__log(message, "warning")

    def error(self, message):
        self.__log(message, "error")

    def success(self, message):
        self.__log(message, "success")

    def debug(self, message):
        self.__log(message, "debug")