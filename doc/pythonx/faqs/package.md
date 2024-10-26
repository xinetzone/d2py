# Python 包安装

## No module named "Crypto"

参考：[解释Crypto模块怎么就这么"皮"？No module named "Crypto"](https://www.cnblogs.com/fawaikuangtu123/p/9761943.html)

1. `pycrypto`、`pycrytodome` 和 `crypto` 是一个东西，`crypto` 在 python 上面的名字是 `pycrypto`，它是一个第三方库，但是已经停止更新三年了，所以不建议安装这个库；
2. 正确的安装方法：

    ```bash
    pip install pycryptodome
    ```
