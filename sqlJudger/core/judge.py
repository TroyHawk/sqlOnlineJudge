from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from .executor import MySQLExecutor


@dataclass
class JudgeResult:
    """判题结果类"""
    success: bool
    score: int
    total_score: int
    execution_time: float
    error_message: Optional[str]
    test_case_results: List[Dict[str, Any]]


class SQLJudger:
    def __init__(self, executor: MySQLExecutor):
        self.executor = executor

    async def judge(self, user_sql: str, test_cases: List[Dict]) -> Dict:
        """
        评判用户的SQL查询
        :param user_sql: 用户提交的SQL
        :param test_cases: 测试用例列表
            {   id: int
                description: str
                init_sql: List[str]  # 初始化数据的SQL语句
                answer_sql: str  # 标准答案SQL
                score: int  # 测试用例分数
            }
        """
        start_time = datetime.now()
        total_score = sum(case["score"] for case in test_cases)
        earned_score = 0
        test_results = []

        for case in test_cases:
            case_result = await self._judge_test_case(user_sql, case)
            test_results.append(case_result)

            if case_result['success']:
                earned_score += case["score"]

        execution_time = (datetime.now() - start_time).total_seconds()

        return {
            "success":all(result['success'] for result in test_results),
            "score":earned_score,
            "total_score":total_score,
            "execution_time":execution_time,
            "error_message":None,
            "test_case_results":test_results
        }

    async def _judge_test_case(self, user_sql: str, case: Dict) -> Dict[str, Any]:
        """
        评判单个测试用例
        :param user_sql: 用户的SQL查询
        :param case: 测试用例
        :return: 测试用例的评判结果
        """

        # 初始化测试数据
        try:
            await self._initialize_test_data(case["init_sql"])
        except Exception as e:
            return {
                'test_case_id': case["id"],
                'success': False,
                'error_message': f"Failed to initialize test data: {str(e)}",
                'execution_time': 0
            }

        # 执行标准答案SQL
        expected_result = await self.executor.execute_query(case["answer_sql"])
        if not expected_result.success:
            return {
                'test_case_id': case["id"],
                'success': False,
                'error_message': f"Standard answer execution failed: {expected_result.error_message}",
                'execution_time': 0
            }

        # 执行用户SQL
        user_result = await self.executor.execute_query(user_sql)
        if not user_result.success:
            return {
                'test_case_id': case["id"],
                'success': False,
                'error_message': f"User query execution failed: {user_result.error_message}",
                'execution_time': user_result.execution_time
            }

        # 比对结果
        is_correct = self._compare_results(
            expected_result.result_set,
            user_result.result_set
        )

        return {
            'test_case_id': case["id"],
            'success': is_correct,
            'execution_time': user_result.execution_time,
            'error_message': None if is_correct else "Result does not match expected output",
            "user_result": user_result.result_set,
            "expected_result": expected_result.result_set
        }

    async def _initialize_test_data(self, init_sql_list: List[str]):
        """
        初始化测试数据
        :param init_sql_list: 初始化SQL语句列表
        """
        for sql in init_sql_list:
            result = await self.executor.execute_query(sql, need_validate=False)
            if not result.success:
                raise Exception(f"Failed to execute init SQL: {result.error_message}")

    def _compare_results(self, expected: List[Dict], actual: List[Dict]) -> bool:
        """
        比对查询结果
        :param expected: 期望的结果集
        :param actual: 实际的结果集
        :return: 是否匹配
        """
        if len(expected) != len(actual):
            return False

        # 对结果集进行排序以确保顺序无关性
        expected_sorted = sorted(expected, key=lambda x: str(x))
        actual_sorted = sorted(actual, key=lambda x: str(x))

        # 逐行比对
        return all(
            self._compare_rows(exp_row, act_row)
            for exp_row, act_row in zip(expected_sorted, actual_sorted)
        )

    def _compare_rows(self, expected_row: Dict, actual_row: Dict) -> bool:
        """
        比对单行结果
        :param expected_row: 期望的行数据
        :param actual_row: 实际的行数据
        :return: 是否匹配
        """
        # 检查列是否相同
        if set(expected_row.keys()) != set(actual_row.keys()):
            return False

        # 比对每个列的值
        for key in expected_row:
            exp_val = expected_row[key]
            act_val = actual_row[key]

            # 处理数值类型的精度问题
            if isinstance(exp_val, (float, int)) and isinstance(act_val, (float, int)):
                if abs(float(exp_val) - float(act_val)) > 1e-6:
                    return False
            elif exp_val != act_val:
                return False

        return True
