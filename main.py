from rich.console import Console
from rich.table import Table
from rich.traceback import install
from rich.prompt import Prompt
from tinydb import TinyDB, Query
from datetime import date
install() # better error handling. from rich.traceback

# Database
# for dev
DB = TinyDB('db.json', sort_keys=True, indent=4, separators=(',', ': '))
# for "production"py 
#DB = TinyDB('db.json') 

# function to insert into db
def db_insert(task: str, status: str, completed_by: str):
    # Must be stringified or tinyDB throws a fit.
    created_when: str = str(date.today())
    DB.insert({
        "task": task,
        "status": status,
        "completed_by": completed_by,
        "created": created_when
    })

# reuseable initmenu the type setting
# is probably not necessary could be like list_todo()
def menu(a: str, r: str, v: str, u: str) -> str:
    prompt: str = Prompt.ask(
        f"""please select your destination.
        {a} to Add task
        {r} to Remove task
        {v} to View Tasks
        {u} to update task status \n""", 
        choices=[a, r, v, u]
    )
    return prompt

# reuseable listing todo
def list_todo():
    table = Table(title="Todo list", style="blue")
    table.add_column("Item ID", style="red", justify="right")
    table.add_column("Task", style="blue")
    table.add_column("Do date", style="blue")
    table.add_column("Status", style="green", justify="right")
    console = Console()
    
    for item in sorted(DB, key = lambda i: int(i.doc_id)):
    # Lambda is like an inline function see below it's the same putting 
    # this here for my own reference and learning.
    #def foo(i):
    #   return int(i.doc_id)
    #   for item in sorted(db, key = foo):
        table.add_row(
            str(item.doc_id),
            item["task"],
            item["completed_by"],
            item["status"]
        )

    console.print(table)

# removing entry this should probably be sanitized somehow but I am not sure.
def db_remove(prompt: str):
        usr_prompt = input(prompt)
        id = int(usr_prompt)
        try:
            DB.remove(doc_ids=[id])
        except Exception as e:
            print(f"Your task was not added to do an unforeseen error:{e}")

# change status to completed
def db_update(prompt: str):
    usr_prompt = input(prompt)
    id = int(usr_prompt)
    try:
        DB.update({"status": "Done"}, doc_ids=[id])
    except Exception as e:
        print(f"Your task was not updated to do an unforeseen error:{e}")

# this is the main program
def main(user_message: str):
    # this is how we exit the loop call
    # exit_program("message", "affirmative", "negative") after task with
    def exit_program(m: str, y: str, n: str) -> bool:
        exit_prompt: str = Prompt.ask(f"{m}", choices=[y, n])
        if (exit_prompt == y):
            return False
        else:
            return True

    print(user_message)
    run_program: bool = True

    while (run_program is True):
        init_menu: str = menu("A", "R", "V", "U")

        # adds to db.json
        if (init_menu == "A"):
            task_name: str = input(
                "Great, please name the task you would like to add!: "
            )
            task_status: str = "Pending"
            task_complete_by: str = input(
                "When should this task be done by? (example: \
                30th of december 2020): "
            )
            try:
                db_insert(task_name, task_status, task_complete_by)
                run_program = exit_program(
                    "Success! Task has been added. Exit?", "Yes", "No"
                )
            except Exception as e:
                print(f"Your task was not added to do an unforeseen error:{e}")

        # removes from db.json
        if (init_menu == "R"):
            list_todo()
            db_remove("please type in the ID of the task you want to delete: ")
            run_program = exit_program(
                "Success! Task have been removed. Exit?","Yes", "No"
            )
        #V iew db.json   
        if (init_menu == "V"):
            list_todo()
            run_program = exit_program("Wanna exit the program?", "Yes", "No")
        # update status
        if (init_menu == "U"):
            list_todo()
            db_update("""
            Please enter the ID of the task you would like to mark as completed
            """)
            run_program = exit_program(
                "Success! Task have been updated. Exit?","Yes", "No"
            )
#running program
if __name__ == '__main__': 
    main("Welcome user")
else:
    print("this file is not suppose to be imported anywhere you done goofed")