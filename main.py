from tkinter import *
import requests
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import matplotlib.pyplot as plt
import pandas as pd
import re


root = Tk()
root.title("E.M.S App")
root.geometry("600x500+50+50")
f = ("Arial", 20, "bold")
root.configure(bg = "lightgreen")

# Home - Add Window
def add():
	root.withdraw()
	aw.deiconify()

def add_back():
	aw.withdraw()
	root.deiconify()

def add_save():
	con = None
	try:
		con = connect("db_emp")
		id = int(aw_ent_id.get().strip())
		if (id < 1):
			raise Exception("Id Should be positive")
		name = aw_ent_name.get().strip()
		if (len(name) < 2):
			raise Exception("Name should be minimum two character")
		if not bool(re.match("^[A-Za-z ]+$", name)):
			raise Exception("Name should be a character")
		salary = float(aw_ent_sal.get().strip())
		if (salary < 8000):
			raise Exception("Salary should be minimum 8K")
		sql = "insert into employee values('%d','%s','%f')"
		cursor = con.cursor()
		cursor.execute(sql % (id,name,salary))
		if cursor.rowcount == 1:	
			con.commit()
			showinfo("Success ", "Record Created")
		else:
			showerror("Issue", "Id already exists")
	
	except IntegrityError:
		showerror("Issue", "Id already exists")

	except ValueError:
		showerror("Issue", "Integers Only")
		

	except Exception as e:
		if con is not None:
			con.rollback()
		showerror("Issue ", e)
		print(e)

	finally:
		if con is not None:
			con.close()
		aw_ent_id.delete(0, END)
		aw_ent_name.delete(0, END)
		aw_ent_sal.delete(0, END)
		aw_ent_id.focus()

# Home - View Window
def view():
	root.withdraw()
	vw.deiconify()
	vw_st_data.delete(1.0, END)
	con = None
	try:
		con = connect("db_emp")
		cursor = con.cursor()
		sql = "select * from employee order by id"
		cursor.execute(sql)
		data = cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Emp ID = " + str(d[0]) + " Name = " + str(d[1]) + " Salary = " + str(d[2]) + "\n"
		vw_st_data.insert(INSERT, info)
	except Exception as e:
		showerror("Issue ", e)
	finally:
		if con is not None:
			con.close()
	
def view_back():
	vw.withdraw()
	root.deiconify()
	
# Home - Update Window
def update():
	root.withdraw()
	uw.deiconify()

def update_back():
	uw.withdraw()
	root.deiconify()

def update_save():
	con = None
	try:
		con = connect("db_emp")
		id = int(uw_ent_id.get().strip())
		if (id < 1):
			raise Exception("Id Should be positive")

		name = uw_ent_name.get().strip()
		if (len(name) < 2):
			raise Exception("Name should be minimum two character")
		if not bool(re.match("^[A-Za-z ]+$", name)):
			raise Exception("Name should be a character")

		salary = float(uw_ent_sal.get().strip())
		if (salary < 8000):
			raise Exception("Salary should be minimum 8K")
		sql = "update employee set name = '%s', salary = '%f' where id = '%d'"
		cursor = con.cursor()			
		cursor.execute(sql % (name, salary, id))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Success", "Record Update")	
		else:
			showerror("Failure", "Record does not exist")

	except IntegrityError:
		showerror("Issue", "Record does not exist")

	except ValueError:
		showerror("Issue", "Integers Only")

	except Exception as e:
		if con is not None:
			con.rollback()
		showerror("Issue ", e)
	finally:
		if con is not None:
			con.close()
			uw_ent_id.delete(0, END)
			uw_ent_name.delete(0, END)
			uw_ent_sal.delete(0, END)
			uw_ent_id.focus()

# Home - Delete Window
def delete():
	root.withdraw()
	dw.deiconify()

def delete_back():
	dw.withdraw()
	root.deiconify()

def delete_save():
	con = None
	try:
		con = connect("db_emp")
		id = int(dw_ent_id.get().strip())
		if (id < 1):
			raise Exception("Id Should be positive")

		sql = "delete from employee where id = '%d'"
		cursor = con.cursor()
		cursor.execute(sql % (id))
		if cursor.rowcount == 1:
			con.commit()
			showinfo("Success", "Record Deleted")
		else:
			showerror("Failure", "Record does not exist")

	except ValueError:
		showerror("Issue", "Id Integers Only")

	except Exception as e:
		if con is not None:
			con.rollback()
		showerror("Issue ", e)
	finally:
		if con is not None:
			con.close()
			dw_ent_id.delete(0, END)
			dw_ent_id.focus()

# Charts
def chart():
	con = None
	try:
		con = connect("db_emp")
		cursor = con.cursor()
		sql = "select name, salary from employee order by salary desc limit 5"
		cursor.execute(sql)
		data = cursor.fetchall()
		name = []
		salary = []
		for d in data:
			name.append(d[0])
			salary.append(d[1])
		plt.bar(name, salary)
		plt.xlabel("Names of Employee")
		plt.ylabel("Salary of Employee")
		plt.title("Top 5 Highest Salaried Employee")
		plt.grid()
		plt.show()
	except Exception as e:
		showerror("issue ", e)
		con.rollback()
	finally:
		if con is not None:
			con.close()


