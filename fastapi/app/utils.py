import bcrypt

def hash_password(plain_password: str) -> str:
    # # 1. 將明文字串轉成 bytes
    # password_bytes = password.encode("utf-8")
    # # 2. 產生鹽（Salt）並進行雜湊
    # salt = bcrypt.gensalt()
    # hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    # # 3. 將結果轉回字串，方便存入資料庫
    # return hashed_bytes.decode("utf-8")   
    return bcrypt.hashpw(plain_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # 登入驗證時使用
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )