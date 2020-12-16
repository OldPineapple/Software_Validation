Feature: Change donestatus

As a student, I mark a task as done on my course to do list, so I can track my accomplishments.

  Background:
    Given the server is running by led

  Scenario Outline: (Normal flow) Directly modify
    Given there is a task "<taskName>" I have known Id by led
    When I modify the doneStatus of the task to "<newS>" by led
    Then the donestatus of the task "<taskName>" should have been changed to "<newS>" by led

    Examples:
      | taskName |   newS  |
      |    task1 |   true  |
      |    task2 |   true  |
      |    task3 |   true  |

	Scenario Outline: (Alternative flow) Delete and create
    Given there is a task "<taskName>" I have known Id by led
    When I modify the doneStatus of the task to "<newS>" by led
    And I modify the description of the task to "<newD>" by led
    Then the description of the task "<taskName>" should have been changed to "<newD>" by led
		And the donestatus of the task "<taskName>" should have been changed to "<newS>" by led

		Examples:
      | taskName |   newS  | newD  |
      |    task1 |   true  | newD1 |
      |    task2 |   true  | newD2 |
      |    task3 |   true  | newD3 |


	Scenario Outline: (Error flow 1) Task does not exist
    Given there is not a task "<taskName>" I have known Id by led
    When I modify the doneStatus of the task to "<newS>" by led
    Then I get an error message by led

		Examples:
      | taskName |   newS  |
      |    task1 |   true  |
      |    task2 |   true  |
      |    task3 |   true  |
