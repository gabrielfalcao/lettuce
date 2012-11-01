---
layout: default
title: Welcome
keywords: Introduction, Nutshell
description: Lettuce is a behavior-driven development framework for python based on Cucumber. It supports over 15 languages and integrates with Django really well.
---

# Lettuce in a nutshell

## 1 - install it

```console
user@machine:~$ [sudo] pip install lettuce
```

## 2 - describe your first feature

```ruby
Feature: Manipulate strings
  In order to have some fun
  As a programming beginner
  I want to manipulate strings

  Scenario: Uppercased strings
    Given I have the string "lettuce leaves"
    When I put it in upper case
    Then I see the string is "LETTUCE LEAVES"
```

## 3 - define its steps

```python
from lettuce import *

@step('I have the string "(.*)"')
def have_the_string(step, string):
    world.string = string

@step('I put it in upper case')
def put_it_in_upper(step):
    world.string = world.string.upper()

@step('I see the string is "(.*)"')
def see_the_string_is(step, expected):
    assert world.string == expected, \
        "Got %s" % world.string
```

## 4 - watch it pass

```console
user@machine:~/Projects/my-project$ lettuce features/
```
