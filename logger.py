import colorama
import time

colorama.init(autoreset=False)

def log(message, **kwargs):

    if len(kwargs) > 0:
        message += f" {colorama.Fore.LIGHTBLACK_EX}→ {colorama.Fore.WHITE}"
        for key in kwargs:
            message += f"{colorama.Fore.LIGHTBLACK_EX}{key}={colorama.Fore.LIGHTCYAN_EX} {kwargs[key]} "

    print(
        f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.LIGHTMAGENTA_EX}{time.strftime('%H:%M:%S', time.localtime())}{colorama.Fore.LIGHTBLACK_EX}] {colorama.Fore.WHITE}{message}"
    )

def fail(message, **kwargs):
    log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.RED}INFO{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.RED} {message}", **kwargs)

def success(message, **kwargs):
    log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.LIGHTGREEN_EX}INFO{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.LIGHTCYAN_EX} {message}", **kwargs)

def info(message, **kwargs):
    log(f"{colorama.Fore.LIGHTBLACK_EX}[{colorama.Fore.BLUE}INFO{colorama.Fore.LIGHTBLACK_EX}]{colorama.Fore.LIGHTGREEN_EX} {message}", **kwargs)