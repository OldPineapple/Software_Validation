
Feature: As a student, I categorize tasks as HIGH, MEDIUM or LOW priority, so I can better manage my time.

Background:
	Given the server is running by led

Scenario Outline: Normal Flow
  I use post API to relate task with category

	Given there is a task "<taskName>" I have known Id by led
	And there are three categories HIGH, MEDIUM and LOW by led
	When I add a new relationship between "<newPriority>" and the task by led
	Then the priority of the task should have been changed to "<newPriority>" by led

	Examples:
		| taskName | newPriority   |
		|    task1 |    LOW        |
		|    task2 |    MEDIUM     |
		|    task3 |    HIGH       |

Scenario Outline: Alternate Flow
	I use post API to set up the priority when i post the task

	Given there is a task "<taskName>" I have known Id by led
	And there are three categories HIGH, MEDIUM and LOW by led
	When I add a relationship between "<oldPriority>" and the task by led
	And I delete the relationship between "<oldPriority>" and the task by led
  And I add a new relationship between "<newPriority>" and the task by led
	Then the priority of the task should have been changed to "<newPriority>" by led

	Examples:
		| taskName | oldPriority | newPriority |
		|    task1 |        HIGH |         LOW |
		|    task2 |         LOW |        HIGH |
		|    task3 |      MEDIUM |        HIGH |

Scenario Outline: (Error flow) Task does not exist
  Given there is not a task "<taskName>" I have known Id by led
  And there are three categories HIGH, MEDIUM and LOW by led
  When I add a new relationship between "<newPriority>" and the task by led
  Then I get an error message by led

  Examples:
    | taskName | newPriority |
    |    task1 |        HIGH |
    |    task2 |         LOW |
    |    task3 |      MEDIUM |