# Home Window
add_btn = Button(root, text = "Add Employee", width = 15, font = f, command = add)
add_btn.pack(pady = 10)
view_btn = Button(root, text = "View Employee", width = 15, font = f, command = view)
view_btn.pack(pady = 10)
update_btn = Button(root, text = "Update Employee", width = 15, font = f, command = update)
update_btn.pack(pady = 10)
delete_btn = Button(root, text = "Delete Employee", width = 15, font = f, command = delete)
delete_btn.pack(pady = 10)
charts_btn = Button(root, text = "Charts Employee", width = 15, font = f, command = chart)
charts_btn.pack(pady = 10)

# Location
lab_loc = Label(root, text = "Location:", font = f, bg = "lightgreen")
lab_loc.place(x=10, y=450)
lab_lans = Label(root, text = "", font = f, bg = "lightgreen")
lab_lans.place(x=130, y=450)

loc = 'https://ipinfo.io/'
res = requests.get(loc)
data = res.json()
loc = data["city"]
lab_lans.configure(text=loc)

# Temperature
lab_temp = Label(root, text = "Temperature:", font = f, bg = "lightgreen")
lab_temp.place(x=350, y=450)
lab_tans = Label(root, text = "", font = f, bg = "lightgreen")
lab_tans.place(x=525, y=450)

temp = "https://api.openweathermap.org/data/2.5/weather?q=mumbai&appid=c6e315d09197cec231495138183954bd&units=metric"
res = requests.get(temp)
data= res.json()
temp = data["main"]["temp"]
lab_tans.configure(text=temp)
	

# Add Window
aw = Toplevel(root)
aw.title("Add Employee")
aw.geometry("600x500+50+50")
aw.configure(bg = "lightblue")

aw_lab_id = Label(aw, text = "Enter Id", font = f, bg = "lightblue")
aw_lab_id.pack(pady = 10)
aw_ent_id = Entry(aw, font = f, bd = 2)
aw_ent_id.pack()
aw_lab_name = Label(aw, text = "Enter Name", font = f, bg = "lightblue")
aw_lab_name.pack(pady = 10)
aw_ent_name = Entry(aw, font = f, bd = 2)
aw_ent_name.pack()
aw_lab_sal = Label(aw, text = "Enter Salary", font = f, bg = "lightblue")
aw_lab_sal.pack(pady = 10)
aw_ent_sal = Entry(aw, font = f, bd = 2)
aw_ent_sal.pack()

aw_btn_save = Button(aw, text = "Save", width = 10, font = f, command = add_save)
aw_btn_save.pack(pady = 10)

aw_btn_back = Button(aw, text = "Back", width = 10, font = f, command = add_back)
aw_btn_back.pack(pady = 10)

aw.withdraw()

# View Window
vw = Toplevel(root)
vw.title("View Employee")
vw.geometry("600x500+50+50")
vw.configure(bg = "orange1")

vw_st_data = ScrolledText(vw, width = 40, height = 12, font = f, bg = "orange1")
vw_st_data.pack(pady = 10)
vw_btn_back = Button(vw, text = "Back", font = f, command = view_back)
vw_btn_back.pack(pady = 10)

vw.withdraw()

# Update Window
uw = Toplevel(root)
uw.title("Update Employee")
uw.geometry("600x500+50+50")
uw.configure(bg = "LightPink1")

uw_lab_id = Label(uw, text = "Enter Id", font = f, bg = "LightPink1")
uw_lab_id.pack(pady = 10)
uw_ent_id = Entry(uw, font = f, bd = 2)
uw_ent_id.pack()
uw_lab_name = Label(uw, text = "Enter Name", font = f, bg = "LightPink1")
uw_lab_name.pack(pady = 10)
uw_ent_name = Entry(uw, font = f, bd = 2)
uw_ent_name.pack()
uw_lab_sal = Label(uw, text = "Enter Salary", font = f, bg = "LightPink1")
uw_lab_sal.pack(pady = 10)
uw_ent_sal = Entry(uw, font = f, bd = 2)
uw_ent_sal.pack()

uw_btn_save = Button(uw, text = "Save", width = 10, font = f, command = update_save)
uw_btn_save.pack(pady = 10)

uw_btn_back = Button(uw, text = "Back", width = 10, font = f, command = update_back)
uw_btn_back.pack(pady = 10)

uw.withdraw()
		
# Delete Window
dw = Toplevel(root)
dw.title("Delete Employee")
dw.geometry("600x500+50+50")
dw.configure(bg = "RoyalBlue1")

dw_lab_id = Label(dw, text = "Enter Id", font = f, bg = "RoyalBlue1")
dw_lab_id.pack(pady = 10)
dw_ent_id = Entry(dw, font = f, bd = 2)
dw_ent_id.pack()

dw_btn_save = Button(dw, text = "Save", width = 10, font = f, command = delete_save)
dw_btn_save.pack(pady = 10)

dw_btn_back = Button(dw, text = "Back", width = 10, font = f, command = delete_back)
dw_btn_back.pack(pady = 10)

dw.withdraw()
 
root.mainloop()