import os
from locust import TaskSet, task, between, HttpUser


class CustodianTaskSet(TaskSet):
    wait_time = between(5, 15)

    @task(10)
    def get_clients_list_depth_1(self):
        self.client.get("/custodian/data/client?depth=1", headers=self.locust.headers)

    # @todo: clients request depth > 1 requests causes fails on RPS > 3, may rely on amount of DB sessions

    # @task
    # def get_clients_list_depth_2(self):
    #     self.client.get("/custodian/data/client?depth=2", headers=self.locust.headers)

    # @task
    # def get_clients_list_depth_3(self):
    #     self.client.get("/custodian/data/client?depth=3", headers=self.locust.headers)

    @task(30)
    def get_employee_position(self):
        self.client.get("/custodian/data/employee_position/1", headers=self.locust.headers)

    @task(10)
    def get_employee_positions(self):
        self.client.get("/custodian/data/employee_position?depth=1", headers=self.locust.headers)

    @task(10)
    def get_employee_positions_d2(self):
        self.client.get("/custodian/data/employee_position?depth=2", headers=self.locust.headers)

    @task(20)
    def get_documents_d1(self):
        self.client.get("/custodian/data/document?depth=1", headers=self.locust.headers)

    @task(20)
    def get_documents_d2(self):
        self.client.get("/custodian/data/document?depth=2", headers=self.locust.headers)


class FastTasksSet(TaskSet):
    tasks = {CustodianTaskSet, }


class LegalLocust(HttpUser):
    task_set = FastTasksSet

    headers = {
        "Authentication": os.environ.get("LOCUST_TOKEN")
    }
