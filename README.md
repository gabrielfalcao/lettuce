# lettuce
> Version 0.1 - barium

## On release names

Lettuce release names will be inspired by any green stuff.

Barium: In form of "barium nitrate" is commonly used to make green fireworks. Such a good name for a first version :)

# What

Lettuce is a BDD tool for python, 100% inspired on [cucumber](http://cukes.info/ "BDD with elegance and joy").

# Motivation

1. [Cucumber](http://cukes.info/) makes [Ruby](http://www.ruby-lang.org/) even more sexy. Python needed something like it.
2. Testing must be funny and easy.
3. Most python developers code in python, not ruby.
4. Ruby has Capistrano, Python has Fabric. Ruby has cucumber, Python has lettuce.
5. I personally don't like mixing many languages in small projects. Keeping all in python is better.
6. I love python, and ever did. But I also ever missed something that make writing tests easier and funnier.
7. I like [nose](http://code.google.com/p/python-nose/), which is a unittest pythonic framework. However, as the project I work on grows, so do the tests, and it becomes harder to understand them.
8. [lettuce ladies](http://www.lettuceladies.com/) :)

# Dependencies

**you will need to install these dependencies in order to** *hack* **lettuce** :)
all them are used within lettuce tests

* [nose](http://code.google.com/p/python-nose/)
    > [sudo] pip install nose
* [mox](http://code.google.com/p/pymox/)
    > [sudo] pip install mox
* [sphinx](http://sphinx.pocoo.org/)
    > [sudo] pip install sphinx
* [lxml](http://codespeak.net/lxml/)
    > [sudo] pip install lxml
* [django](http://djangoproject.com/)
    > [sudo] pip install django

# Contributing

1. fork and clone the project
2. install the dependencies above
3. run the tests with make:
    > make unit functional integration doctest
4. hack at will
5. commit, push etc
6. send a pull request

# Special thanks

1. [Cucumber](http://cukes.info/) crew, for creating such a AWESOME project, and for inspiring [Lettuce](http://lettuce.it/).
2. [Tatiana](http://github.com/tatiana) for helping a lot with documentation.
3. [Django](http://djangoproject.com) which documentation structure was borrowed.
