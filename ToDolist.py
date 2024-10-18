import json
import time


class Task:
    def __init__(self, task):
        self.task = task
        self.completed = False

    #Markera uppgift som klar
    def complete(self):
        self.completed = True

    #Representera uppgiften som en ordbok
    def to_dict(self):
        return {"task": self.task, "completed": self.completed}

    #Skapa en Task från en ordbok
    def from_dict(self, data):
        self.task = data["task"]
        self.completed = data["completed"]

#Egen klass för att hantera listan med uppgifter, den laddar upp uppgifterna från en fil direkt
#Allt i programet sparas automatiskt igenom self.save_to_json()
class TodoList:
    def __init__(self, filename):
        self.tasks = []
        self.filename = filename
        self.load_from_json()  

    #Lägga till en ny uppgift
    def add_task(self, task_name):
        task = Task(task_name)
        self.tasks.append(task)
        self.save_to_json()

    #Markerar en uppgift som klar
    def complete_task(self, task_name):
        for task in self.tasks:
            if task.task == task_name:
                task.complete()
                self.save_to_json()
                break

    #Tar bort en uppgift
    def remove_task(self, task_name):
        self.tasks = [task for task in self.tasks if task.task != task_name]
        self.save_to_json() 

    #Visar alla uppgifter
    def show_tasks(self):
        if not self.tasks:
            print("Du har inga uppgifter!")
        for task in self.tasks:
            status = "Gjort!" if task.completed else "Ogjort!"
            print(f"Uppgift: {task.task} | Status: {status}")

    #Sparar uppgifter till JSON-fil, w skapar/skriver över uppgiften till filen
    def save_to_json(self):
        with open(self.filename, 'w') as file:
            json.dump({"tasks": [task.to_dict() for task in self.tasks]}, file, indent=4)

    #Laddar uppgifter från JSON-fil
    def load_from_json(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for task_data in data["tasks"]:
                    task = Task("") 
                    task.from_dict(task_data) 
                    self.tasks.append(task)
        except FileNotFoundError:
            print(f"Filen '{self.filename}' Inga uppgifter hittades.")

#Användarmeny för att hantera uppgifter
#Använder mig av time för att användaren inte ska få all information samtidigt och det ska se lite renare ut
def menu(todo_list):
    while True:
        print("\n--- To-Do List Meny ---")
        time.sleep(2)
        print("1. Visa uppgifter")
        time.sleep(0.5)
        print("2. Lägg till uppgift")
        time.sleep(0.5)
        print("3. Markera uppgift som klar")
        time.sleep(0.5)
        print("4. Ta bort uppgift")
        time.sleep(0.5)
        print("5. Avsluta")
        time.sleep(0.5)
        choice = input("Välj ett alternativ (1-5): ")

        #Nedan bestämmer vad som händer i programmet beroende på vad användaren skriver in i input
        if choice == "1":
            todo_list.show_tasks()
        elif choice == "2":
            task_name = input("Ange uppgiften du vill lägga till: ")
            todo_list.add_task(task_name)
        elif choice == "3":
            task_name = input("Ange uppgiften du vill markera som klar: ")
            todo_list.complete_task(task_name)
        elif choice == "4":
            task_name = input("Ange uppgiften du vill ta bort: ")
            todo_list.remove_task(task_name)
        elif choice == "5":
            print("Ses sen!")
            time.sleep(1)
            print ("------Programmet avslutas------")
            break
        else:
            print("Ogiltigt val. Försök igen.")


if __name__ == "__main__":
    filename = "todo_list.json"
    todo_list = TodoList(filename)

    #Startar menyn
    menu(todo_list)
