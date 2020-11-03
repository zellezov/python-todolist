from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class TableTask(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


class ToDoList:

    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    @staticmethod
    def print_menu():
        print("\n1) Today's tasks\n2) Week's tasks\n3) All tasks\n4) Missed tasks\n5) Add task\n6) Delete task\n0) Exit")

    def list_today_tasks(self):
        today = datetime.today()
        print(f"Today {today.day} {today.strftime('%b')}:")
        rows = self.session.query(TableTask).filter(TableTask.deadline == today.date()).all()
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for row in rows:
                print(row.task)

    def list_week_tasks(self):
        week = 8
        today = datetime.today()
        for day in range(week):
            daily = today + timedelta(days=day)
            print(f"\n{daily.strftime('%A')} {daily.day} {daily.strftime('%b')}:")
            rows = self.session.query(TableTask).filter(TableTask.deadline == daily.date()).all()
            count = len(rows)
            if count == 0:
                print("Nothing to do!")
            else:
                for i in range(count):
                    print(f"{i + 1}. {rows[i].task}")

    def list_all_tasks(self):
        print("All tasks:")
        rows = self.session.query(TableTask).order_by(TableTask.deadline).all()
        count = len(rows)
        if count == 0:
            print("Nothing to do!")
        else:
            for i in range(count):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")

    def list_missed_tasks(self):
        print("Missed tasks:")
        rows = self.session.query(TableTask).filter(TableTask.deadline < datetime.today()).order_by(TableTask.deadline).all()
        count = len(rows)
        if count == 0:
            print("Nothing is missed!")
        else:
            for i in range(count):
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")

    def add_task(self):
        new_task = input("\nEnter task\n")
        new_deadline = input("\nEnter deadline\n")
        new_row = TableTask(task=new_task, deadline=datetime.strptime(new_deadline, '%Y-%m-%d'))
        self.session.add(new_row)
        self.session.commit()
        print("The task has been added!")

    def delete_task(self):
        print("\nChoose the number of the task you want to delete:")
        rows = self.session.query(TableTask).order_by(TableTask.deadline).all()
        count = len(rows)
        all_tasks = {}
        if count == 0:
            print("Nothing to delete!")
        else:
            for i in range(count):
                all_tasks[i + 1] = rows[i].id
                print(f"{i + 1}. {rows[i].task}. {rows[i].deadline.day} {rows[i].deadline.strftime('%b')}")
        to_delete = int(input())
        row_to_delete = self.session.query(TableTask).filter(TableTask.id == all_tasks[to_delete]).all()
        specific_row_to_delete = row_to_delete[0]
        self.session.delete(specific_row_to_delete)
        self.session.commit()
        print("The task has been deleted!")

    def run(self):
        running = True
        while running:
            ToDoList.print_menu()
            choice = input()
            if choice == "0":
                print("\nBye!")
                running = False
            elif choice == "1":
                ToDoList.list_today_tasks(self)
            elif choice == "2":
                ToDoList.list_week_tasks(self)
            elif choice == "3":
                ToDoList.list_all_tasks(self)
            elif choice == "4":
                ToDoList.list_missed_tasks(self)
            elif choice == "5":
                ToDoList.add_task(self)
            elif choice == "6":
                ToDoList.delete_task(self)


Base.metadata.create_all(engine)
ToDoList().run()
