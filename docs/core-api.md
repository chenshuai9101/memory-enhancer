# Memory-Enhancer 核心脚本

## 功能说明
本脚本提供智能记忆管理的核心API实现。

## API 列表

### 1. memory_store - 存储记忆
```python
def memory_store(content: str, importance_score: int = 5, category: str = "context", ttl: int = 86400):
    """
    存储记忆到指定存储层
    
    Args:
        content: 记忆内容
        importance_score: 重要性评分(1-10)，默认5
        category: 记忆分类(事实/偏好/上下文/工具调用)
        ttl: 生存时间(秒)，默认86400(24小时)
    """
    pass
```

### 2. memory_retrieve - 检索记忆
```python
def memory_retrieve(query: str, intent: str = "general", limit: int = 10):
    """
    检索相关记忆
    
    Args:
        query: 查询内容
        intent: 查询意图(事实查询/偏好查询/上下文补全)
        limit: 返回数量限制
    """
    pass
```

### 3. memory_clean - 清理记忆
```python
def memory_clean(threshold: int = 3):
    """
    清理低价值记忆
    
    Args:
        threshold: 重要性阈值，低于此值的记忆将被归档
    """
    pass
```

### 4. importance_evaluate - 重要性评估
```python
def importance_evaluate(content: str, context: dict = None) -> int:
    """
    LLM自动评估内容重要性
    
    Args:
        content: 待评估内容
        context: 上下文信息
    Returns:
        重要性评分(1-10)
    """
    # 评分规则:
    # 1-3: 临时信息，可遗忘
    # 4-6: 一般信息，标准保留
    # 7-10: 重要信息，长期保留
    pass
```

### 5. intent_recognize - 意图识别
```python
def intent_recognize(query: str) -> str:
    """
    识别查询意图
    
    Args:
        query: 用户查询
    Returns:
        意图类型: fact/preference/context/general
    """
    pass
```

## 记忆分类
- `fact`: 事实性信息（日期、数字、定义）
- `preference`: 用户偏好（风格、口味、习惯）
- `context`: 对话上下文（当前任务、讨论主题）
- `tool_call`: 工具调用记录（API调用、命令执行）
