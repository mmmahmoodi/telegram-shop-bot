import aiosqlite
from config import DB_PATH


async def init_db():
    """ساخت جداول دیتابیس در اولین اجرا"""
    async with aiosqlite.connect(DB_PATH) as db:
        # جدول کاربران
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                balance REAL DEFAULT 0.0,
                referral_code TEXT UNIQUE,
                referred_by INTEGER DEFAULT NULL,
                is_banned INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # جدول دسته‌بندی محصولات
        await db.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)

        # جدول محصولات
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                is_active INTEGER DEFAULT 1,
                FOREIGN KEY (category_id) REFERENCES categories(id)
            )
        """)

        # جدول موجودی کدها (برای تحویل خودکار)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS product_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                code TEXT NOT NULL,
                is_used INTEGER DEFAULT 0,
                used_by INTEGER DEFAULT NULL,
                used_at TIMESTAMP DEFAULT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # جدول سفارشات
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER,
                amount REAL,
                status TEXT DEFAULT 'pending',
                delivered_code TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)

        # جدول تراکنش‌های مالی
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                type TEXT,
                status TEXT DEFAULT 'pending',
                receipt_photo TEXT DEFAULT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        # جدول تیکت‌ها
        await db.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message TEXT,
                admin_reply TEXT DEFAULT NULL,
                is_closed INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

        await db.commit()


async def add_user(user_id: int, username: str, first_name: str):
    """ثبت کاربر جدید (اگر قبلاً ثبت نشده باشه)"""
    import uuid
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT user_id FROM users WHERE user_id = ?", (user_id,)
        )
        if not await cursor.fetchone():
            referral_code = str(uuid.uuid4())[:8]
            await db.execute(
                "INSERT INTO users (user_id, username, first_name, referral_code) VALUES (?, ?, ?, ?)",
                (user_id, username, first_name, referral_code)
            )
            await db.commit()


async def get_user(user_id: int):
    """دریافت اطلاعات کاربر"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM users WHERE user_id = ?", (user_id,)
        )
        return await cursor.fetchone()
