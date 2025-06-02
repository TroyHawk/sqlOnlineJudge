from dataclasses import dataclass
from typing import List


@dataclass
class TestCase:
    """测试用例类"""
    id: int
    description: str
    init_sql: List[str]  # 初始化数据的SQL语句
    answer_sql: str  # 标准答案SQL
    score: int  # 测试用例分数




    