# Chemify

1. install packages with requirements.txt

   ```
   pip install -r requirements.txt
   ```
2. after install requirements, you can run this app by this line

   ```
   flask run --reload
   ```
3. all the test can be run by postman. in the 'api_test_postman' has a exported json file. you can import that json file and test.

The final number in the URL represents the user_no. While it may has challenges in commercial usage, for the convenience of testing, I have unavoidably included the user ID in the URL.


---

__DB relationship__

- User_model

| Column    | Data Type | Constraints |
| --------- | --------- | ----------- |
| user_no   | int       | Primary Key |
| user_id   | str       | Unique      |
| user_name | str       | -           |

- Task_model

| Column         | Data Type | Constraints                                |
| -------------- | --------- | ------------------------------------------ |
| task_id        | int       | Primary Key                                |
| task_name      | str       | -                                          |
| description    | str       | -                                          |
| status         | str       | -                                          |
| assign_user_id | int       | Foreign Key (user_model.user_no), Not Null |

- Task_history_model

| Column           | Data Type | Constraints                                |
| ---------------- | --------- | ------------------------------------------ |
| task_history_id  | int       | Primary Key                                |
| task_id          | int       | Not Null, Foreign Key (task_model.task_id) |
| task_name        | str       | -                                          |
| description      | str       | -                                          |
| status           | str       | -                                          |
| action_type      | str       | Not Null                                   |
| transaction_time | datetime  | Default: UTC Now                           |
| transaction_user | str       | -                                          |
