```{post} 2024/09/25 08:00
:category: pandas
:tags: FAQs
:excerpt: 1
```
# `pandas` 常见问题

## 美化 `pandas` 打印

```python
import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('expand_frame_repr', False) # 输出数据宽度超过设置宽度时，是否要折叠
pd.set_option('display.max_colwidth', None)
pd.set_option('display.precision', 5)
```
