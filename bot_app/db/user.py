import datetime

from aiogram.types import User

from bot_app.db.base import create_dict_con


async def create_user(user: User, source):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into user (user_id, first_name, user_name, registration, source) '
                      'values (%s, %s, %s, %s, %s)',
                      (user.id, user.first_name, user.username, datetime.datetime.now(), source))
    await con.commit()
    await cur.execute('select * from user where user_id = %s ', (user.id,))
    user_data = await cur.fetchone()
    await con.ensure_closed()
    return user_data


async def get_user(user_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from user where user_id = %s ', (user_id,))
    user_data = await cur.fetchone()
    await con.ensure_closed()
    return user_data


async def get_all():
    con, cur = await create_dict_con()
    await cur.execute('select * from user ')
    users = await cur.fetchall()
    await con.ensure_closed()
    return users
