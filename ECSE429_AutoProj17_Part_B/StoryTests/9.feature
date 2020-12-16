Feature: Adjust priority
  As a student,
  I want to adjust the priority of a task,
  to help better manage my time.

  Background: 
    Given the server is running

  Scenario Outline: (Normal flow) Delete then add
    Given there is a task "<taskName>" I have known Id
    And there are three categories HIGH, MEDIUM and LOW
    And the task is related to the category "<oldPriority>"
    When I delete the relationship between "<oldPriority>" and the task
    And I add a new relationship between "<newPriority>" and the task
    Then the priority of the task should have been changed to "<newPriority>"

    Examples:
      | taskName | oldPriority | newPriority |
      |    task1 |        HIGH |         LOW |
      |    task2 |         LOW |        HIGH |
      |    task3 |      MEDIUM |        HIGH |

  Scenario Outline: (Alternative flow) Add then delete
    Given there is a task "<taskName>" I have known Id
    And there are three categories HIGH, MEDIUM and LOW
    And the task is related to the category "<oldPriority>"
    When I add a new relationship between "<newPriority>" and the task
    And I delete the relationship between "<oldPriority>" and the task
    Then the priority of the task should have been changed to "<newPriority>"

    Examples:
      | taskName | oldPriority | newPriority |
      |    task1 |        HIGH |         LOW |
      |    task2 |         LOW |        HIGH |
      |    task3 |      MEDIUM |        HIGH |

  Scenario Outline: (Error flow 1) Task does not exist
    Given there is not a task "<taskName>" I have known Id
    And there are three categories HIGH, MEDIUM and LOW
    When I add a new relationship between "<newPriority>" and the task
    Then I get an error message

    Examples:
      | taskName | newPriority |
      |    task1 |        HIGH |
      |    task2 |         LOW |
      |    task3 |      MEDIUM |

  Scenario Outline: (Error flow 2) Task id is in wrong format
    Given there is a task "<taskName>" I have known Id
    And there are three categories HIGH, MEDIUM and LOW
    When I add a new relationship between "<newPriority>" and the task with a wrong id "<wrongId>"
    Then I get an error message

    Examples:
      | taskName | wrongId | newPriority |
      |    task1 |     one |         LOW |
      |    task2 |     two |        HIGH |
      |    task3 |   three |        HIGH |

  Scenario Outline: (Error flow 3) Priority is in wrong format
    Given there is a task "<taskName>" I have known Id
    And there are three categories HIGH, MEDIUM and LOW
    When I add a new relationship between a wrong priority "<wrongP>" and the task
    Then I get an error message

    Examples:
      | taskName | newPriority |   wrongP |
      |    task1 |        HIGH |   wrongP |
      |    task2 |         LOW |   wrongP |
      |    task3 |      MEDIUM |   wrongP |