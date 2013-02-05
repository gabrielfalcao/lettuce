# -*- coding: utf-8 -*-
# <Lettuce - Behaviour Driven Development for python>
# Copyright (C) <2010-2012>  Gabriel Falcão <gabriel@nacaolivre.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lettuce import before, after


@before.all
def celeries_before_all():
    print "Celeries before all"


@after.all
def celeries_after_all(total):
    print "Celeries after all"


@before.harvest
def celeries_before_harvest(variables):
    print "Celeries before harvest"


@after.harvest
def celeries_after_harvest(results):
    print "Celeries after harvest"


@before.each_feature
def celeries_before_feature(feature):
    print "Celeries before feature '%s'" % feature.name


@after.each_feature
def celeries_after_feature(feature):
    print "Celeries after feature '%s'" % feature.name


@before.each_scenario
def celeries_before_scenario(scenario):
    print "Celeries before scenario '%s'" % scenario.name


@after.each_scenario
def celeries_after_scenario(scenario):
    print "Celeries after scenario '%s'" % scenario.name


@before.each_step
def celeries_before_step(step):
    print "Celeries before step '%s'" % step.sentence


@after.each_step
def celeries_after_step(step):
    print "Celeries after step '%s'" % step.sentence
