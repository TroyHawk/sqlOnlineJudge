import asyncio
from sqlJudger.core.executor import MySQLExecutor

async def main():


    config = {
        'DB_HOST': 'localhost',
        'DB_PORT': 3306,
        'DB_USER': 'root',
        'DB_PASSWORD': 'lusini123',
        'DB_NAME': 'student'
    }

    # 创建执行器实例
    executor = MySQLExecutor(config)

    try:
        # 初始化连接池
        await executor.initialize()

        # 执行查询
        query = "SELECT * from blog;"
        result = await executor.execute_query(query, timeout=3000)

        # 处理结果
        if result.success:
            print(f"查询结果: {result.result_set}")
            print(f"执行时间: {result.execution_time}秒")
        else:
            print(f"查询错误: {result.error_message}")

    finally:
        # 清理资源
        await executor.cleanup()

asyncio.run(main())

