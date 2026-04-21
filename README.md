# Memory-Enhancer 使用指南

## 快速开始

### 1. 安装
```bash
# 克隆仓库
git clone https://github.com/chenshuai9101/memory-enhancer.git

# 进入目录
cd memory-enhancer

# 安装依赖
pip install -r requirements.txt
```

### 2. 基本使用

```python
from memory_engine import memory_store_api, memory_retrieve_api, memory_clean_api

# 存储记忆
memory_store_api(
    content="用户喜欢简洁的回答",
    category="preference",
    ttl=604800  # 7天
)

# 检索记忆
results = memory_retrieve_api(
    query="用户的回复风格",
    intent="preference"
)

# 清理低价值记忆
memory_clean_api(threshold=3)
```

### 3. Coze平台集成

参见 `scripts/coze_integration.py` 中的集成示例。

## API参考

### memory_store_api
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| content | str | 是 | 记忆内容 |
| importance | int | 否 | 重要性评分(1-10) |
| category | str | 否 | 分类标签 |
| ttl | int | 否 | 生存时间(秒) |

### memory_retrieve_api
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | str | 是 | 查询内容 |
| intent | str | 否 | 查询意图 |
| limit | int | 否 | 返回数量 |

### memory_clean_api
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| threshold | int | 否 | 清理阈值 |

## 验收标准

| 指标 | 目标值 | 当前值 |
|------|--------|--------|
| 注入延迟 | <200ms | ✅ |
| 检索延迟 | <300ms | ✅ |
| Token节省 | >50% | ✅ |
| 提取准确率 | >85% | ✅ |
| 偏好识别准确率 | >90% | ✅ |
