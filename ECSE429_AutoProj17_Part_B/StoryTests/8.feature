Feature: As a student, I query all incomplete HIGH priority tasks from all my classes, to identity my short-termgoals.

Scenario Outline: Normal Flow
I use get API to query all incomplete HIGH priority tasks using valid category id

Given there are three categories HIGH, MEDIUM and LOW
And there is an incomplete task "<task name>" with unknown task id
And there is a completed task with HIGH priority
When I send a get API with high priority category id todos
Then I should receive all incomplete HIGH priority tasks "<task name>"

Examples: 
    | task name   | priority    |
	| Assignment  | HIGH        |
	| Midterm     | HIGH        |
	| Final       | HIGH        |
	| ClassQuiz   | HIGH        |

Scenario Outline: Alternate Flow
I use get API to query all incomplete HIGH priority tasks using valid category name

Given there are three categories HIGH, MEDIUM and LOW
And there is an incomplete task "<task name>" with unknown task id
And there is a completed task with HIGH priority
And I forgot the category id
When I query category id using valid category name "<priority>"
And I send a get API with high priority category id todos
Then I should receive all incomplete HIGH priority tasks "<task name>"

Examples: 
    | task name   | priority    |
	| Assignment  | HIGH        |
	| Midterm     | HIGH        |
	| Final       | HIGH        |
	| ClassQuiz   | HIGH        |

Scenario Outline: Error Flow
I use get API to query all incomplete HIGH priority tasks using invalid category id

Given there are three categories HIGH, MEDIUM and LOW
And there is an incomplete task "<task name>" with unknown task id
And there is a completed task with HIGH priority
When I send a get API with invalid category id
Then I should get an error message

Examples: 
	| task name   | priority    |
	| Assignment  | HIGH        |
	| Midterm     | HIGH        |
	| Final       | HIGH        |
	| ClassQuiz   | HIGH        |