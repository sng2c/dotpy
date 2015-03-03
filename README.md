# dotfiles

심플한 dotfiles 헬퍼.

# 기능

1. ~/dotfiles 디렉토리를 생성하고, 
1. attach한 파일들을 ~/dotfiles/ 안으로 옮기면서
1. 옮긴파일로의 심볼릭 링크를 원래자리에 만듭니다.
1. ~/dotfiles 디렉토리를 git으로 관리하면 됩니다.

# 제약 사항

* 이미 관리되고 있는 파일은 detach만 가능합니다.
* 관리되고 있지않은 심볼릭 링크는 attach만 가능합니다.
* recover는 존재하지 않는 심볼릭 링크를 복구할 때 사용합니다.
* 아직 출력이 구립니다.
* ~/ 에 있는 파일만 관리가 가능합니다.

```bash
$ python dotpy.py

usage: dotpy [-h] {status,attach,detach,recover} ...

dotfiles helper

optional arguments:
  -h, --help            show this help message and exit

Commands:
  {status,attach,detach,recover}
    status              show dotfiles
    attach              attach dotfiles to manage
    detach              detach dotfiles managing
    recover             recover missing symlinks
```
