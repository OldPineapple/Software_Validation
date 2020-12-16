
Feature: As a student,I create a todo list for a new class I am taking,so I can manage course work.

Scenario Outline: Normal Flow 
I create a todo with name

When I send a post api "<APIpost>" with "<className>"
And I send a get Request "<APIget>" about projects Course
Then I will get a projects with right "<className>"

Examples: 
	| APIpost   | className | APIget        |
	| /projects | ECSE429   | /projects/:id |
	| /projects | COMP512   | /projects/:id |
	| /projects | COMP417   | /projects/:id |
	| /projects | ECSE326   | /projects/:id |
	| /projects | ECSE420   | /projects/:id |
	| /projects | ECSE458   | /projects/:id |

Scenario Outline: Alternate Flow 
I create a projects with name and description

When I send a post api "<APIpost>" with both "<className>" and "<description>"
And I send a get Request "<APIget>" about projects Course
Then I will get a project with right "<className>" and "<description>"

Examples: 
	| APIpost   | className | description | APIget        |
	| /projects | ECSE429   | validation  | /projects/:id |
	| /projects | COMP512   | distribute  | /projects/:id |
	| /projects | COMP417   | robotics    | /projects/:id |
	| /projects | ECSE326   | requirement | /projects/:id |
	| /projects | ECSE420   | parallel    | /projects/:id |
	| /projects | ECSE458   | dp          | /projects/:id |


Scenario Outline: Error Flow 
I create a todo with name and ID

When I send a post api "<APIpost>" with "<className>" with id
Then I should get a error message "<error>"

Examples:
	| APIpost   | className | error                                                              |
	| /projects | ECSE429   | Invalid Creation: Failed Validation: Not allowed to create with id |
	| /projects | COMP512   | Invalid Creation: Failed Validation: Not allowed to create with id |
	| /projects | COMP417   | Invalid Creation: Failed Validation: Not allowed to create with id |
	| /projects | ECSE326   | Invalid Creation: Failed Validation: Not allowed to create with id |
	| /projects | ECSE420   | Invalid Creation: Failed Validation: Not allowed to create with id |
	| /projects | ECSE458   | Invalid Creation: Failed Validation: Not allowed to create with id |