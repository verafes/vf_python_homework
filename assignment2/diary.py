# Assignment 2. Task 1
import traceback
from datetime import datetime

try:
    with open("diary.txt", "a") as file:
        current_time = datetime.now().strftime("%A, %B %d, %Y %I:%M %p")
        file.write(f"\nDiary Entry - {current_time}\n")
        file.write("-" * 30 + "\n")
        prompt = "What happened today? \n(Type 'done for now' for exit) "
        while True:
            user_entry = input(prompt)
            file.write(user_entry + "\n")

            if user_entry.lower() in ["done for now", 'done']:
                break
            prompt = "What else? "

except Exception as e:
   trace_back = traceback.extract_tb(e.__traceback__)
   stack_trace = list()
   for trace in trace_back:
      stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
   print(f"Exception type: {type(e).__name__}")
   message = str(e)
   if message:
      print(f"Exception message: {message}")
   print(f"Stack trace: {stack_trace}")

