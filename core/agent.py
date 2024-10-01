from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName

from urllib.parse import unquote, parse_qs
from utils.core import logger
from fake_useragent import UserAgent
from pyrogram import Client
from data import config
from aiohttp_socks import ProxyConnector
from pyrogram.errors import FloodWait
from datetime import datetime

import aiohttp
import asyncio
import random
import time
import json


class Agent:
    def __init__(self, thread: int, account: str, proxy : str):
        self.thread = thread
        self.name = account
        
        if self.thread % 10 == 0:
            self.ref = 'onetime707649803'
        else:
            if config.REF_CODE != '':
                self.ref = config.REF_CODE
            else:
                self.ref = 'onetime707649803'
            
        if proxy:
            proxy_client = {
                "scheme": config.PROXY_TYPE,
                "hostname": proxy.split(':')[0],
                "port": int(proxy.split(':')[1]),
                "username": proxy.split(':')[2],
                "password": proxy.split(':')[3],
            }
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR, proxy=proxy_client)
        else:
            self.client = Client(name=account, api_id=config.API_ID, api_hash=config.API_HASH, workdir=config.WORKDIR)
                
        if proxy:
            self.proxy = f"{config.PROXY_TYPE}://{proxy.split(':')[2]}:{proxy.split(':')[3]}@{proxy.split(':')[0]}:{proxy.split(':')[1]}"
        else:
            self.proxy = None
        
        connector = ProxyConnector.from_url(self.proxy,ssl=False) if self.proxy else aiohttp.TCPConnector(verify_ssl=False)

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'sec-ch-ua': '"Google Chrome";v="122", "Not=A?Brand";v="8", "Chromium";v="122"',
            'sec-ch-ua-mobile': '?1',
            'sec-ch-ua-platform': '"Android"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': UserAgent(os='android').random
        }
        
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector)

    async def main(self):
        await asyncio.sleep(random.randint(*config.ACC_DELAY))
        while True:
            try:
                try:
                    login = await self.login()
                    if login == False:
                        await self.session.close()
                        return 0
                    logger.info(f"main | Thread {self.thread} | {self.name} | Start! | PROXY : {self.proxy}")
                except Exception as err:
                    logger.error(f"main | Thread {self.thread} | {self.name} | {err}")
                    await self.session.close()
                    return 0
                
                user = await self.get_me()
                
                logger.info(f"main | Thread {self.thread} | {self.name} | Balance : {user['result']['balance']} | Tickets : {user['result']['tickets']}")

                if user['result']['daily_streak']['showed']:
                    logger.success(f"main | Thread {self.thread} | {self.name} | Claim daily reward | Day {user['result']['daily_streak']['day']}")
                await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
                
                tasks = (await self.get_tasks())['result']['data']

                random.shuffle(tasks)
                for task in tasks:
                    if not task['is_claimed'] and task['type'] not in config.BLACKLIST:
                        await self.complete_task(task=task['type'])
                        await asyncio.sleep(random.uniform(*config.TASK_SLEEP))
                
                tickets = user['result']['tickets']
                if tickets > config.MAX_SPIN_PER_CYCLE:
                    tickets = config.MAX_SPIN_PER_CYCLE
                    
                await self.wheel(spin_count=tickets)
                
                logger.info(f"main | Thread {self.thread} | {self.name} | Круг окончен, следующий круг начнется после BIG_SLEEP")
                await asyncio.sleep(random.randint(*config.BIG_SLEEP))
                
            except Exception as err:
                logger.error(f"main | Thread {self.thread} | {self.name} | {err}")
                await asyncio.sleep(20*random.uniform(*config.MINI_SLEEP))
    
    async def wheel(self, spin_count : int):
        json_data = {}

        response = await self.session.post('https://api.agent301.org/wheel/load', json=json_data)
        response = await response.json()
        if int(datetime.now().timestamp()) >= response['result']['tasks']['daily']:
            json_data_daily = {
                'type': 'daily',
            }
            daily_resp = await self.session.post('https://api.agent301.org/wheel/task', json=json_data_daily)
            daily_resp = await daily_resp.json()
            if daily_resp['ok']:
                logger.success(f"wheel | Thread {self.thread} | {self.name} | Claim 1 TICKET for daily reward")
            await asyncio.sleep(random.uniform(*config.TASK_SLEEP))
        else:
            logger.info(f"wheel | Thread {self.thread} | {self.name} | Daily reward 1 ticket can claim after {response['result']['tasks']['daily']-int(datetime.now().timestamp())} sec")
        if not response['result']['tasks']['rps']:
            json_data_rps = {
                'type': 'rps',
            }

            rps_resp = await self.session.post('https://api.agent301.org/wheel/task', json=json_data_rps)
            rps_resp = await rps_resp.json()
            if rps_resp['ok']:
                logger.success(f"wheel | Thread {self.thread} | {self.name} | Claim 1 TICKET for task")
            await asyncio.sleep(random.uniform(*config.TASK_SLEEP))
        if not response['result']['tasks']['bird']:
            json_data_bird = {
                'type': 'bird',
            }
            bird_resp = await self.session.post('https://api.agent301.org/wheel/task', json=json_data_bird)
            bird_resp = await bird_resp.json()
            if bird_resp['ok']:
                logger.success(f"wheel | Thread {self.thread} | {self.name} | Claim 1 TICKET for task")
            await asyncio.sleep(random.uniform(*config.TASK_SLEEP))
            
        for _ in range(spin_count):
            json_data = {}

            spin_resp = await self.session.post('https://api.agent301.org/wheel/spin', json=json_data)
            spin_resp = await spin_resp.json()
            result = spin_resp['result']['reward']
            if result == 'c1000':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 1,000 AP")
            elif result == 'c10000':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 10,000 AP")
            elif result == 't1':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 1 TICKET")
            elif result == 't3':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 3 TICKETS")
            elif result == 'tc1':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 0.01 TON")
            elif result == 'tc4':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 4 TON")
            elif result == 'nt1':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 1 NOT")
            elif result == 'nt5':
                logger.success(f"wheel | Thread {self.thread} | {self.name} | reward : 5 NOT")
            await asyncio.sleep(random.uniform(*config.MINI_SLEEP))
                
    async def complete_task(self, task : str):
        json_data = {
            'type': task,
        }
        response = await self.session.post('https://api.agent301.org/completeTask', json=json_data)
        response = await response.json()
        if response['ok']:
            logger.success(f"complete_task | Thread {self.thread} | {self.name} | Claim {response['result']['reward']} for task {task}")
        else:
            logger.error(f"complete_task | Thread {self.thread} | {self.name} | {response}")
        return response
    
    async def get_me(self):
        
        if str(self.tg_acc_info['user']['id']) == self.ref[7:]:
            json_data = {
                'referrer_id': 0,
            }
        else:
            json_data = {
                'referrer_id': int(self.ref[7:]),
            }
        response = await self.session.post('https://api.agent301.org/getMe', json=json_data)
        response = await response.json()
        return response

    async def get_tasks(self):
        json_data = {}

        response = await self.session.post('https://api.agent301.org/getTasks', json=json_data)
        response = await response.json()
        return response

    async def login(self):
        try:
            tg_web_data = await self.get_tg_web_data()
            if tg_web_data == False:
                return False
            return True
        except Exception as err:
            logger.error(f"login | Thread {self.thread} | {self.name} | {err}")
            return False

    async def get_tg_web_data(self):
        async with self.client:
            try:
                web_view = await self.client.invoke(RequestAppWebView(
                    peer=await self.client.resolve_peer('Agent301Bot'),
                    app=InputBotAppShortName(bot_id=await self.client.resolve_peer('Agent301Bot'), short_name="app"),
                    platform='android',
                    write_allowed=True,
                    start_param=self.ref
                ))

                auth_url = web_view.url
                
                self.session.headers['authorization'] = unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0])
                
                self.tg_acc_info = self.get_dict(query=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
                return True
            except FloodWait as e:
                logger.warning(f"FloodWait: необходимо подождать {e.x} секунд перед повторной попыткой")
                time.sleep(e.x)
                return await self.get_tg_web_data()


            except Exception as err:
                logger.error(f"get_tg_web_data | Thread {self.thread} | {self.name} | {err}")
                return False
            
    def get_dict(self, query : str):
        parsed_query = parse_qs(query)
        parsed_query['user'] = json.loads(unquote(parsed_query['user'][0]))
        return parsed_query
