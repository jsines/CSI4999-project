
Test

_**Database Requirements:**_
* Database service: MySQL (run localy for presentations, though web service for specific demonstartive purposes)
  * Backend service to connect directly to database, frontend service used to add to/change database in real time
* Total Classes: 3 (Business, Employer, Employee)
  * Class Hierarchy: Business > Employer > Employee
  * Queries under Business class can modify/manipulate Employer and Employee entities
  * Queries under Employer class can modify/manipulate Employee entities
  * Queries under Employee class can only modify their own, individual entity

_**UI Plan:**_
