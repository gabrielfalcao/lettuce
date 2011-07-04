#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import step


def assert_in(condition, possibilities):
    assert condition in possibilities, \
        u"%r は次のリストに入っている可能性がある: %r" % (
        condition, possibilities
    )

@step(u'入力値を (.*) とし')
def dado_que_tenho(step, group):
    possibilities = [
        u'何か',
        u'その他',
        u'データ'
    ]
    assert_in(group, possibilities)

@step(u'処理 (.*) を使って')
def faco_algo_com(step, group):
    possibilities = [
        u'これ',
        u'ここ',
        u'動く'
    ]
    assert_in(group, possibilities)

@step(u'表示は (.*) である')
def fico_feliz_em_ver(step, group):
    possibilities = [
        u'機能',
        u'同じ',
        u'unicodeで!'
    ]
    assert_in(group, possibilities)
