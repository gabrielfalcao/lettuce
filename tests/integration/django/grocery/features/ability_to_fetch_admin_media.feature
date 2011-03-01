Feature: fetch admin media from lettuce + django builtin server
  Scenario: Running on port 7000
    Given my settings.py has "LETTUCE_SERVER_PORT" set to "7000"
    Then I see that requesting "http://localhost:7000/media/css/base.css" gets "200"

  Scenario: Fetching CSS files:
    Given I fetch the urls:
      | url                        |
      | /media/css/base.css        |
      | /media/css/changelists.css |
      | /media/css/dashboard.css   |
      | /media/css/forms.css       |
      | /media/css/ie.css          |
      | /media/css/login.css       |
      | /media/css/rtl.css         |
      | /media/css/widgets.css     |
    When all the responses have status code 200
    Then all the responses have mime type "text/css"

  Scenario: Fetching javascript files:
    Given I fetch the urls:
      | url                                |
      | /media/js/actions.js               |
      | /media/js/calendar.js              |
      | /media/js/core.js                  |
      | /media/js/dateparse.js             |
      | /media/js/getElementsBySelector.js |
      | /media/js/timeparse.js             |
      | /media/js/urlify.js                |
    When all the responses have status code 200
    Then all the responses have mime type "application/javascript"
