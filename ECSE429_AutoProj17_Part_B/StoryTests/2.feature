
Feature: As a student, I add a task to a course to do list, so I can remember it.

Scenario Outline: Normal Flow
  I add a todo with name to the class todos list

	Given there is a class "<className>" projects I have known Id by led
	And there is a task "<taskName>" I have known Id by led
	When I add the task "<taskName>" to a course to do list by led
	Then the task "<taskName>" is in that class "<className>" by led

	Examples:
		| className     | taskName    |
		| MATH140       | Assignment  |
		| ECSE429       | Midterm     |
		| COMP512       | Final       |
		| ECSE326       | ClassQuiz   |


Scenario Outline: Alternate Flow
	I create a todo with name and add to the class todos list

	Given there is a class "<className>" projects I have known Id by led
	When I create a task "<taskName>" I have known Id by led
	And I add the task "<taskName>" to a course to do list by led
	Then the task "<taskName>" is in that class "<className>" by led

	Examples:
		| className     | taskName    |
		| MATH140       | Assignment  |
		| ECSE429       | Midterm     |
		| COMP512       | Final       |
		| ECSE326       | ClassQuiz   |

Scenario Outline: Error Flow
	I enter the wrong className ID

	Given there is a class "<className>" projects I have known Id by led
	And there is a task "<taskName>" I have known Id by led
	When I add the task "<taskName>" to a course to do list with wrong Id by led
	Then I get an error message by led

	Examples:
		| className     | taskName    |
		| MATH140       | Assignment  |
		| ECSE429       | Midterm     |
		| COMP512       | Final       |
		| ECSE326       | ClassQuiz   |
