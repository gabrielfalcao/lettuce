---
layout: default
title: Installing
keywords: Installing
category: Introduction
description: Instructions to install lettuce in your computer, requires python and maybe git.
---

# Installing Lettuce

You can install the stable verstion lettuce through
[pip](http://pypi.python.org/pypi/pip) or install the development
version through [git](http://en.wikipedia.org/wiki/Git_(software))


## Stable version

```console
user@machine:~$ [sudo] pip install lettuce
```

## Development version

If you're a more adventurous developer, you can use the
bleeding edge version of Lettuce by taking the git HEAD

If you want so, you have basically 2 options:

### Build and install the egg from sources

Good for those that just want to use the latest features

```console
user@machine:~$ git clone git://github.com/gabrielfalcao/lettuce.git
user@machine:~$ cd lettuce
user@machine:~/lettuce$ python setup.py install
```

### Use the latest code to contribute with lettuce's codebase

If it is your case, I strongly recommend a sandbox:


#### 1. Fetch the code

```console
user@machine:~/Projects$ git clone git://github.com/gabrielfalcao/lettuce.git
```

#### 2. Add to your PYTHONPATH

```console
user@machine:~/Projects$ echo "export PYTHONPATH=$HOME/Projects/lettuce:$PYTHONPATH" >> $HOME/.bashrc
```

3. Open a new terminal and enjoy!
