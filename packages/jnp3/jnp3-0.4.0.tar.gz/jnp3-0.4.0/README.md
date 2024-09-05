# jnp3

一个 Python 语言的辅助工具集，用于记录个人感觉比较有用的辅助函数或者类。

> 名称中的 3 是指 python3，同时也是为了避免和已存在的包冲突。

## 安装

```sh
pip install jnp3
```

### 安装 pyside6 工具集

```shell
pip install jnp3[gui6]
```

如果要使用 *检查更新* 按钮

```shell
pip install jnp3[gui6-with-update]
```

### 安装 pyside2 工具集

pyside2 主要是为了兼容 MacOS 10.13，且因为 _检查更新_ 按钮在 MacOS 系统不会引起报毒，所以不单独排除

```shell
pip install jnp3[gui2]
```
