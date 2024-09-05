# tailx

带颜色的 `tail -f`，更好看的查看日志。

## 安装

```
pip install tailx
```

## 用例

```bash
tailx [文件路径] [-no] [--nocolor] [-n Num] [-f REGEX] [--filter REGEX] [-h] [--help] 
```
## 查看帮助

```bash
tailx -h
tailx --help
```

## 彩色输出（默认）

```bash
tailx path/to/file.log
```

## 无颜色输出

```bash
tailx path/to/file.log -no
tailx path/to/file.log --nocolor
```

## 修改默认行数

```bash
tailx path/to/file.log -n 10
```

## 修改默认行数

```bash
tailx path/to/file.log -n 10
```

## 过滤输出(支持正则)

```bash
tailx path/to/file.log -f "INFO"
tailx path/to/file.log --filter "SUCCESS"
```
