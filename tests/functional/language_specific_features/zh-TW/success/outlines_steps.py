#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import step


def assert_in(condition, possibilities):
    assert condition in possibilities, \
        u"%r 應該包含在: %r" % (
        condition, possibilities
    )

@step(u'輸入是(.*)')
def shu_ru(step, group):
    possibilities = [
        u'什麽',
        u'其他',
        u'數據'
    ]
    assert_in(group, possibilities)

@step(u'執行(.*)時')
def zhi_xing(step, group):
    possibilities = [
        u'這個',
        u'這裏',
        u'動作'
    ]
    assert_in(group, possibilities)

@step(u'得到(.*)')
def de_dao(step, group):
    possibilities = [
        u'功能',
        u'一樣',
        u'unicode輸出!'
    ]
    assert_in(group, possibilities)
