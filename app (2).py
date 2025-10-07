#╭───𓆩🛡️𓆪───╮
 #    👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
import telebot
from telebot import types
import sqlite3, time, random, string

# ============ حط معلوماتك ============
TOKEN = "6674373168:AAEAs1tNUZTkZzw0adnl0vsxQW7Zy3gAcm0"
ADMIN_ID = 6697545222  # آي دي الأدمن
bot = telebot.TeleBot(TOKEN)

#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    last_daily INTEGER DEFAULT 0,
    referred_by INTEGER
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    price INTEGER,
    stock INTEGER,
    delivery_type TEXT,   -- auto/manual
    content TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS settings (
    key TEXT PRIMARY KEY,
    value TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS links (
    code TEXT PRIMARY KEY,
    points INTEGER,
    max_uses INTEGER,
    used_count INTEGER DEFAULT 0,
    expire_at INTEGER
)""")

conn.commit()

# ============ إعدادات افتراضية ============
def set_default_settings():
    defaults = {
        "daily_status": "on",
        "daily_points": "10",
        "ref_points": "5"
    }
    for k,v in defaults.items():
        cur.execute("INSERT OR IGNORE INTO settings (key,value) VALUES (?,?)",(k,v))
    conn.commit()
set_default_settings()

def get_setting(key):
    cur.execute("SELECT value FROM settings WHERE key=?",(key,))
    r = cur.fetchone()
    return r[0] if r else None

def set_setting(key,value):
    cur.execute("INSERT OR REPLACE INTO settings (key,value) VALUES (?,?)",(key,str(value)))
    conn.commit()

# ============ لوح زيك يلوح ============

def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("🛒 عرض السلع", callback_data="show_products"))
    kb.add(
        types.InlineKeyboardButton("🎁 الجائزة اليومية", callback_data="daily"),
        types.InlineKeyboardButton("👥 الإحالات", callback_data="refs")
    )
    kb.add(types.InlineKeyboardButton("💰 رصيدي", callback_data="balance"))
    return kb

def back_menu():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
    return kb

def admin_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(types.InlineKeyboardButton("➕ إضافة سلعة", callback_data="add_product"))
    kb.add(types.InlineKeyboardButton("📦 إدارة السلع", callback_data="manage_products"))
    kb.add(
        types.InlineKeyboardButton("🎁 فتح الجائزة", callback_data="open_daily"),
        types.InlineKeyboardButton("🚫 غلق الجائزة", callback_data="close_daily")
    )
    kb.add(types.InlineKeyboardButton("⚙️ تعديل نقاط الجائزة", callback_data="set_daily_points"))
    kb.add(types.InlineKeyboardButton("⚙️ تعديل نقاط الإحالة", callback_data="set_ref_points"))
    kb.add(types.InlineKeyboardButton("🔗 صنع رابط نقاط", callback_data="make_link"))
    kb.add(types.InlineKeyboardButton("📊 الإحصائيات", callback_data="stats"))
    kb.add(types.InlineKeyboardButton("📢 رسالة جماعية", callback_data="broadcast"))
    return kb

#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
def reg_user(uid, ref=None):
    cur.execute("SELECT 1 FROM users WHERE user_id=?",(uid,))
    if not cur.fetchone():
        cur.execute("INSERT INTO users (user_id,balance,referred_by) VALUES (?,?,?)",(uid,0,ref))
        conn.commit()
        if ref and ref != uid:
            ref_points = int(get_setting("ref_points"))
            cur.execute("UPDATE users SET balance=balance+? WHERE user_id=?",(ref_points,ref))
            conn.commit()
            try:
                bot.send_message(ref, f"👥 شخص دخل من رابطك! +{ref_points}💎")
            except: pass

# ============ start ============
@bot.message_handler(commands=["start"])
def start(msg):
    uid = msg.from_user.id
    args = msg.text.split()
    ref = None
    if len(args) > 1:
        param = args[1]
        # رابط نقاط
        cur.execute("SELECT points,max_uses,used_count,expire_at FROM links WHERE code=?",(param,))
        link = cur.fetchone()
        if link:
            points,max_uses,used_count,expire_at = link
            now = int(time.time())
            if used_count >= max_uses or now > expire_at:
                bot.send_message(uid,"❌ الرابط منتهي.")
            else:
                cur.execute("UPDATE users SET balance=balance+? WHERE user_id=?",(points,uid))
                cur.execute("UPDATE links SET used_count=used_count+1 WHERE code=?",(param,))
                conn.commit()
                bot.send_message(uid,f"🎁 تمت إضافة {points}💎 لرصيدك من الرابط!")
        else:
            ref = int(param) if param.isdigit() else None
    reg_user(uid, ref)
    bot.send_message(uid,"👋 أهلاً بيك!",reply_markup=main_menu())

#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    uid = call.from_user.id
    if call.data == "back":
        bot.edit_message_text("🏠 القائمة الرئيسية:",uid,call.message.message_id,reply_markup=main_menu())

    elif call.data == "balance":
        cur.execute("SELECT balance FROM users WHERE user_id=?",(uid,))
        bal = cur.fetchone()[0]
        bot.edit_message_text(f"💰 رصيدك: {bal}💎",uid,call.message.message_id,reply_markup=back_menu())

    elif call.data == "daily":
        status = get_setting("daily_status")
        if status=="off":
            bot.edit_message_text("🚫 الجائزة اليومية مغلقة حالياً.",uid,call.message.message_id,reply_markup=back_menu())
            return
        cur.execute("SELECT last_daily FROM users WHERE user_id=?",(uid,))
        last = cur.fetchone()[0]
        now = int(time.time())
        if now-last < 86400:
            bot.edit_message_text("❌ استلمت جائزتك النهاردة، ارجع بكرة.",uid,call.message.message_id,reply_markup=back_menu())
        else:
            points = int(get_setting("daily_points"))
            cur.execute("UPDATE users SET balance=balance+?, last_daily=? WHERE user_id=?",(points,now,uid))
            conn.commit()
            bot.edit_message_text(f"✅ استلمت {points}💎 من الجائزة اليومية.",uid,call.message.message_id,reply_markup=back_menu())

    elif call.data == "refs":
        link = f"https://t.me/{bot.get_me().username}?start={uid}"
        bot.edit_message_text(f"👥 رابط الإحالة:\n{link}",uid,call.message.message_id,reply_markup=back_menu())

    elif call.data == "show_products":
        cur.execute("SELECT id,name,price FROM products WHERE stock>0")
        prods = cur.fetchall()
        kb = types.InlineKeyboardMarkup(row_width=2)
        for pid,name,price in prods:
            kb.add(types.InlineKeyboardButton(f"{name} - {price}💎", callback_data=f"buy_{pid}"))
        kb.add(types.InlineKeyboardButton("🔙 رجوع", callback_data="back"))
        bot.edit_message_text("🛒 السلع المتاحة:",uid,call.message.message_id,reply_markup=kb)

    elif call.data.startswith("buy_"):
        pid = int(call.data.split("_")[1])
        cur.execute("SELECT name,price,delivery_type,content,stock FROM products WHERE id=?",(pid,))
        p = cur.fetchone()
        if not p or p[4]<=0:
            bot.answer_callback_query(call.id,"❌ السلعة غير متاحة")
            return
        name,price,delivery,content,stock = p
        cur.execute("SELECT balance FROM users WHERE user_id=?",(uid,))
        bal = cur.fetchone()[0]
        if bal<price:
            bot.edit_message_text("❌ رصيدك غير كافي.",uid,call.message.message_id,reply_markup=back_menu())
            return
        
#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
        cur.execute("UPDATE users SET balance=balance-? WHERE user_id=?", (price, uid))
        # 2. تحديث مخزون السلعة
        cur.execute("UPDATE products SET stock=stock-1 WHERE id=?", (pid,))
        
        conn.commit()
        # ---متجيش هنا علشان ميقفش ---

        if delivery=="auto":
            bot.edit_message_text(f"✅ اشتريت {name}\n\n📦 المحتوى:\n{content}",uid,call.message.message_id,reply_markup=back_menu())
        else:
            bot.edit_message_text(f"✅ تم تسجيل طلبك للسلعة: {name}\nالإدارة هتتواصل معاك قريباً.",uid,call.message.message_id,reply_markup=back_menu())
        try:
            bot.send_message(ADMIN_ID,f"🔔 عملية شراء:\n👤 {uid}\n📦 {name}\n💰 {price}",reply_markup=None)
        except: pass

   #╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
    elif uid==ADMIN_ID:
        if call.data=="add_product":
            bot.send_message(uid,"📝 ارسل اسم السلعة:")
            bot.register_next_step_handler(call.message, step_add_name)
        elif call.data=="manage_products":
            cur.execute("SELECT id,name FROM products")
            prods = cur.fetchall()
            txt="📦 السلع:\n"
            for i,(pid,name) in enumerate(prods,1):
                txt+=f"{i}. {name} (/del{pid})\n"
            bot.send_message(uid,txt or "❌ مفيش سلع",reply_markup=admin_menu())
        elif call.data=="open_daily": set_setting("daily_status","on"); bot.send_message(uid,"✅ تم فتح الجائزة.",reply_markup=admin_menu())
        elif call.data=="close_daily": set_setting("daily_status","off"); bot.send_message(uid,"🚫 تم غلق الجائزة.",reply_markup=admin_menu())
        elif call.data=="set_daily_points":
            bot.send_message(uid,"📝 ارسل عدد النقاط اليومية:")
            bot.register_next_step_handler(call.message,set_daily_points_step)
        elif call.data=="set_ref_points":
            bot.send_message(uid,"📝 ارسل عدد نقاط الإحالة:")
            bot.register_next_step_handler(call.message,set_ref_points_step)
        elif call.data=="make_link":
            bot.send_message(uid,"📝 ارسل: عدد_النقاط عدد_الاستخدامات عدد_الساعات\nمثال: 50 10 24")
            bot.register_next_step_handler(call.message,make_link_step)
        elif call.data=="stats":
            cur.execute("SELECT COUNT(*) FROM users"); u=cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM products"); p=cur.fetchone()[0]
            bot.send_message(uid,f"📊 الإحصائيات:\n👥 المستخدمين: {u}\n📦 السلع: {p}",reply_markup=admin_menu())
        elif call.data=="broadcast":
            bot.send_message(uid,"📝 ارسل الرسالة للبث:")
            bot.register_next_step_handler(call.message,broadcast_step)

#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top

def step_add_name(msg):
    bot.send_message(msg.chat.id,"💰 ارسل سعر السلعة:")
    bot.register_next_step_handler(msg, lambda m: step_add_price(m, msg.text))

def step_add_price(msg,name):
    try:
        price=int(msg.text)
        bot.send_message(msg.chat.id,"🔢 ارسل الكمية:")
        bot.register_next_step_handler(msg, lambda m: step_add_stock(m, name, price))
    except: bot.send_message(msg.chat.id,"❌ السعر لازم يكون رقم.")

def step_add_stock(msg,name,price):
    try:
        stock=int(msg.text)
        kb = types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        kb.add("📦 تسليم تلقائي","🛎️ إشعار الإدارة")
        bot.send_message(msg.chat.id,"اختار نوع التسليم:",reply_markup=kb)
        bot.register_next_step_handler(msg, lambda m: step_add_delivery(m,name,price,stock))
    except: bot.send_message(msg.chat.id,"❌ الكمية لازم تكون رقم.")

def step_add_delivery(msg,name,price,stock):
    delivery="auto" if "تلقائي" in msg.text else "manual"
    if delivery=="auto":
        bot.send_message(msg.chat.id,"📝 ارسل المحتوى (اللي هيتسلم للمشتري):",reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, lambda m: save_product(m,name,price,stock,delivery))
    else:
        save_product(msg,name,price,stock,delivery,"")

def save_product(msg,name,price,stock,delivery,content=""):
    cur.execute("INSERT INTO products (name,price,stock,delivery_type,content) VALUES (?,?,?,?,?)",
                (name,price,stock,delivery,content if delivery=="auto" else None))
    conn.commit()
    bot.send_message(msg.chat.id,"✅ تم إضافة السلعة!",reply_markup=admin_menu())

def set_daily_points_step(msg):
    try:
        v=int(msg.text)
        set_setting("daily_points",v)
        bot.send_message(msg.chat.id,"✅ تم التحديث.",reply_markup=admin_menu())
    except: bot.send_message(msg.chat.id,"❌ لازم رقم.")

def set_ref_points_step(msg):
    try:
        v=int(msg.text)
        set_setting("ref_points",v)
        bot.send_message(msg.chat.id,"✅ تم التحديث.",reply_markup=admin_menu())
    except: bot.send_message(msg.chat.id,"❌ لازم رقم.")

def make_link_step(msg):
    try:
        pts,uses,hours=map(int,msg.text.split())
        expire=int(time.time())+hours*3600
        code=''.join(random.choices(string.ascii_letters+string.digits,k=8))
        cur.execute("INSERT INTO links (code,points,max_uses,expire_at) VALUES (?,?,?,?)",(code,pts,uses,expire))
        conn.commit()
        bot.send_message(msg.chat.id,f"✅ رابط:\nhttps://t.me/{bot.get_me().username}?start={code}",reply_markup=admin_menu())
    except: bot.send_message(msg.chat.id,"❌ الصيغة خطأ.",reply_markup=admin_menu())

def broadcast_step(msg):
    cur.execute("SELECT user_id FROM users")
    for u in cur.fetchall():
        try: bot.send_message(u[0],msg.text)
        except: pass
    bot.send_message(msg.chat.id,"✅ تم الإرسال.",reply_markup=admin_menu())

#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top
@bot.message_handler(commands=["admin"])
def admin_panel(msg):
    if msg.from_user.id == ADMIN_ID:
        bot.send_message(msg.chat.id, "⚙️ لوحة التحكم:", reply_markup=admin_menu())
    else:
        bot.send_message(msg.chat.id, "❌ مش مسموحلك بالأمر ده.")

# ============ تشغيل ============
bot.infinity_polling()
#╭───𓆩🛡️𓆪───╮
#     👨‍💻 𝘿𝙚𝙫: @S_S_F3  
#    📢 𝘾𝙝: @NSEIF
#سنكر لا تسرق
#تمت برمجة البوت بالكامل By Saif
#مش مسامح اي حد يخمط الملف بدون اذني
#Saif Hassan is Top