from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button
import sqlite3, paymentManager
import asyncio, nest_asyncio
nest_asyncio.apply()
loop = asyncio.get_event_loop()
def button(text, id):
    return Button.inline(text, str(id).encode())
cnx = sqlite3.connect('djangodb')
cursor = cnx.cursor()
cursor.execute('SELECT * FROM "db_bot" WHERE const_id="black"')
black_bot = cursor.fetchone()
cursor.execute('SELECT * FROM "db_botdetails" WHERE const_id="black"')
black_desc = cursor.fetchone()
cursor.execute('SELECT * FROM "db_plansprice"')
prices = cursor.fetchall()
print(prices)
cnx.commit()
cnx.close()
BOT_TOKEN = black_bot[3]
class StopCl():
    run=True
    def set(self, bool):
        self.run=bool
runcl = StopCl()
bot = TelegramClient(black_bot[4], black_bot[1], black_bot[2])
btns = [[
        Button.inline("Тарифы🔥❤️", b"1")
    ],[
        Button.inline("За что я плачу🤍🤝", b"2")
    ],[
        Button.inline("❕❗ ВАЖНАЯ ИНФА ❗❕", b"help")
    ]]
forces={}
def set_forces( n, v):
    forces[n]=v
async def check_for_user(user, oid, url):
    if forces[user[0:len(user)-12]]==False:
        while runcl.run:
            if forces[user[0:len(user)-12]]:
                await bot.send_message(user[0:len(user)-12], f"Вы отменили платеж.", buttons=btns)
                return
            if paymentManager.mgr.isOrderDone(oid):
                await bot.send_message(user[0:len(user)-12], f"Вы оплатили платеж. \nВаша ссылка:\n{url}", buttons=btns)
                print("Успешно!")
                forces[user[0:len(user)-12]]=False
                return
            print(f"Ожидание {user}.")
            await asyncio.sleep(0.2)
    else:
        await bot.send_message(user[0:len(user)-12], f"Вы отменили платеж.", buttons=btns)
        return
bot.start(bot_token=BOT_TOKEN)
def btn_gen(price, user, oid):
    return [[Button.url("Купить", paymentManager.mgr.mk_order(oid, price, user))], [button("Отмена", "ret")]]
@bot.on(events.NewMessage(pattern="/start"))
async def chat_action(event):
    await event.respond("Приветствую вас в главном меню.", buttons=btns)
    snd=await event.get_sender()
    print(f"[C_EVENT] USER:{snd.username} MSG:{event.message.message}")
