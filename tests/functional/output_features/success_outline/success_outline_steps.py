from lettuce import step


@step(r'Given I open browser at "http://(.*)"')
def given_i_open_browser_at_http_address(step, address):
    pass


@step(r'And click on "sign[-]up"')
def and_click_on_sign_up(step):
    pass


@step(r'I fill the field "(.*)" with "(.*)"')
def when_i_fill_the_field_x_with_y(step, field, value):
    pass


@step(r'And I click "done"')
def and_i_click_done(step):
    pass


@step(r'I see the title of the page is "(.*)"')
def then_i_see_the_message_message(step, title):
    possible_titles = [
        u'John | My Website',
        u'Mary | My Website',
        u'Foo | My Website',
    ]

    assert title in possible_titles, (
        '"%s" should be between the options [%s]' % (title, ", ".join(possible_titles)))
