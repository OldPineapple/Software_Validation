
Feature: As a student,I remove a to dolist for a classwhichI am no longer taking,to declutter my schedule.

Scenario Outline: Normal Flow 
I remove a project directly with knowing id

Given there is a class "<className>" projects I have known Id
When I send a delete API "<APIdelete>"
And I send a get Request "<APIget>" about projects Course
Then check all the projects. there is no projects with this "<className>"

Examples: 
	| className | APIdelete     | APIget    |
	| ECSE429   | /projects/:id | /projects |
	| COMP512   | /projects/:id | /projects |
	| COMP417   | /projects/:id | /projects |
	| ECSE326   | /projects/:id | /projects |
	| ECSE420   | /projects/:id | /projects |
	| ECSE458   | /projects/:id | /projects |


Scenario Outline: Normal Flow 
I remove a project directly without knowing id

Given there is a class "<className>" projects I have not known Id
When I use a get api "<APIget>" with parameter "<className>" string as a filter to get id
And I send a delete API "<APIdelete>"
And I send a get Request "<APIget>" about projects Course
Then check all the projects. there is no projects with this "<className>"

Examples: 
	| className | APIdelete     | APIget    |
	| ECSE429   | /projects/:id | /projects |
	| COMP512   | /projects/:id | /projects |
	| COMP417   | /projects/:id | /projects |
	| ECSE326   | /projects/:id | /projects |
	| ECSE420   | /projects/:id | /projects |
	| ECSE458   | /projects/:id | /projects |


Scenario Outline: Error Flow 
I remove a project directly with knowing wrong id

Given there is a class "<className>" projects I have known a wrong Id
When I send a delete API "<APIdelete>"
Then I should get a error message "<error>"

Examples: 
	| className | APIdelete     | error                        |
	| ECSE429   | /projects/:id | Could not find any instances |
	| COMP512   | /projects/:id | Could not find any instances |
	| COMP417   | /projects/:id | Could not find any instances |
	| ECSE326   | /projects/:id | Could not find any instances |
	| ECSE420   | /projects/:id | Could not find any instances |
	| ECSE458   | /projects/:id | Could not find any instances |

