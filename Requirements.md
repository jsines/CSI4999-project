_**Tool Chain**_
*repository*:  *Github and using google drive for any additional files needed\
*Issue tracking*:  *Github
*Communication*:  *Discord 
*Hosting*:  *Initally we plan to run the web program on our local machines but will move to use a SECS vitrual machine or other web hosting soultions such as 000webhost
*Development environment*:  *Any IDE anyone would like to use is welcome most group memebers will use plain text editors or markdown inside github

_**Database Requirements:**_
* Database service: MySQL (run localy for presentations, though web service for specific demonstartive purposes)
  * Backend service to connect directly to database, frontend service used to add to/change database in real time
* Total Classes: 3 (Business, Employer, Employee)
  * Class Hierarchy: Business > Employer > Employee
  * Queries under Business class can modify/manipulate Employer and Employee entities
  * Queries under Employer class can modify/manipulate Employee entities
  * Queries under Employee class can only modify their own, individual entity

_**UI Plan:**_
