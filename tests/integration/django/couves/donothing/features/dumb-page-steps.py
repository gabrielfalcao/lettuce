from lettuce import step

@step(r'Given I navigate to "(.*)"')
def given_i_navigate_to_group1(step, group1):
    pass
@step(r'Then I see the title of the page is "(.*)"')
def then_i_see_the_title_of_the_page_is_group1(step, group1):
    pass
@step(r'When I look inside de 1st paragraph')
def when_i_look_inside_de_1st_paragraph(step):
    pass
@step(r'Then I see it has no attributes')
def then_i_see_it_has_no_attributes(step):
    pass
@step(r'And that its content is "(.*)"')
def and_that_its_content_is_group1(step, group1):
    pass
@step(r'When I look inside de 1st header')
def when_i_look_inside_de_1st_header(step):
    pass
@step(r'Then I see its content is "(.*)"')
def then_i_see_its_content_is_group1(step, group1):
    pass
@step(r'And that its id is "(.*)"')
def and_that_its_id_is_group1(step, group1):
    pass
