#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import step


def assert_in(dado, possibilidades):
    assert dado in possibilidades, \
        u"%r deveria estar nas possibilidades: %r" % (
        dado, possibilidades
    )

@step(u'tenho o (.*)')
def dado_que_tenho(step, grupo):
    possibilidades = [
        'algo',
        'outro',
        'dados'
    ]
    assert_in(grupo, possibilidades)

@step(u'faço algo com (.*)')
def faco_algo_com(step, grupo):
    possibilidades = [
        'assim',
        'aqui',
        u'funcionarão'
    ]
    assert_in(grupo, possibilidades)

@step(u'fico feliz em ver (.*)')
def fico_feliz_em_ver(step, grupo):
    possibilidades = [
        'funcional',
        u'também',
        'com unicode !'
    ]
    assert_in(grupo, possibilidades)
