import asyncio

from sqlJudger.core.executor import MySQLExecutor
from sqlJudger.core.judge import SQLJudger


async def judge_submission():
    # 配置数据库连接
    config = {
        'DB_HOST': 'localhost',
        'DB_PORT': 3306,
        'DB_USER': 'root',
        'DB_PASSWORD': 'lusini123',
        'DB_NAME': 'student'
    }

    # 创建执行器和判题器
    executor = MySQLExecutor(config)
    judger = SQLJudger(executor)

    # 定义测试用例
    test_cases = [
        {
            "id" : 1,
            "description": "基本查询测试",
            "init_sql":[
                "DROP TABLE if Exists users",
                "CREATE TABLE users (id INT, name VARCHAR(50), age INT)",
                "INSERT INTO users VALUES (1, 'Alice', 21), (2, 'Bob', 25)"
            ],
            "answer_sql":"SELECT * FROM users WHERE age > 20",
            "score":10
        },
        {
            "id":2,
            "description":"聚合函数测试",
            "init_sql":[
                "DROP TABLE if Exists orders",
                "CREATE TABLE orders (id INT, amount DECIMAL(10,2))",
                "INSERT INTO orders VALUES (1, 100.50), (2, 200.75)"
             ],
            "answer_sql":"SELECT SUM(amount) as total FROM orders",
            "score":15
        }
    ]

    try:
        # 初始化数据库连接
        await executor.initialize()

        # 评判用户提交的SQL
        user_sql = "SELECT * FROM users WHERE age > 20"
        result = await judger.judge(user_sql, test_cases)

        # 输出结果
        if result.success:
            print(f"通过所有测试用例！")
            print(f"得分: {result.score}/{result.total_score}")
            print(f"执行时间: {result.execution_time}秒")
        else:
            print("未通过所有测试用例")
            for case_result in result.test_case_results:
                print(case_result)
                if not case_result['success']:
                    print(f"测试用例 {case_result['test_case_id']} 失败:")
                    print(f"错误信息: {case_result['error_message']}")
                    print(f"你的答案：{case_result['user_result']}")
                    print(f"正确答案: {case_result['expected_result']}")
                else:
                    print(f"答案正确，测试用例 {case_result['test_case_id']} 通过:")
                    print(f"正确答案: {case_result['expected_result']}")

    finally:
        await executor.cleanup()

# 运行
asyncio.run(judge_submission())