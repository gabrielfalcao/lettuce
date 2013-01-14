from splinter.browser import Browser
from lettuce import before, after, world


@before.harvest
def setup(server):
    world.browser = Browser()


@after.harvest
def cleanup(server):
    world.browser.quit()
