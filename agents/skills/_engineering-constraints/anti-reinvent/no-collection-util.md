# 禁止自造集合工具

> Apache Commons Collections / Google Guava / Hutool 已覆盖 90% 场景。

## Java

**首选 Hutool**（集大成），其次 Guava，特定场景用 Apache Commons Collections：

```java
// ✅ 正确：用 Hutool
import cn.hutool.core.collection.CollUtil;
import cn.hutool.core.util.ObjectUtil;

boolean isEmpty = CollUtil.isEmpty(list);  // null-safe
List<String> filtered = CollUtil.filter(list, s -> s.startsWith("a"));
List<String> newList = CollUtil.distinct(list);

// ✅ 正确：用 Guava（不可变集合 / Multimap）
List<String> immutable = ImmutableList.of("a", "b");
Multimap<String, String> map = ArrayListMultimap.create();

// ✅ 正确：用 Apache Commons Collections
Collection<String> filtered = CollectionUtils.select(list, predicate);

// ❌ 错误：自造
public class ListUtil {
    public static boolean isEmpty(List<?> list) {
        return list == null || list.isEmpty();
    }
}
```

## Python

**首选内置 + itertools / functools**：

```python
# ✅ 正确：用标准库
from collections import Counter, defaultdict, OrderedDict
from itertools import chain, groupby
from functools import reduce, lru_cache

# 频次统计
counts = Counter(['a', 'b', 'a', 'c'])  # {'a': 2, 'b': 1, 'c': 1}

# 嵌套默认值
graph = defaultdict(list)
graph['a'].append('b')

# 缓存
@lru_cache(maxsize=128)
def expensive_func(x):
    return ...

# ✅ 正确：sortedcontainers 库
from sortedcontainers import SortedDict
sd = SortedDict({'a': 1, 'b': 2})

# ❌ 错误：自造
def my_count(items):
    result = {}
    for item in items:
        if item in result:
            result[item] += 1
        else:
            result[item] = 1
    return result  # 用 Counter 替代
```

## JavaScript / TypeScript

**首选 es-toolkit**（替代 lodash）：

```typescript
import { chunk, uniq, groupBy, debounce, throttle } from 'es-toolkit';

const chunks = chunk([1, 2, 3, 4, 5], 2);  // [[1,2], [3,4], [5]]
const unique = uniq([1, 2, 2, 3]);
const grouped = groupBy([1, 2, 3, 4], x => x % 2);
const debounced = debounce(() => console.log('hi'), 300);
```

## 反模式检测

- `class.*Util.*Collection`（自造工具类）
- 手写 `isEmpty`（用 Hutool / CollUtil / 框架自带）
- 手写 deep clone（用 Hutool / lodash.cloneDeep）
- 手写排序（用 `list.sort()`）
