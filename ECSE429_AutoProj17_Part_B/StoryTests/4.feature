
Feature: As a student,I remove an unnecessary task from my course todo list,so I can forget about it.


Scenario Outline: Normal Flow 
I use delete API to delete task with correct id

Given there is a class "<className>" projects I have known Id
And I have a unnecessary task "<taskName>" in it
When I send a delete API "<APIdelete>"
And I send a get Request "<APIget>" about projects Course
Then the task should be not in the project Course

Examples: 
	| CourseName    | task Name   | APIdelete               | APIget        |
	| MATH140       | Assignment  | /projects/:id/tasks/:id | /projects/:id |
	| ECSE429       | Midterm     | /projects/:id/tasks/:id | /projects/:id |
	| COMP512       | Final       | /projects/:id/tasks/:id | /projects/:id |
	| ECSE326       | ClassQuiz   | /projects/:id/tasks/:id | /projects/:id |

Scenario Outline: Alternate Flow 
I use post API to delete task with correct id

Given there is a class "<className>" projects I have known Id
And I have a unnecessary task "<taskName>" in it
When I send a put API "<APIpost>" with "<data>"
And I send a get Request "<APIget>" about projects Course
Then the task should be not in the project Course

Examples: 
	| CourseName    | task Name   | APIpost       | data          | APIget        |
	| MATH140       | Assignment  | /projects/:id | {"tasks": []} | /projects/:id |
	| ECSE429       | Midterm     | /projects/:id | {"tasks": []} | /projects/:id | 
	| COMP512       | Final       | /projects/:id | {"tasks": []} | /projects/:id |
	| ECSE326       | ClassQuiz   | /projects/:id | {"tasks": []} | /projects/:id |

Scenario Outline: Error Flow 
I use delete API to delete task with wrong id

Given there is a class "<className>" projects I have known Id
And I have a unnecessary task "<taskName>" in it
When I send a delete API "<APIdelete>" with wrong id
Then I should get a error message "<error>"

Examples:
	| CourseName    | taskName    | APIdelete               | error                        |
	| MATH140       | Assignment  | /projects/:id/tasks/:id | Could not find any instances |
	| ECSE429       | Midterm     | /projects/:id/tasks/:id | Could not find any instances |
	| COMP512       | Final       | /projects/:id/tasks/:id | Could not find any instances |
	| ECSE326       | ClassQuiz   | /projects/:id/tasks/:id | Could not find any instances |