# My Sing Course Database 

## Description: My project is a database/portal that captures information which a singing instructor can gather from his/her students.
Information that can be gathered includes feedback from sessions, student's personal information, account information, etc. My intent is to make this process simple and easy for the singing instructor to implement and enable them keep track of a student's progress. Ideally, students would be able to log into their account and also keep track of what improvements they've made or how they are doing.


###                                    API Reference Table for Students and User Accounts                                  

|   endpoint paths                      | methods            | parameters |    Description                                  | 
|   :---:                               |:---:               | :---:      | :---:                                           |
| {{ base_url }}/                       | def index          |  None      |   Query all students                            |
| {{ base_url }}/<int:id>               | def show           | id: int    |   Query for specific student                    |
| {{ base_url }}/user_accounts          | def index_accounts |  None      |   Query all user accounts                       |
| {{ base_url }}/                       | def create         |  None      |   Add New Student                               |
| {{ base_url }}user_account/new        | def new_account    |  None       |   Add a user account for a student              |
| {{ base_url }}update_account/<int:id> | def update         | id: int    |   Update Student's user account and password    |
| {{ base_url }}<int:id>                | def remove_student | id: int    |   Delete Student from students table            |

<p>
Note: {{ base_url }} = http://localhost:5000/students in my case. This may vary.
</p>

<p>
1. How did the project's esign evolve over time?

As I developed news skills during the Nucamp training bootcamp, I integrated what I learned in order to practice applying the skills.
I then thought of ways to enhance the project and make it more friendly and easy to understand for the end user, which would be a singing instructor.
</p>
<p>
2. Did you choose to use an ORM or raw SQL? Why?

I originally chose to use an ORM  in order to become more familiar with it. However, for a project such as this singing course, raw SQL seemed to be the better and more efficient choice for querying data and viewing reports. I also choose raw SQL to avoid N+1 queries using ORM.

</p>
<p>
3. What future improvements are in store, if any?

I would like to make an easy to use web interface/frontend for a singing instructor and a portal for students to use and review the feedback on their training. I would also attempt to optimize the database further and work on best practices for database security.
</p>
