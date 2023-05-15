from asyncio import get_event_loop
from typing import Tuple, Any
import aioredis
from aiogram import Dispatcher, Bot
from aiogram import types
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from aiohttp import web
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from babel.core import Locale
from bot_app import db
from bot_app.config import BOT_TOKEN, REDIS
from bot_app.config import I18N_DOMAIN, LOCALES_DIR

loop = get_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
storage = RedisStorage2(**REDIS, loop=loop)
dp = Dispatcher(bot, loop, storage)
redis = aioredis.Redis(decode_responses=True)
routes = web.RouteTableDef()
scheduler = AsyncIOScheduler()


async def set_lang(user_id, lang):
    await redis.hset(I18N_DOMAIN, user_id, lang)
    await db.users.update_locale(user_id, lang)


async def get_lang(user_id):
    lang = await redis.hget(I18N_DOMAIN, user_id)
    if not lang:
        user = await db.users.get_user(user_id)
        if not user:
            lang = 'en'
        else:
            lang = user.language
        await redis.hset(I18N_DOMAIN, user_id, lang)
        return Locale(lang)
    return Locale(lang)


class MyI18nLocale(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        chat: types.Chat = types.Chat.get_current()
        try:
            locale: Locale = await get_lang(chat.id)
        except AttributeError:
            locale = Locale('uk')

        if locale:
            *_, data = args
            language = data['locale'] = locale.language

            return language


i18n = MyI18nLocale(I18N_DOMAIN, LOCALES_DIR)
_ = i18n.gettext
_l = i18n.lazy_gettext
