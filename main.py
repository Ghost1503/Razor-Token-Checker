import colorama
import time
import ctypes
import concurrent.futures
import msvcrt
import os
import json
import random
import threading
import pystyle
import logger
import toml
from curl_cffi import requests as request
from datetime import datetime


with open("data/tokens.txt", "r") as f:
    tokens = f.readlines()

with open("data/proxies.txt", "r") as f:
    proxies = f.readlines()

tokens = list(set(tokens))
valid = 0
invalid = 0
locked = 0
nitro = 0
flagged = 0
total = len(tokens)
current = 0
no_nitro = 0
redeemable = 0
non_redeemable = 0
done = False
config = toml.load("data/config.toml")
settings = json.loads(open("data/settings.json", "r").read())

LOCK = threading.Lock()
TOKEN_LOCK = threading.Lock()
MAX_RETRIES_PER_TOKEN = 5
REQUEST_TIMEOUT = 15

banner = str(f'''
                   

██████╗  █████╗ ███████╗ ██████╗ ██████╗     ██████╗  ██████╗  ██████╗ ███████╗████████╗
██╔══██╗██╔══██╗╚══███╔╝██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝
██████╔╝███████║  ███╔╝ ██║   ██║██████╔╝    ██████╔╝██║   ██║██║   ██║███████╗   ██║   
██╔══██╗██╔══██║ ███╔╝  ██║   ██║██╔══██╗    ██╔══██╗██║   ██║██║   ██║╚════██║   ██║   
██║  ██║██║  ██║███████╗╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝                                                                      
                        {pystyle.Colorate.Color(color=pystyle.Colors.cyan, text="https://discord.gg/razor-cap")}


''')
print(pystyle.Center.XCenter(pystyle.Colorate.Vertical(text=banner, color=pystyle.Colors.purple_to_blue), spaces=15))
output_folder = f"output/{time.strftime('%Y-%m-%d %H-%M-%S')}"
logger.info("Checking Tokens", output=output_folder, total=total)
print()

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

start = time.time()

