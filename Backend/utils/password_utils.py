import bcrypt


def hash_password(password: str) -> str:
    """
    对传入的密码进行哈希处理，并返回字符串格式的哈希值。
    """
    # 生成盐，并对密码进行哈希（返回值是字节类型）
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # 将字节类型转换为字符串存储到数据库中
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码与哈希密码是否匹配，返回 True 或 False。
    """
    # 将明文密码编码成字节类型，并将存储的哈希密码转换成字节类型进行验证
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


# 示例使用
if __name__ == "__main__":
    password = "mysecretpassword"
    hashed = hash_password(password)
    print("Hashed password:", hashed)

    # 验证密码是否匹配
    assert verify_password("mysecretpassword", hashed) == True
    assert verify_password("wrongpassword", hashed) == False
    print("Password verification passed.")
