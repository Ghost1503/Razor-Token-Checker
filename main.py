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
import tls_client


with open("data/tokens.txt", "r") as f:
    tokens = f.readlines()

with open("data/proxies.txt", "r") as f:
    proxies = f.readlines()

LOCK = threading.Lock()
tokens = list(set(tokens))
valid = 0
invalid = 0
locked = 0
nitro = 0
flagged = 0
total = len(tokens)
current = 0
no_nitro = 0
done = False
config = toml.load("data/config.toml")
settings = json.loads(open("data/settings.json", "r").read())

banner = str(f'''
                   

██████╗  █████╗ ███████╗ ██████╗ ██████╗     ██████╗  ██████╗  ██████╗ ███████╗████████╗
██╔══██╗██╔══██╗╚══███╔╝██╔═══██╗██╔══██╗    ██╔══██╗██╔═══██╗██╔═══██╗██╔════╝╚══██╔══╝
██████╔╝███████║  ███╔╝ ██║   ██║██████╔╝    ██████╔╝██║   ██║██║   ██║███████╗   ██║   
██╔══██╗██╔══██║ ███╔╝  ██║   ██║██╔══██╗    ██╔══██╗██║   ██║██║   ██║╚════██║   ██║   
██║  ██║██║  ██║███████╗╚██████╔╝██║  ██║    ██████╔╝╚██████╔╝╚██████╔╝███████║   ██║   
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚═════╝  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝                                                                      
                        {pystyle.Colorate.Color(color=pystyle.Colors.cyan, text="https://discord.gg/razor-boost")}


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
        self.session = tls_client.Session(
            client_identifier="chrome_120"
        )

        self.session.headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }

        if not config["main"]["proxyless"]:
            proxy = random.choice(proxies).strip()
            self.session.proxies = {
                "https": f"http://{proxy}",
                "http": f"http://{proxy}"
                }

    def check(self) -> None:
        '''
            Made By Ghost!
        '''
        global current, total, valid, locked, nitro, invalid, flagged, no_nitro, redeemable, non_redeemable
        while True:
            if len(tokens) == 0:
                break
            token = tokens.pop().strip()
            try:
                token_only = token.split(":")[-1]
                half_token = token_only[:20]
                masked_token = half_token + ".***.*****"

                self.session.headers["authorization"] = token_only
                r = self.session.get(f"https://discord.com/api/v9/users/@me/guilds")
                if r.status_code == 429:
                    logger.fail("Rate limited", token=masked_token)
                    tokens.append(token)
                    continue

                current += 1

                if r.status_code == 401:
                    invalid += 1
                    logger.fail("Invalid", token=masked_token)
                    LOCK.acquire()
                    with open(f"{output_folder}/invalid.txt", "a") as f:
                        f.write(token + "\n")
                    LOCK.release()
                    continue

                if r.status_code == 403:
                    locked += 1
                    logger.fail("Locked", token=masked_token)
                    LOCK.acquire()
                    with open(f"{output_folder}/locked.txt", "a") as f:
                        f.write(token + "\n")
                    LOCK.release()

                if r.status_code == 200:
                    try:
                        r = self.session.get(f"https://discord.com/api/v9/users/@me")
                        args = {
                            "token": masked_token,
                        }

                        if settings["flagged"]:
                            try:
                                if r.json()["flags"] & 1048576 == 1048576:
                                    flagged += 1
                                    logger.fail("Flagged", **args)
                                    LOCK.acquire()
                                    with open(f"{output_folder}/flagged.txt", "a") as f:
                                        f.write(token + "\n")
                                    LOCK.release()
                                    continue
                            except Exception as e:
                                logger.fail("Error", **args, error=e)
                                tokens.append(token)
                                continue

                        if settings["type"]:
                            LOCK.acquire()
                            type = "Unclaimed"
                            if r.json()["email"] != None and r.json()["verified"] == True:
                                type = "Email verified"
                            if r.json()["phone"] != None:
                                if type == "Email verified":
                                    type = "Fully verified"
                                else:
                                    type = "Phone verified"
                        else:
                            type = "Valid"

                        args["type"] = type
                        LOCK.release()

                        if settings["age"]:
                            try:
                                LOCK.acquire()
                                created_at = ((int(r.json()["id"]) >> 22) + 1420070400000) / 1000
                                age = (time.time() - created_at) / 86400 / 30
                                if age > 12:
                                    age_int = f"{int(age / 12)} Years"
                                    args["age"] = age_int
                                else:
                                    age_int = f"{int(age)} Month"
                                    args["age"] = age_int

                                if not os.path.exists(f"{output_folder}/Age/{age_int}"):
                                    os.makedirs(f"{output_folder}/Age/{age_int}")

                                with open(f"{output_folder}/Age/{age_int}/{type}.txt", "a") as f:
                                    f.write(token + "\n")
                                LOCK.release()
                            except Exception as e:
                                logger.fail("Error", **args, error=e)
                                tokens.append(token)
                                continue

                        if settings["nitro"]:
                            r = self.session.get(f"https://discord.com/api/v9/users/@me/billing/subscriptions")
                            data = r.json()
                            if data:
                                try:
                                    for sub in r.json():
                                        days_left = (time.mktime(time.strptime(sub["current_period_end"], "%Y-%m-%dT%H:%M:%S.%f%z")) - time.time()) / 86400

                                        r = self.session.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots")
                                        available = 0

                                        for sub in r.json():
                                            if sub["cooldown_ends_at"] == None:
                                                available += 1
                                        LOCK.acquire()
                                        args["boost"] = available

                                        if days_left <= 31:
                                            month = "1 Month"
                                        else:
                                            month = "3 Month"

                                        args["nitro"] = f"{month} [{days_left:.0f}d]"
                                        nitro += 1

                                        LOCK.release()

                                except Exception as e:
                                    logger.fail("Error", **args, error=e)
                                    tokens.append(token)
                                    continue
                            else:
                                LOCK.acquire()
                                args["boost"] = 0
                                args["nitro"] = "No Nitro"
                                with open(f"{output_folder}/No Nitro.txt", "a") as f:
                                    f.write(token + "\n")
                                LOCK.release()
                                no_nitro += 1

                        valid += 1
                        logger.success("Valid", **args)
                        with open(f"{output_folder}/{type}.txt", "a") as f:
                            f.write(token + "\n")
                        with open(f"{output_folder}/Valid.txt", "a") as f:
                            f.write(token + "\n") 
                    except Exception as e:
                        logger.fail("Error", **args, error=e)
                        tokens.append(token)
                        continue

            except Exception as e:
                logger.fail("Error", **args, error=e)
                tokens.append(token)
                continue


def update_title():
    while not done:
        if total != 0:
            time.sleep(0.1)
            ctypes.windll.kernel32.SetConsoleTitleW(f"Razor Token Checker | Valid: {valid} | Invalid: {invalid} | Locked: {locked} | Remaining: {len(tokens)} | Checked: {current/total*100:.2f}% | CPS: {current/(time.time()-start)*1:.2f}")


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

    checker = Checker()

    with concurrent.futures.ThreadPoolExecutor(max_workers=config["main"]["threads"]) as executor:
        for i in range(config["main"]["threads"]):
            executor.submit(checker.check)

    done = True
    update.join()
    print()
    logger.info(f"Checked {current} tokens in {time.gmtime(time.time()-start).tm_min} minutes and {time.gmtime(time.time()-start).tm_sec} seconds")
    logger.info("Finished checking tokens:", Checked=current, Valid=valid, Invalid=invalid, Nitro=nitro, Locked=locked, Flagged=flagged)
    logger.info("Press Enter to exit.")
    wait_for_enter()
