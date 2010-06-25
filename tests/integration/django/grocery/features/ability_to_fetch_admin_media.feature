Feature: fetch admin media from lettuce + django builtin server
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
      | /media/js/actions.min.js           |
      | /media/js/calendar.js              |
      | /media/js/collapse.js              |
      | /media/js/collapse.min.js          |
      | /media/js/core.js                  |
      | /media/js/dateparse.js             |
      | /media/js/getElementsBySelector.js |
      | /media/js/inlines.js               |
      | /media/js/inlines.min.js           |
      | /media/js/jquery.init.js           |
      | /media/js/jquery.js                |
      | /media/js/jquery.min.js            |
      | /media/js/prepopulate.js           |
      | /media/js/prepopulate.min.js       |
      | /media/js/timeparse.js             |
      | /media/js/urlify.js                |
    When all the responses have status code 200
    Then all the responses have mime type "application/javascript"
