class A01Task:
    task_id = "A01"

    def check_exploit(self, data, user):
        if data["owner_id"] != user.id:
            return "FLAG{A01_IDOR_EXPLOIT}"

