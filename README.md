# dotpy

Simple dotfiles helper.

# Features

It

1. It makes ~/dotfiles directory,
1. It moves `attach`ed files into ~/dotfiles/
1. It makes symbolic links for the moved files onto original locations.
1. And, You can manage the files in ~/dotfiles using GIT manually.

# Limited

* Already managed dotfiles can be `detach`ed.
* Non-managed dotfiles can be `attach`ed.
* `recover` recovers only symbolic links which is not yet exists. 
* Not yet nice status-output.
* Only for dotfiles on ~/ directory.

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
# Thanks to contributors

* [@ujuc](https://github.com/sng2c/dotpy/commits?author=ujuc)

