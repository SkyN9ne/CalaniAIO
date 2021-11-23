from console.utils import set_title
from colorama import Fore
from requests import get
from time import sleep

red = Fore.RED
cyan = Fore.CYAN
reset = Fore.RESET

def check():
    """Checks for updates"""
    set_title("Calani AIO | Checking For Updates | MickeyYe#0003")
    print(f"    [{cyan}>{reset}] Checking for updates")
    try:
        v = get("https://raw.githubusercontent.com/Mickey758/Calani-AIO/master/version").text.rstrip()
        if v != "0.2.0":
            return True
        else:
            return False
    except:
        print(f"    [{red}>{reset}] Could not connect to update server")
        sleep(2)
        return False
