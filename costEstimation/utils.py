
def estimateEffort(loc, task_level, months):
    if task_level == "easy":
        p = 2000
    elif task_level == "medium":
        p = 10000
    elif task_level == "hard":
        p = 20000
    else:
        raise Exception("invalid task difficulty")

    if loc < 15E3:
        B = 0.16
    else:
        B = 0.39

    return (loc/p)**3 * B * months**-4