@bot.on(events.CallbackQuery())
async def two(event):
    loop = asyncio.get_event_loop()
    snd=await event.get_sender()
    unm=snd.username
    print(f"[BUTTON_EVENT] USER:{snd.username} ID=1")
    id = event.data
    if(id==b'1'):
        await event.respond(black_desc[3], buttons=[
            [button(f"1️⃣💘Mini Pack🎒 - {prices[0][2]}₽", "3")],
            [button(f"2️⃣👱‍♀️OnlyFaнS👙 - {prices[1][2]}₽", '4')],
            [button(f"3️⃣🧒hentai loli👶 - {prices[2][2]}₽", '5')],
            [button(f"4️⃣🎗7-15 years🎭 - {prices[3][2]}₽", '6')],
            [button(f"5️⃣🎒9-11 SCHOOL💌 - {prices[4][2]}₽",'7')],
            [button(f"6️⃣🤱5-10 years🎒 - {prices[5][2]}₽", '8')],
            [button(f"7️⃣👗2-8 years🍼 - {prices[6][2]}₽", '9')],
            [button(f"8️⃣🎢BIG PACK🎡 - {prices[7][2]}₽", '10')],
            [button(f"9️⃣👄👩‍❤️‍💋‍👩Ultra big pack👩🫦 - {prices[8][2]}₽", '11')],
            [button(f"1️⃣0️⃣🔥RAPE (ИЗНОС)🔥 - {prices[9][2]}₽", '14')],
            [button(f"1️⃣1️⃣💏gay pack 6-16💏 - {prices[10][2]}₽", '15')],
            [button(f"1️⃣2️⃣🔥👑ALL IN👑🔥 - {prices[11][2]}₽", '12')],
            [button("◄ Назад", '13')]])
    if(id==b'ret'):
        if unm in forces:
            set_forces(unm, True)
        await event.respond(black_desc[3], buttons=[
            [button(f"1️⃣💘Mini Pack🎒 - {prices[0][2]}₽", "3")],
            [button(f"2️⃣👱‍♀️OnlyFaнS👙 - {prices[1][2]}₽", '4')],
            [button(f"3️⃣🧒hentai loli👶 - {prices[2][2]}₽", '5')],
            [button(f"4️⃣🎗7-15 years🎭 - {prices[3][2]}₽", '6')],
            [button(f"5️⃣🎒9-11 SCHOOL💌 - {prices[4][2]}₽",'7')],
            [button(f"6️⃣🤱5-10 years🎒 - {prices[5][2]}₽", '8')],
            [button(f"7️⃣👗2-8 years🍼 - {prices[6][2]}₽", '9')],
            [button(f"8️⃣🎢BIG PACK🎡 - {prices[7][2]}₽", '10')],
            [button(f"9️⃣👄👩‍❤️‍💋‍👩Ultra big pack👩🫦 - {prices[8][2]}₽", '11')],
            [button(f"1️⃣0️⃣🔥RAPE (ИЗНОС)🔥 - {prices[9][2]}₽", '14')],
            [button(f"1️⃣1️⃣💏gay pack 6-16💏 - {prices[10][2]}₽", '15')],
            [button(f"1️⃣2️⃣🔥👑ALL IN👑🔥 - {prices[11][2]}₽", '12')],
            [button("◄ Назад", '13')]])
    if id==b'3':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "Probnik"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—🔥150 ПРОБНЫХ ВИДЕО🔥 
