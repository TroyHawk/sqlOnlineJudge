

from typing import Dict, Any, Optional, List
from datetime import datetime
import aiomysql


class ExecutionResult:
    """执行结果类"""

    def __init__(self):
        self.success: bool = False
        self.error_message: Optional[str] = None
        self.result_set: List[Dict[str, Any]] = []
        self.execution_time: float = 0.0


class MySQLExecutor:
    def __init__(self, config: Dict[str, Any]):
        """
        初始化MySQL执行器
        config参数示例:
        {
            'DB_HOST': 'localhost',
            'DB_PORT': 3306,
            'DB_USER': 'your_user',
            'DB_PASSWORD': 'your_password',
            'DB_NAME': 'judge_db'
        }
        """
        self.config = config
        self.pool = None

    async def initialize(self):
        """初始化数据库连接池"""
        if not self.pool:
            self.pool = await aiomysql.create_pool(
                host=self.config['DB_HOST'],
                port=self.config['DB_PORT'],
                user=self.config['DB_USER'],
                password=self.config['DB_PASSWORD'],
                db=self.config['DB_NAME'],
                autocommit=False,
                maxsize=10,
                minsize=1,
                charset='utf8mb4'
            )

    async def execute_query(self, query: str, timeout: int = 30, need_validate = True) -> ExecutionResult:
        """
        执行SQL查询
        :param need_validate: 是否限制SQL种类为查询
        :param query: SQL查询语句
        :param timeout: 查询超时时间（秒）
        :return: ExecutionResult 对象
        """
        if need_validate and not self.validate_query(query):
            return ExecutionResult(
                success=False,
                error_message="Query contains forbidden keywords"
            )

        result = ExecutionResult()
        start_time = datetime.now()

        try:
            if not self.pool:
                await self.initialize()

            async with self.pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    try:
                        # 设置会话超时
                        await cursor.execute(f"SET SESSION MAX_EXECUTION_TIME={timeout * 1000}")

                        # 开启事务
                        await conn.begin()

                        # 执行查询
                        await cursor.execute(query)
                        rows = await cursor.fetchall()
                        result.result_set = [dict(row) for row in rows]

                        # 提交事务
                        await conn.commit()

                        result.success = True
                        result.execution_time = (datetime.now() - start_time).total_seconds()

                    except Exception as e:
                        await conn.rollback()
                        result.success = False
                        result.error_message = str(e)

        except Exception as e:
            result.success = False
            result.error_message = f"Database connection error: {str(e)}"

        return result

    def validate_query(self, query: str) -> bool:
        """
        验证SQL查询的安全性
        :param query: SQL查询语句
        :return: 是否是安全的查询
        """
        forbidden_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'INSERT', 'UPDATE']
        upper_query = query.upper()
        return not any(keyword in upper_query for keyword in forbidden_keywords)

    async def cleanup(self):
        """清理资源"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()