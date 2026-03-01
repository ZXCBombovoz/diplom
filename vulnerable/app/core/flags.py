def submit_flag(task_id, mode, data, user):
    task = TASK_REGISTRY[task_id]

    if mode == "exploit":
        return task.check_exploit(data, user)
    if mode == "fix":
        return task.check_fix(data, user)

