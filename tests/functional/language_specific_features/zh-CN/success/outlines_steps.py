#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import step


def assert_in(condition, possibilities):
    assert condition in possibilities, \
        u"%r 应该包含在: %r" % (
        condition, possibilities
    )

@step(u'输入是(.*)')
def shu_ru(step, group):
    possibilities = [
        u'什么',
        u'其他',
        u'数据'
    ]
    assert_in(group, possibilities)

@step(u'执行(.*)时')
def zhi_xing(step, group):
    possibilities = [
        u'这个',
        u'这里',
        u'动作'
    ]
    assert_in(group, possibilities)

@step(u'得到(.*)')
def de_dao(step, group):
    possibilities = [
        u'功能',
        u'一样',
        u'unicode输出!'
    ]
    assert_in(group, possibilities)
