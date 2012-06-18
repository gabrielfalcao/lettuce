#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import step


def assert_in(dado, possibilidades):
    assert dado in possibilidades, \
        u"%r deveria estar nas possibilidades: %r" % (
        dado, possibilidades
    )

@step(u'un après midi de (.*)')
def un_apres_midi(step, groupe):
    possibilites = [
        u'janvier',
        u'aôut',
        u'octobre'
    ]
    assert_in(groupe, possibilites)

@step(u'je veux faire la sieste')
def je_veux_dormir(step):
	pass

@step(u'je peux aller (.*)')
def lieux_de_sieste(step, groupe):
    possibilites = [
        u'près de la cheminé',
        u'dans le transat',
        u'dans le canapé'
    ]
    assert_in(groupe, possibilites)

@step(u'fico feliz em ver (.*)')
def fico_feliz_em_ver(step, grupo):
    possibilidades = [
        'funcional',
        u'também',
        'com unicode !'
    ]
    assert_in(grupo, possibilidades)
