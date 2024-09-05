import sys
import time
import re
from rich import print as print_rich
from rich.panel import Panel


def tail_f(filepath, n=5, *, nocolor=False, filter=None):
    """
    【彩色版】tail -f

    filepath: 文件路径
    n: 默认展示行数
    color: 是否使用颜色，默认为 true
    filter: 过滤关键字, 支持正则表达式
    """
    with open(filepath, "rb") as file:
        for _ in range(10):
            try:
                size = file.seek(0, 2)
                if size > 1000 * n:
                    offset = -1000 * n
                    file.seek(offset, 2)
                    lines = file.readlines()[1:]
                else:
                    file.seek(0, 0)
                    lines = file.readlines()
                for line in lines[-n:]:
                    line = line.decode()
                    if filter and not re.findall(filter, line):
                        continue
                    if not nocolor:
                        line = (
                            line.replace("INFO", "[bold]INFO[/]")
                            .replace("SUCCESS", "[green bold]SUCCESS[/]")
                            .replace("ERROR", "[red bold]ERROR[/]")
                            .replace("CRITICAL", "[white on red bold]CRITICAL[/]")
                            .replace("WARNING", "[khaki1 bold]WARNING[/]")
                            .replace("DEBUG", "[dodger_blue1 bold]DEBUG[/]")
                        )
                        print_rich(line, end="")
                    else:
                        print(line, end="")
                break
            except Exception:
                continue
        while True:
            try:
                line = file.readline()
                if not line:
                    time.sleep(0.5)
                    continue
                line = line.decode()
                if filter and not re.findall(filter, line):
                    continue
                if not nocolor:
                    line = (
                        line.replace("INFO", "[bold]INFO[/]")
                        .replace("SUCCESS", "[green bold]SUCCESS[/]")
                        .replace("ERROR", "[red bold]ERROR[/]")
                        .replace("CRITICAL", "[white on red bold]CRITICAL[/]")
                        .replace("WARNING", "[khaki1 bold]WARNING[/]")
                        .replace("DEBUG", "[dodger_blue1 bold]DEBUG[/]")
                    )
                    print_rich(line, end="")
                else:
                    print(line, end="")
            except KeyboardInterrupt:
                break


def main():
    args = sys.argv
    if "--nocolor" in args:
        nocolor = True
        args.remove("--nocolor")
    elif "-no" in args:
        nocolor = True
        args.remove("-no")
    else:
        nocolor = False
    if "-n" in args:
        n = int(args[args.index("-n") + 1])
        args.remove("-n")
        args.remove(str(n))
    else:
        n = 5
    if "-f" in args:
        filter = args[args.index("-f") + 1]
        args.remove("-f")
        args.remove(filter)
    elif "--filter" in args:
        filter = args[args.index("--filter") + 1]
        args.remove("--filter")
        args.remove(filter)
    else:
        filter = None
    filepath = args[1] if len(args) > 1 else None

    help_string = """[b red]【tailx】(彩色版 tail -f)[/] 0.1.5

用例: tailx [FILEPATH] [-h] [--nocolor] [-n NUM] [-f REGEX] [--filter REGEX]

参数:
  
  [green]FILEPATH[/]              文件路径
  [green]-no --nocolor[/]         关闭颜色
  [green]-h, --help[/]            帮助信息
  [green]-n NUM[/]                默认行数
  [green]-f REGEX[/]              过滤关键字, 支持正则表达式
  [green]--filter REGEX[/]        过滤关键字, 支持正则表达式
  """
    if filepath is None or "--help" in args or "-h" in args:
        print_rich(Panel(help_string, expand=False))
    else:
        tail_f(filepath, n=n, nocolor=nocolor, filter=filter)
        print()
