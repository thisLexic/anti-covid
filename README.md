The Problem this project attempts to alleviate:

This site attempts to solve an integral problem in the current state of the Philippine quarantine. 
Due to the nature of the covid quarantine in our country, cities and minicipalities 
have their own way of implementing the quarantine. 
Some cities are more lenient than others but other cities and municipalities make it very difficult 
for people to go in or out of their respective locations.

Now, this is a huge problem for the work force of the Philippines: 
nurses, doctors, cashiers, technicians, security guards, janitors, etc. 
Some workers do not live in the city where their place of work is. 
Even those that live in the city where their place of work is, it is still hard because public transportation is gone 
for the most part. This makes transportation for the work force hard.
Since the work force cannot go to their place of work, businesses are understaffed. 
This means that the general public will have a hard time buying necessary goods and services.

Basically, the problem is that workers need a way to go from their residence to their place of work 
without being stopped by checkpoints, lack of transportation, and other hurdles.

-------------------------------------------------------------------------------------------------------------------------------

The Solution this project is meant to implement (overview):

With the problem made clear, this website provides itself as a possible solution. 
Commuters can sign up and upload necessary documents that verify their identity and place of work. 
Afterwards, they can apply for routes that are determined by the city they are applying in.
After applying, city hall employees can choose to approve or disapprove their application based on the documents they provided.

-------------------------------------------------------------------------------------------------------------------------------

The Solution this project is meant to implement (general implementation):

The will be three types of users in the application: cities, employees, and commuters.

Description:

City
  - super admins
  - add one or more employees for their city account
  
Employee
  - admins
  - created my the city super admin
  - create routes
  - approve applicants
  - view commuter documents
  
 Commuter
  - created by themselves
  - applies for a route
  - uploads their documents that prove their identity/work

-------------------------------------------------------------------------------------------------------------------------------

The Solution this project is meant to implement (actually implemented):

Currently supported features of the application:

For Cities admin:
1) create and update announcements for the city	
2) delete routes
3) create, inactivate, reactivate employees 

For Employees: 
1) view announcements for their commuters
2) activate/inactivate routes (which employee made the change is visible)
3) create routes (which employee made the change is visible)
4) set and edit route trips and times (which employee made the changes is visible)
5) approve, reject and return to pending the application of commuters (which employee made the decision is visible)
6) view all commuter information and all their documents 
7) view preferred times of all commuters for any given route (tabulated) 

For Commuters
1) logging in, logging out, and signing up 
2) uploading, editing, viewing, and deleting their documents
3) viewing all routes of a city with each route's details such as starting point, end point, times, etc. 
4) can apply for any route and see the status of their application 
5) view announcements made by the cities they have applied for 
6) edit information about self (ex: contact information) 
7) create and edit preferred time of leaving per route

-------------------------------------------------------------------------------------------------------------------------------

Future features/optimisations:

1) make pdf documents visible from Firefox browsers
2) optimised queries
3) Proper ordering and display of time for employees/commuters
4) Make button for "My routes" view for Commuter PDF-able
5) Logo 

-------------------------------------------------------------------------------------------------------------------------------

Message to the reader

This is the third website I am making so please excuse my code when it is suboptimal and spaghetti-like.
Help in the form of optimisations or critiques would be much appreciated.
The project is currently active on the following website:

pasahero.benvillabroza.com
