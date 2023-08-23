import argparse
import asyncio
import aiohttp
import sys
from colorama import Fore, Style

print(Fore.RED + r"""
         (   (      (            )   )  
   (     )\ ))\ )   )\ )      ( /(( /(  
   )\   (()/(()/(  (()/(   (  )\())\()) 
((((_)(  /(_))(_))  /(_))  )\((_)((_)\  
 )\ _ )\(_))(_))   (_))_| ((_)_((_)((_) 
 (_)_\(_) _ \_ _|  | |_| | | |_  /_  /  
  / _ \ |  _/| |   | __| |_| |/ / / /   
 /_/ \_\|_| |___|  |_|  \___//___/___|
 
""" + Style.RESET_ALL)

async def fetch_word(session, url, word):
    async with session.get(f"{url}/{word}") as resp:
        if resp.status == 200:
            print("Status Code:", Fore.GREEN + "\u27A4", resp.status, Style.RESET_ALL)
            data = await resp.json()
            print("Word:", Fore.RED + "\u27A4", word, Style.RESET_ALL)
            print("Received Data:")
            print(data)

async def loop(url, wordlist):
    async with aiohttp.ClientSession() as session:
        tasks = []
        with open(wordlist, "r") as f:
            for word in f:
                word = word.strip()
                task = asyncio.ensure_future(fetch_word(session, url, word))
                tasks.append(task)

        await asyncio.gather(*tasks)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Api Fuzzer")
    parser.add_argument("-url", type=str, help="UrL FoR ReqUEsT")
    parser.add_argument("-wordlist", type=str, help="WoRdLiSt fOr ATtaCK")
    args = parser.parse_args()
    if not (args.url and args.wordlist):
        print("You NeeD tO ProViDe aN *uRl* ANd *WorDlIsT*")
        exit(1)

    loop_coroutine = loop(args.url,args.wordlist)
    asyncio.run(loop_coroutine)
