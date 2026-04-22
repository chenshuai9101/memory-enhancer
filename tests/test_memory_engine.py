#!/usr/bin/env python3
"""
Memory-Enhancer 测试用例
验证记忆存储、检索、清理功能
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from scripts.memory_engine import (
    memory_store_api, 
    memory_retrieve_api, 
    memory_clean_api,
    IntentRecognizer,
    ImportanceEvaluator,
    MemoryStore
)

def test_memory_store():
    """测试记忆存储"""
    print("=== 测试: 记忆存储 ===")
    
    # 测试基本存储
    result = memory_store_api(
        content="用户喜欢简洁的回复风格",
        category="preference",
        ttl=3600
    )
    assert result["success"] == True
    assert "memory_id" in result
    print(f"✅ 基本存储成功: {result['memory_id']}")
    
    # 测试重要性评估
    result2 = memory_store_api(
        content="这个信息非常重要，必须记住",
        category="fact"
    )
    assert result2["success"] == True
    print(f"✅ 高重要性评估成功")
    
    return True

def test_memory_retrieve():
    """测试记忆检索"""
    print("\n=== 测试: 记忆检索 ===")
    
    # 先存储测试数据
    memory_store_api("用户住在深圳", category="fact")
    memory_store_api("用户喜欢编程", category="preference")
    memory_store_api("用户正在做Python项目", category="context")
    
    # 测试关键词检索
    results = memory_retrieve_api("深圳")
    assert len(results) >= 1
    print(f"✅ 关键词检索成功，找到 {len(results)} 条结果")
    
    # 测试意图识别检索
    results = memory_retrieve_api("用户喜欢什么")
    print(f"✅ 意图识别检索成功，找到 {len(results)} 条结果")
    
    return True

def test_intent_recognition():
    """测试意图识别"""
    print("\n=== 测试: 意图识别 ===")
    
    recognizer = IntentRecognizer()
    
    test_cases = [
        ("用户喜欢什么风格", "preference"),
        ("之前讨论的内容", "context"),
        ("什么是机器学习", "fact"),
    ]
    
    for query, _ in test_cases:
        result = recognizer.recognize(query)
        print(f"  查询: '{query}' -> 意图: {result}")
    
    print("✅ 意图识别功能正常")
    return True

def test_importance_evaluation():
    """测试重要性评估"""
    print("\n=== 测试: 重要性评估 ===")
    
    evaluator = ImportanceEvaluator()
    
    test_cases = [
        ("这个信息非常重要，必须记住", 5),
        ("随便说说", 3),
        ("这是一段很长的详细描述内容，包含了很多具体的细节和例子说明", 6),
    ]
    
    for content, min_score in test_cases:
        score = evaluator.evaluate(content)
        print(f"  内容评分: {score}")
        assert score >= min_score
    
    print("✅ 重要性评估功能正常")
    return True

def test_memory_clean():
    """测试记忆清理"""
    print("\n=== 测试: 记忆清理 ===")
    
    memory_store_api("临时测试记忆", category="context", importance=1)
    result = memory_clean_api(threshold=5)
    assert result["success"] == True
    print(f"✅ 清理成功，移除了 {result['removed_count']} 条记忆")
    
    return True

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Memory-Enhancer 测试套件")
    print("=" * 50)
    
    tests = [
        test_memory_store,
        test_memory_retrieve,
        test_intent_recognition,
        test_importance_evaluation,
        test_memory_clean,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 50)
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