—💵МЕЛКИЕ💵
—👄ИНЦЕСТ👄
—👠ШКОЛЬНИЦЫ👠
—💏ГЕЙСЫ💏
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[0][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+Mp8uDwdCfmM1MTJh"))
    if id==b'4':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "Onlik"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—🔥1500 ВИДЕО🔥 
—👄МОКРЫЕ ПИСИ👄
—👠ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ👠
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[1][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+BfoNA4D-pVpmMjA9"))
    if id==b'5':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "hent"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—💌500 ВИДЕО И ФОТО💌 
—👄МЕЛКИЕ👄
—👠ШКОЛЬНИЦЫ👠
—🤱БРАТ И СЕСТРА🤱
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[2][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+ep5A3EruyogxODM9"))
    if id==b'6':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "sevenyo"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙2000 ВИДЕО И ФОТО👙 
—🎡МЕЛКИЕ🎡
—🎒ШКОЛЬНИЦЫ🎒
—👗ИНЦЕСТ👗
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[3][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+Q2IcBMsQqgE1NjBl"))
    if id==b'7':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "school"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙3000 ВИДЕО И ФОТО👙 
—🎒ШКОЛЬНИЦЫ🎒
—👗БРАТ И СЕСТРА👗
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[4][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+hYSpN32nhPhhM2Jl"))
    if id==b'8':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "fiveyo"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙3500 ВИДЕО И ФОТО👙 
—🎒ИНCEST🎒
—👗БРАТ И СЕСТРА👗
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[5][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "future tg"))
    if id==b'9':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "threeyo"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙5.000 ВИДЕО И ФОТО👙 
—🎒В ЭТОМ ПАКЕ ЕСТЬ ВСЕ - ЦП, ИНЦЕСТ, ШКОЛО, ГЕИ, ПЕДО МАМКИ.🎒
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[6][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+LuHI9MBzlkxlNTk1"))
    if id==b'10':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "bigpck"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙5.000 ВИДЕО И ФОТО👙 
—🎒В ЭТОМ ПАКЕ ЕСТЬ ВСЕ - ЦП, ИНЦЕСТ, ШКОЛО, ГЕИ, ПЕДО МАМКИ.🎒
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[7][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+__WMNED17F0yNTE1"))
    if id==b'11':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "ubp"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙6.000 ВИДЕО И ФОТО👙  
—👄ВЗРОСЛЫЕ👄
—🎡МЕЛКИЕ🎡
—🎒ШКОЛЬНИЦЫ🎒
—👗ИНЦЕСТ👗
—👑В ДВА РАЗА ЛУЧШЕ КОНТЕНТ НЕЖЕЛИ В ОБЫЧНОМ БИГ ПАКЕ👑
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[8][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+2T2OigU9CqA4ZDI1"))
    if id==b'14':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "rpevids"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👙500+ ВИДЕО И ФОТО👙  
—👄ВЗРОСЛЫЕ👄
—🎡МЕЛКИЕ🎡
—🎒ШКОЛЬНИЦЫ🎒
—👗ИНЦЕСТ👗
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—💌ПРИВАТНЫЙ КАНАЛ💌
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[9][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+pRUoqWlRno5mMjcx"))
    if id==b'15':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "gypck"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—🎗6.000 ВИДЕО И ФОТО🎗 
—🎗ВЗРОСЛЫЕ🎗
—🎗МЕЛКИЕ🎗
—🎗ИНЦЕСТ🎗
—🎗ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ🎗
—🎗ПРИВАТНЫЙ КАНАЛ🎗
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[10][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+EG62SwWP1J42Njgx"))
    if id==b'12':
        set_forces(unm, True)
        loop = asyncio.get_event_loop()
        nm = unm+paymentManager.get_rnd(12)
        oid = "ollinpk"+paymentManager.get_rnd(12)
        await event.respond("""
➖➖➖➖➖➖➖➖➖➖➖
👇🏻ОПИСАНИЯ ТАРИФА👇🏻
➖➖➖➖➖➖➖➖➖➖➖
—👑10.000+ ВИДЕО И ФОТО💵
—💵ЭТО САМЫЙ БОЛЬШОЙ ПАК КОТОРЫЙ ВКЛЮЧАЕТ В СЕБЯ ВСЕ КАТЕГОРИИ НАШЕГО ШОПА👑
—👑ПОЛНЫЙ РЕЗЕРВ ВИДЕО И ПОДПИСКИ💵
—💵ПРИВАТНЫЙ КАНАЛ👑
➖➖➖➖➖➖➖➖➖➖➖
❇️Полная конфиденциальность
❇️Качественный и уникальный контент
➖➖➖➖➖➖➖➖➖➖➖
""",buttons=btn_gen(prices[11][2], unm, oid))
        print("Loop strted")
        print(forces[unm])
        await asyncio.sleep(0.2)
        print("Loop 0.2")
        print(forces[unm])
        set_forces(unm, False)
        await asyncio.sleep(0.05)
        print(forces[unm])
        print("Loop 0.05")
        loop.run_until_complete(check_for_user(nm, oid, "https://t.me/+eqQ1He3nTrcxMzhl"))
    if id==b'13':
        await event.respond("Приветствую вас в главном меню.", buttons=btns)
    if id==b'help':
        await event.respond("""❗❕ ВАЖНО ❕❗
Если вы выбрали ваш тариф и нажали на кнопку, то после того, как вышлется сообщение со ссылкой:
!!НИ В КОЕМ СЛУЧАЕ НЕ НАЖИМАЙТЕ ДРУГИЕ РАЗДЕЛЫ!!
Ваш платеж аннулится, хоть и ссылка будет доступна.
❗❕ ВАЖНО ❕❗
""", buttons=btns)
#TODO:TRFF BUTTONS

bot.run_until_disconnected()