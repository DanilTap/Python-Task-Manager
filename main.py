import tkinter as tk
from tkinter import ttk, RIGHT, BOTTOM, LEFT, X, Y, HORIZONTAL, VERTICAL# new widgets
from threading import Thread
import psutil
import time
import os
#print(psutil.cpu_percent(3))
root = tk.Tk()
root.title("Псевдо диспетчер")
root.geometry("770x550")
processes_nums = 0
all_processes = 0
uptime = 3


# METHODS
def ProcUpdate():
	global processes_nums
	global all_processes
	while True:
		time.sleep(uptime)
		p1 = 0
		for i in proc_table.get_children():
			proc_table.delete(i)

		for proc in psutil.process_iter():
			num = processes_nums + 1
			proc_table.insert(parent='', index='end', iid=num, text='', values=(f'{proc.name()}', f'{round(proc.cpu_percent())}', f'{round(proc.memory_info().rss / 1048576, 2)} МБ', f'{proc.ppid()}', ' '))
			processes_nums += 1

			p1 += 1

		all_processes = p1
		processes_amount.configure(text=f'Процессов: {all_processes}      ')


def ProcDelete(a):
	item = proc_table.selection()[0]
	values = proc_table.item(item, option="values")
	os.system(f'TASKKILL /IM {values[0]}')
	proc_table.delete(item)

def SetUptime():
	global uptime
	uptime = int(uptime_entry.get())


# WIDGETS
# Notebook
tabs = ttk.Notebook(root)
# Processes
processes = tk.Frame(tabs)
tabs.add(processes, text='Процессы')
proc_table = ttk.Treeview(processes)
proc_table['columns'] = ('name', 'cpu', 'ram', 'pid', 'about')

proc_table.column("name", width=160)
proc_table.column("cpu", width=30)
proc_table.column("ram", width=60)
proc_table.column("pid", width=35)
proc_table.column("about",width=100)

proc_table.heading("name",text="Имя")
proc_table.heading("cpu",text="ЦП")
proc_table.heading("ram",text="ОЗУ")
proc_table.heading("pid",text="PID")
proc_table.heading("about",text="Описание")

proc_table.pack(expand=1, fill='both')

# Scrollbar
# Scroll bar y
scrollbary = tk.Scrollbar(proc_table, orient=VERTICAL)
proc_table.configure(yscrollcommand=scrollbary.set)
scrollbary.config(command=proc_table.yview, cursor="arrow")# sb_v_double_arrow
scrollbary.pack(fill=Y, side=RIGHT)
# Scroll bar x
scrollbarx = tk.Scrollbar(proc_table, orient=HORIZONTAL)
proc_table.configure(xscrollcommand=scrollbarx.set)
scrollbarx.config(command=proc_table.xview, cursor="arrow")# sb_h_double_arrow
scrollbarx.pack(fill=X, side=BOTTOM)


# System
system = tk.Frame(tabs)
tabs.add(system, text='Система')
tabs.pack(expand=2, fill='both')
sys_lab = tk.Label(system, text="Пасхалочка", font=('Hack', 11))
sys_lab.place(x=150, y=50)

# Buttons
proc_delete = tk.Button(processes, text="Завершить процесс", font=('Arial', 9), command=ProcDelete)
proc_delete.pack(side=RIGHT)

# Labels
processes_amount = tk.Label(processes, text=f'Процессов: {all_processes}      ', font=('Arial', 9))
processes_amount.pack(side=LEFT)
uptime_label = tk.Label(processes, text=f'Время обновления(сек):', font=('Arial', 9))
uptime_label.pack(side=LEFT)

# Entry
uptime_entry = tk.Entry(processes, width=3)
uptime_entry.pack(side=LEFT)
uptime_button = tk.Button(processes, text="✔", font=('Arial', 9), border=0, cursor="hand2", command=SetUptime)
uptime_button.pack(side=LEFT)


root.bind("<KeyPress-Delete>", ProcDelete)
processes_update = Thread(target=ProcUpdate, args=[])
processes_update.start()
root.mainloop()
