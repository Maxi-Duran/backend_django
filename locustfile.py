from locust import HttpUser, task, between

ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzYxMzEyMzEyLCJpYXQiOjE3NTg3MjAzMTIsImp0aSI6Ijk1YzE3MzM5YmRkZTQwYzZhYTgwNzhjNmJhYzZiM2Q5IiwidXNlcl9pZCI6IjIifQ.B_FeYCn54SQYANCTH2TYmL-pjgfzoZJv-cg2tD7ypv4"  

class ContestUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def register_participant(self):
        self.client.get(
            "/api/contest/participants/",
            json={"user": 2, "contest": 1},  
            headers={
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/json",
                "Accept": "*/*",
            }
        )
    
