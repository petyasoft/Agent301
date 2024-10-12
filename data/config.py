# api id, hash
API_ID = 11111111
API_HASH = 'Your api hash'

USE_TG_BOT = False # True if you want use tg, else False
BOT_TOKEN = '' # API TOKEN get in @BotFather
CHAT_ID = '' # Your telegram id

# задержка между подключениями к аккаунтам
ACC_DELAY = [5, 150]

# тип прокси
PROXY_TYPE = "socks5" # http/socks5

# папка с сессиями (не менять)
WORKDIR = "sessions/"

# использование прокси
USE_PROXY = True # True/False
# проверять прокси
CHECK_PROXY = True

#то что идет после startapp=
REF_CODE = ""

# мини задержка 
MINI_SLEEP = [7, 20] #[min, max]

# задержка между тасками
TASK_SLEEP = [25, 50] #[min, max]

# макимальное количество спинов в рулетке за круг
MAX_SPIN_PER_CYCLE = 10

# задержка после круга
BIG_SLEEP = [24*60*60,28*60*60]

# таски которые он будет скипать
BLACKLIST = {'stars_purchase', 'invite_3_friends', 'transaction', 'boost'}

hello ='''              _                               __  _        
 _ __    ___ | |_  _   _   __ _  ___   ___   / _|| |_  ___ 
| '_ \  / _ \| __|| | | | / _` |/ __| / _ \ | |_ | __|/ __|
| |_) ||  __/| |_ | |_| || (_| |\__ \| (_) ||  _|| |_ \__ \\
| .__/  \___| \__| \__, | \__,_||___/ \___/ |_|   \__||___/
|_|                |___/        

'''
