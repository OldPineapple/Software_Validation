Feature: As a student, I query the incomplete tasks for a class I am taking, to help manage my time.

Scenario Outline: Normal Flow
I use get API to query incomplete tasks using valid class id

Given there is a class "<class name>" projects I have known Id
And there is an incomplete task "<task name>"
And there is a completed task
When I send a get API with class id
Then I should receive all incomplete tasks "<task name>" of that class

Examples: 
	| class name    | task name   |
	| MATH140       | Assignment  |
	| ECSE429       | Midterm     |
	| COMP512       | Final       |
	| ECSE326       | ClassQuiz   |


Scenario Outline: Alternate Flow
I use get API to query incomplete tasks using valid class name

Given there is a class "<class name>" projects I have known Id
And there is an incomplete task "<task name>"
And there is a completed task
And I forgot the class id
When I query class id using valid class name "<class name>"
And I send a get API with class id
Then I should receive all incomplete tasks "<task name>" of that class

Examples: 
	| class name    | task name   |
	| MATH140       | Assignment  |
	| ECSE429       | Midterm     |
	| COMP512       | Final       |
	| ECSE326       | ClassQuiz   |

Scenario Outline: Error Flow
I use get API to query incomplete tasks using invalid class id

Given there is a class "<className>" projects I have known a wrong Id
And there is an incomplete task "<task name>"
And there is a completed task
When I send a get API with class id
Then I should get an error message

Examples:
	| class name    | task name   |
	| MATH140       | Assignment  |
	| ECSE429       | Midterm     |
	| COMP512       | Final       |
	| ECSE326       | ClassQuiz   |