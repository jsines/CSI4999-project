__*User Stories For Application Design That Translate To Fundamental Database Implementations*__

1. As an Employee, I need to be able to track my time logs for specified projects 

      -->Table: Project; Attributess: Employee_ID, Project_ID, Time_Spent
      
2. As an Employee, I need to be able to track my expenses for specified projects

      -->Table: Project; Atrributes: Employee_ID, Project_ID, Expense_Amount
      
3. As an Employee I need to be able to perform (above actions) using a simple application interface

       --> UI will contain elements on employee page that will allow them to modify their values (attributes)
       for these tables in real time
       
4. As an Employer, I need to be able to register employees under an account that I can monitor and keep track of

      --> Table: Employee; Attributes: (Employee personal information and work-relavent information [availability]), Employee_ID, Business_ID
      
5. As an Employer, I need to be able to manage/modify employee information for administrative purposes.

      --> Employer Acount can modify employee data (attributes) on database in real time through web UI
      
6. As an Employer, I need to be able to generate invoices for employees based on time spent on projects and employee charge rate

      --> Allow for application to fullfil process; invoices will most likely be their own table, with employee IDs linked to them 
      
7. As an Employer, I need to be able to submit invoices for chain of approval across buisness board 

      --> Most likely to be a table in itself, having relevant IDs as and boolean values as attributes (approval, paid, etc.)
   
8. As an Employer, I need full administrative permissions to be able to monitor projects and data changes across the business

      --> proper authentication through login into web application will grant visibility for said tables.
