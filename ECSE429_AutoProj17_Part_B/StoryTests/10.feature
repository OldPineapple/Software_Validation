Feature: Change description
  As a student,
  I want to change a task description,
  to better represent the work to do.

  Background: 
    Given the server is running

  Scenario Outline: (Normal flow) Directly modify
    Given there is a task "<taskName>" I have known Id
    When I modify the description of the task to "<newD>"
    Then the description of the task "<taskName>" should have been changed to "<newD>"

    Examples:
      | taskName |    newD |
      |    task1 |   newD1 |
      |    task2 |   newD2 |
      |    task3 |   newD3 |

  Scenario Outline: (Alternative flow) Delete and create
    Given there is a task "<taskName>" I have known Id
    When I delete the task
    And create a new task of "<taskName>" with the new description "<newD>"
    Then the description of the task "<taskName>" should have been changed to "<newD>"

    Examples:
      | taskName |    newD |
      |    task1 |   newD1 |
      |    task2 |   newD2 |
      |    task3 |   newD3 |

  Scenario Outline: (Error flow 1) Task does not exist
    Given there is not a task "<taskName>" I have known Id
    When I modify the description of the task to "<newD>"
    Then I get an error message

    Examples:
      | taskName |    newD |
      |    task1 |   newD1 |
      |    task2 |   newD2 |
      |    task3 |   newD3 |

  Scenario Outline: (Error flow 2) Task id is in wrong format
    Given there is a task "<taskName>" I have known Id
    When I modify the description of the task using a wrong id "<wrongId>" to "<newD>"
    Then I get an error message

    Examples:
      | taskName | wrongId |    newD |
      |    task1 |     one |   newD1 |
      |    task2 |     two |   newD2 |
      |    task3 |   three |   newD3 |