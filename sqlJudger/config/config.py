class Config:
    """系统配置类"""
    # 数据库配置
    DATABASE_URL = "mysql://root:lusini123@localhost:3306/student"

    # 判题相关配置
    MAX_EXECUTION_TIME = 30  # SQL执行最大时间(秒)
    MAX_MEMORY_USAGE = 512  # 内存使用限制(MB)
    SANDBOX_ENABLED = True  # 是否启用沙箱

    # API配置
    API_PREFIX = "/api/v1"
    JWT_SECRET_KEY = "your-secret-key"
    JWT_EXPIRE_MINUTES = 60


db_config = {
    'DATABASE_URL': "mysql://root:lusini123@localhost:3306/student",
    'USE_DOCKER': True,
    'MAX_MEMORY_MB': 512,
    'MAX_CPU_TIME': 30
}
