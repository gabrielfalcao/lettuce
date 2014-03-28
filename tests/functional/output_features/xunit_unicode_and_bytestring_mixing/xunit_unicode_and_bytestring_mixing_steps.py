# -*- coding: utf-8 -*-
from lettuce import step

@step(u'Non ascii characters "(.*)" in outline')
def non_ascii_characters_in_outline(step, first):
    assert True


@step(u'Non ascii characters "(.*)" in step')
def define_nonascii_chars(step, word):
    assert True


@step(u'Non ascii characters "(.*)" in exception')
def raise_nonascii_chars(step, word):
    raise Exception(word)