class Checker:
    def __init__(self) -> None:
        self.new_session()

    def new_session(self) -> None:
        try:
            self.session = request.Session(impersonate="chrome131")
            self.session.headers = {
                "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
                'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
            if not config["main"]["proxyless"] and proxies:
                proxy = random.choice(proxies).strip()
                self.session.proxies = {
                    "https": f"http://{proxy}",
                    "http": f"http://{proxy}"
                }
        except Exception:
            pass

    def retry_errors(self, e):
        err = str(e).lower()
        return (
            "connection" in err or "timeout" in err or "reset" in err or
            "refused" in err or "network" in err or "curl" in err or
            "ssl" in err or "certificate" in err or "remote host" in err or
            "closed" in err or "abruptly" in err
        )

    def check(self) -> None:
        '''
            Made By Ghost!
        '''
        global current, total, valid, locked, nitro, invalid, flagged, no_nitro, redeemable, non_redeemable
        while True:
            token = None
            try:
                TOKEN_LOCK.acquire()
                if not tokens:
                    TOKEN_LOCK.release()
                    break
                token = tokens.pop().strip()
                TOKEN_LOCK.release()
            except Exception as e:
                if TOKEN_LOCK.locked():
                    try:
                        TOKEN_LOCK.release()
                    except Exception:
                        pass
                logger.fail("Error", error=e)
                continue

            token_only = token.split(":")[-1]
            half_token = token_only[:20]
            masked_token = half_token + ".***.*****"
            args = {"token": masked_token}

            for attempt in range(MAX_RETRIES_PER_TOKEN):
                try:
                    self.session.headers["authorization"] = token_only
                    r = self.session.get("https://discord.com/api/v9/users/@me/guilds", timeout=REQUEST_TIMEOUT)

                    if r.status_code == 429:
                        logger.fail("Rate limited", token=masked_token)
                        TOKEN_LOCK.acquire()
                        tokens.append(token)
                        TOKEN_LOCK.release()
                        break
                    current += 1

                    if r.status_code == 401:
                        invalid += 1
                        logger.fail("Invalid", token=masked_token)
                        LOCK.acquire()
                        with open(f"{output_folder}/invalid.txt", "a") as f:
                            f.write(token + "\n")
                        LOCK.release()
                        break
                    if r.status_code == 403:
                        locked += 1
                        logger.fail("Locked", token=masked_token)
                        LOCK.acquire()
                        with open(f"{output_folder}/locked.txt", "a") as f:
                            f.write(token + "\n")
                        LOCK.release()
                        break

                    if r.status_code != 200:
                        raise Exception(f"Unexpected status {r.status_code}")

                    r = self.session.get("https://discord.com/api/v9/users/@me", timeout=REQUEST_TIMEOUT)
                    if r.status_code != 200:
                        raise Exception("users @me failed")
                    try:
                        user_data = r.json()
                    except Exception:
                        user_data = {}
                    if not isinstance(user_data, dict):
                        user_data = {}

                    if settings["flagged"]:
                        if (user_data.get("flags") or 0) & 1048576 == 1048576:
                            flagged += 1
                            logger.fail("Flagged", **args)
                            LOCK.acquire()
                            with open(f"{output_folder}/flagged.txt", "a") as f:
                                f.write(token + "\n")
                            LOCK.release()
                            break

                    if settings["type"]:
                        type_name = "Unclaimed"
                        if user_data.get("email") and user_data.get("verified"):
                            type_name = "Email verified"
                        if user_data.get("phone"):
                            type_name = "Fully verified" if type_name == "Email verified" else "Phone verified"
                    else:
                        type_name = "Valid"
                    args["type"] = type_name

                    if settings["age"]:
                        try:
                            uid = int(user_data.get("id") or 0)
                            created_at = ((uid >> 22) + 1420070400000) / 1000
                            age = (time.time() - created_at) / 86400 / 30
                            age_int = f"{int(age / 12)} Years" if age > 12 else f"{int(age)} Month"
                            args["age"] = age_int
                            if not os.path.exists(f"{output_folder}/Age/{age_int}"):
                                os.makedirs(f"{output_folder}/Age/{age_int}")
                            LOCK.acquire()
                            with open(f"{output_folder}/Age/{age_int}/{type_name}.txt", "a") as f:
                                f.write(token + "\n")
                            LOCK.release()
                        except Exception:
                            pass

                    if settings["nitro"]:
                        try:
                            r2 = self.session.get("https://discord.com/api/v9/users/@me/billing/subscriptions", timeout=REQUEST_TIMEOUT)
                            data = r2.json() if r2.status_code == 200 else []
                            if isinstance(data, list) and data:
                                for sub in data:
                                    if not isinstance(sub, dict):
                                        continue
                                    try:
                                        end = sub.get("current_period_end")
                                        if not end:
                                            continue
                                        days_left = (time.mktime(time.strptime(end.replace("Z", "+00:00")[:26], "%Y-%m-%dT%H:%M:%S.%f")) - time.time()) / 86400
                                        r3 = self.session.get("https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", timeout=REQUEST_TIMEOUT)
                                        slots = r3.json() if r3.status_code == 200 else []
                                        available = sum(1 for s in (slots if isinstance(slots, list) else []) if isinstance(s, dict) and s.get("cooldown_ends_at") is None)
                                        month = "1 Month" if days_left <= 31 else "3 Month"
                                        args["boost"] = available
                                        args["nitro"] = f"{month} [{days_left:.0f}d]"
                                        nitro += 1
                                        cooldown = sub.get("cooldown_ends_at")
                                        if cooldown is None:
                                            path = f"{output_folder}/Nitro/No Cooldown/{month}/{days_left:.0f} days"
                                            if not os.path.exists(path):
                                                os.makedirs(path)
                                            LOCK.acquire()
                                            with open(f"{path}/{available} boosts.txt", "a") as f:
                                                f.write(token + "\n")
                                            LOCK.release()
                                            args["cooldown"] = "No Cooldown"
                                        else:
                                            dt_obj = datetime.fromisoformat(str(cooldown).replace("Z", "+00:00"))
                                            cd = f"{dt_obj.day}d {dt_obj.hour}hrs"
                                            path = f"{output_folder}/Nitro/Cooldown/{month}/{days_left:.0f} days"
                                            if not os.path.exists(path):
                                                os.makedirs(path)
                                            LOCK.acquire()
                                            with open(f"{path}/{cd}.txt", "a") as f:
                                                f.write(token + "\n")
                                            LOCK.release()
                                            args["cooldown"] = cd
                                    except Exception:
                                        pass
                            else:
                                LOCK.acquire()
                                args["boost"] = 0
                                args["nitro"] = "No Nitro"
                                with open(f"{output_folder}/No Nitro.txt", "a") as f:
                                    f.write(token + "\n")
                                LOCK.release()
                                no_nitro += 1
                        except Exception:
                            LOCK.acquire()
                            try:
                                args["boost"] = 0
                                args["nitro"] = "No Nitro"
                                with open(f"{output_folder}/No Nitro.txt", "a") as f:
                                    f.write(token + "\n")
                                no_nitro += 1
                            except Exception:
                                pass
                            LOCK.release()

                    if settings["redeemable"]:
                        try:
                            r2 = self.session.get("https://discord.com/api/v9/users/@me/billing/subscriptions?include_inactive=true", timeout=REQUEST_TIMEOUT)
                            if r2.status_code == 200 and isinstance(r2.text, str):
                                if "[]" in r2.text:
                                    args["redeemable"] = "Redeemable"
                                    with open(f"{output_folder}/Redeemable.txt", "a") as f:
                                        f.write(token + "\n")
                                    redeemable += 1
                                else:
                                    args["redeemable"] = "Non Redeemable"
                                    with open(f"{output_folder}/Non Redeemable.txt", "a") as f:
                                        f.write(token + "\n")
                                    non_redeemable += 1
                        except Exception:
                            pass

                    valid += 1
                    logger.success("Valid", **args)
                    LOCK.acquire()
                    with open(f"{output_folder}/{type_name}.txt", "a") as f:
                        f.write(token + "\n")
                    with open(f"{output_folder}/Valid.txt", "a") as f:
                        f.write(token + "\n")
                    LOCK.release()
                    break

                except Exception as e:
                    if not self.retry_errors(e) or attempt >= MAX_RETRIES_PER_TOKEN - 1:
                        TOKEN_LOCK.acquire()
                        tokens.append(token)
                        TOKEN_LOCK.release()
                        logger.fail("Error", **args, error=e)
                        break
                    self.new_session()
                    time.sleep(0.2 + random.uniform(0, 0.3))
                    continue


def update_title():
    while not done:
        try:
            time.sleep(0.1)
            elapsed = max(time.time() - start, 0.001)
            pct = (current / total * 100) if total else 0
            cps = current / elapsed if elapsed else 0
            ctypes.windll.kernel32.SetConsoleTitleW(f"Razor Token Checker | Valid: {valid} | Invalid: {invalid} | Locked: {locked} | Remaining: {len(tokens)} | Checked: {pct:.2f}% | CPS: {cps:.2f}")
        except Exception:
            pass


def wait_for_enter():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\r':
                break

    logger.info("Exiting in 3 seconds...")
    time.sleep(3)

if __name__ == "__main__":
    colorama.init()
    time.sleep(0.1)
    update = threading.Thread(target=update_title)
    update.start()

    with concurrent.futures.ThreadPoolExecutor(max_workers=config["main"]["threads"]) as executor:
        for i in range(config["main"]["threads"]):
            executor.submit(Checker().check)

    done = True
    update.join()
    print()
    logger.info(f"Checked {current} tokens in {time.gmtime(time.time()-start).tm_min} minutes and {time.gmtime(time.time()-start).tm_sec} seconds")
    logger.info("Finished checking tokens:", Checked=current, Valid=valid, Invalid=invalid, Nitro=nitro, Locked=locked, Flagged=flagged, Redeemable=redeemable, Non_Redeemable=non_redeemable)
    logger.info("Press Enter to exit.")
    wait_for_enter()
