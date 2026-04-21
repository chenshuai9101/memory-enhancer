#!/usr/bin/env python3
"""
Memory-Enhancer Coze集成脚本
用于扣子平台的记忆管理功能实现
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any


class MemoryStore:
    """记忆存储引擎"""
    
    def __init__(self):
        self.memory_db = {}  # 内存存储，模拟数据库
        self.user_profile = {}  # 用户画像存储
        
    def store(self, content: str, importance: int = 5, 
              category: str = "context", ttl: int = 86400) -> Dict:
        """存储记忆"""
        memory_id = f"mem_{int(time.time() * 1000)}"
        memory = {
            "id": memory_id,
            "content": content,
            "importance": importance,
            "category": category,
            "created_at": datetime.now().isoformat(),
            "expires_at": (datetime.now() + timedelta(seconds=ttl)).isoformat(),
            "access_count": 0,
            "last_access": datetime.now().isoformat()
        }
        self.memory_db[memory_id] = memory
        return {"success": True, "memory_id": memory_id}
    
    def retrieve(self, query: str, intent: str = "general", 
                 limit: int = 10, filters: Dict = None) -> List[Dict]:
        """检索记忆"""
        results = []
        now = datetime.now()
        
        for mem_id, memory in self.memory_db.items():
            # 检查是否过期
            expires = datetime.fromisoformat(memory["expires_at"])
            if expires < now:
                continue
                
            # 简单相似度计算
            score = self._calculate_relevance(query, memory["content"])
            
            # 意图过滤
            if filters and "category" in filters:
                if memory["category"] != filters["category"]:
                    continue
            
            if score > 0.3:  # 相似度阈值
                results.append({
                    **memory,
                    "relevance": score
                })
        
        # 按相关性和重要性排序
        results.sort(key=lambda x: (x["relevance"], x["importance"]), reverse=True)
        return results[:limit]
    
    def clean(self, threshold: int = 3) -> Dict:
        """清理低价值记忆"""
        now = datetime.now()
        removed = []
        
        for mem_id in list(self.memory_db.keys()):
            memory = self.memory_db[mem_id]
            
            # 检查是否过期或评分过低
            expires = datetime.fromisoformat(memory["expires_at"])
            if expires < now or memory["importance"] < threshold:
                del self.memory_db[mem_id]
                removed.append(mem_id)
        
        return {"success": True, "removed_count": len(removed)}
    
    def _calculate_relevance(self, query: str, content: str) -> float:
        """计算查询与记忆的相关性"""
        query_words = set(query.lower().split())
        content_words = set(content.lower().split())
        
        if not query_words:
            return 0.0
            
        intersection = query_words & content_words
        return len(intersection) / len(query_words)


class IntentRecognizer:
    """意图识别器"""
    
    INTENT_PATTERNS = {
        "fact": ["是什么", "谁在", "多少", "什么时候", "定义", "概念"],
        "preference": ["喜欢", "偏好", "习惯", "风格", "想要", "讨厌"],
        "context": ["之前", "刚才", "继续", "还有", "之前说"],
        "tool_call": ["调用", "执行", "运行", "操作"]
    }
    
    def recognize(self, query: str) -> str:
        """识别查询意图"""
        query_lower = query.lower()
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            for pattern in patterns:
                if pattern in query_lower:
                    return intent
        return "general"


class ImportanceEvaluator:
    """重要性评估器"""
    
    HIGH_IMPORTANCE_KEYWORDS = [
        "重要", "必须", "紧急", "记住", "关键", "核心",
        "偏好", "喜欢", "讨厌", "原则", "规则"
    ]
    
    LOW_IMPORTANCE_KEYWORDS = [
        "随便", "无所谓", "临时", "试试", "可能"
    ]
    
    def evaluate(self, content: str, context: Dict = None) -> int:
        """评估内容重要性"""
        score = 5  # 默认分数
        content_lower = content.lower()
        
        # 检查关键词
        for keyword in self.HIGH_IMPORTANCE_KEYWORDS:
            if keyword in content_lower:
                score += 1
                
        for keyword in self.LOW_IMPORTANCE_KEYWORDS:
            if keyword in content_lower:
                score -= 1
        
        # 检查内容长度
        if len(content) > 100:
            score += 1
        elif len(content) < 20:
            score -= 1
        
        return max(1, min(10, score))


# 全局实例
memory_store = MemoryStore()
intent_recognizer = IntentRecognizer()
importance_evaluator = ImportanceEvaluator()


# ============== 对外API接口 ==============

def memory_store_api(content: str, importance: int = None, 
                     category: str = "context", ttl: int = 86400) -> Dict:
    """存储记忆API"""
    # 自动评估重要性
    if importance is None:
        importance = importance_evaluator.evaluate(content)
    
    return memory_store.store(content, importance, category, ttl)


def memory_retrieve_api(query: str, intent: str = None, 
                        limit: int = 10, category: str = None) -> List[Dict]:
    """检索记忆API"""
    # 自动识别意图
    if intent is None:
        intent = intent_recognizer.recognize(query)
    
    filters = {"category": category} if category else None
    return memory_store.retrieve(query, intent, limit, filters)


def memory_clean_api(threshold: int = 3) -> Dict:
    """清理记忆API"""
    return memory_store.clean(threshold)


def memory_summarize(conversation: List[Dict], max_length: int = 500) -> str:
    """对话摘要"""
    # 简单实现：取前N条关键信息
    summary_parts = []
    current_length = 0
    
    for msg in conversation:
        content = msg.get("content", "")
        if current_length + len(content) > max_length:
            break
        summary_parts.append(content)
        current_length += len(content)
    
    return " | ".join(summary_parts)


if __name__ == "__main__":
    # 测试示例
    print("=== Memory-Enhancer 测试 ===\n")
    
    # 存储记忆
    result = memory_store_api(
        "用户喜欢简洁的回复风格，不要太长",
        category="preference",
        ttl=604800  # 7天
    )
    print(f"存储结果: {result}")
    
    # 检索记忆
    results = memory_retrieve_api("用户的回复风格是什么")
    print(f"\n检索结果: {results}")
    
    # 意图识别
    intent = intent_recognizer.recognize("我之前说了什么")
    print(f"\n识别意图: {intent}")
