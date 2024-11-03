from neuralintents import BasicAssistant
import pandas_datareader as web
import sys
from datetime import datetime, timedelta
import numpy as np
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class VirtualAssistant:
    def __init__(self):
        self.stock_tickers = {
            'AAPL': 'Apple', 
            'FB': 'Meta', 
            'GS': 'Goldman Sachs', 
            'TSLA': 'Tesla', 
            'GOOGL': 'Google', 
            'MSFT': 'Microsoft'
        }
        self.todos = []

        if not os.path.exists("short_intents.json"):
            raise FileNotFoundError("short_intents.json file not found. Please ensure it's in the same directory as main.py")

        self.mappings = {
            'stocks': self.stock_function,
            'todoshow': self.todo_show,
            'todoadd': self.todo_add,
            'todoremove': self.todo_remove,
            'goodbye': self.bye
        }
        try:
            self.assistant = BasicAssistant("short_intents.json", self.mappings)
            self.assistant.load_model()

        except Exception as e:
            print(f"Error initializing assistant: {str(e)}")
            raise

    def stock_function(self):
        print("\nFetching latest stock prices...\n")
        try:
            for ticker, company in self.stock_tickers.items():
                end_date = datetime.now()
                start_date = end_date - timedelta(days=7)
                data = web.DataReader(ticker, 'yahoo', start_date, end_date)
                current_price = data['Close'].iloc[-1]
                price_change = data['Close'].iloc[-1] - data['Close'].iloc[-2]
                percent_change = (price_change / data['Close'].iloc[-2]) * 100
                
                print(f"{company} ({ticker}):")
                print(f"Current Price: ${current_price:.2f}")
                print(f"Daily Change: ${price_change:.2f} ({percent_change:.2f}%)")
                print("-" * 50)
        except Exception as e:
            print(f"Error fetching stock data: {str(e)}")

    def todo_show(self):
        if not self.todos:
            print("\nYour todo list is empty!")
            return
        print("\nYour TODO list:")
        for idx, todo in enumerate(self.todos, 1):
            print(f"{idx}. {todo}")

    def todo_add(self):
        todo = input("\nWhat TODO do you want to add: ").strip()
        if todo:
            self.todos.append(todo)
            print(f"Added: {todo}")
        else:
            print("Task cannot be empty!")

    def todo_remove(self):
        if not self.todos:
            print("\nYour todo list is already empty!")
            return
            
        self.todo_show()
        try:
            idx = int(input("\nWhich TODO to remove (number): ")) - 1
            if 0 <= idx < len(self.todos):
                removed_todo = self.todos.pop(idx)
                print(f"Removed: {removed_todo}")
            else:
                print("Invalid task number!")
        except ValueError:
            print("Please enter a valid number!")

    def bye(self):
        print("\nGoodbye! Have a great day!")
        sys.exit(0)

    def run(self):
        print("Virtual Assistant is ready! (Type 'bye' to exit)")
        print("You can ask about stocks, manage todos, or just chat!")

        while True:
            try:
                message = input("\nYou: ").strip().lower()
                self.assistant.request(message)
            except Exception as e:
                print(f"Error: {str(e)}")
                print("Please try again!")

if __name__ == "__main__":
    assistant = VirtualAssistant()                
    assistant.run()