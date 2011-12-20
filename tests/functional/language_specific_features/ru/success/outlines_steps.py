#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lettuce import step

def assert_in(text, variants):
    assert text in variants, \
        u"вариант %r не должен был тестироватся, только: %r" % (
        text, variants
    )

@step(u'я открываю в браузере  "([^"]*)"')
def otkrivayu_v_brauzere(step, url):
    pass

@step(u'я заполняю в поле "Имя" "([^"]*)"')
def zapolnyau_imya(step, name):
    names=[
        u"Виталий Игоревич",
        u"Марина Банраул",
    ]
    assert_in(name, names)

@step(u'я заполняю в поле "Email" "([^"]*)"')
def zapolnyau_email(step, email):
    emails=[
        "john@gmail.org",
        "mary@email.com",
    ]
    assert_in(email, emails)

@step(u'я заполняю в поле "Сообщение" "([^"]*)"')
def zapolnyau_soobchenie(step, message):
    messages=[
        u"Есть интересный проект, нужно обсудить",
        u"Мне нравятся ваши дизайны, хочу сайт",
    ]
    assert_in(message, messages)

@step(u'я нажимаю "Отправить"')
def najimayu_otparavit(step):
    pass
@step(u'я получаю сообщение "Спасибо за ваше сообщение"')
def poluchayu_soopschenie(step):
    pass


