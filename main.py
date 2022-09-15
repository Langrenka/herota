import sqlite3
from tkinter import *
from tkinter import messagebox

insert_sql = "insert into accounts (login, passwords, role) values (?, ?, ?);"

def updqte_dump():
	#db.commit()
	db = sqlite3.connect('persons.db')
	db.commit()
	sql = db.cursor()
	sql.execute("SELECT * FROM accounts")
	records = sql.fetchall()

	row = records[0]

	update_sql = f"update accounts set id = {row[0]},login = \'log\',passwords = {row[2]},role = {row[3]} where id = {row[0]}"

	sql.execute(update_sql)
	db.commit()
	print('lol')

def get_persons(frame, var_height):
	persons_list = Listbox(frame, width = 85, height = var_height, font=('Roboto', 10), selectmode = SINGLE)
	scrollbar_bt = Scrollbar(frame)
	scrollbar_bt.config(command=persons_list.yview)
	scrollbar_bt.pack(side=RIGHT, fill=Y)
	db = sqlite3.connect('persons.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS accounts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		login TEXT,
		passwords TEXT,
		role TEXT
		)""")

	db.commit()
	sql.execute("SELECT * FROM accounts")
	records = sql.fetchall()
	for row in records:
		string = 'id: '+ str(row[0]) + ' | login: '+row[1].ljust(10, ' ')+' | password: ' + row[2].ljust(10, ' ') + ' | adm: ' + row[3]
		persons_list.insert(END, string)
	return persons_list

def get_stuff(frame, var_height):
	stuff_list = Listbox(frame, width = 85, height = var_height, font=('Roboto', 10))
	scrollbar_tp = Scrollbar(frame)
	scrollbar_tp.config(command=stuff_list.yview)
	scrollbar_tp.pack(side=RIGHT, fill=Y)
	return stuff_list

def success_auth(root, var_log):
	root.title("Главная страница")
	root.geometry('800x600')
	root.resizable(width=False, height=False)
	canvas.destroy()
	header_frame.destroy()
	title.destroy()
	basic_frame.destroy()
	login_name.destroy()
	login_input.destroy()
	pass_name.destroy()
	pass_input.destroy()
	btn_auth.destroy()
	btn_reg.destroy()

	if check_adm(var_log) == 0:
		top_frame = Frame(root, width=600, height=280)
		top_frame.pack(anchor = 'e', pady = 10, padx = 10)
		bottom_frame = Frame(root, width=600, height=280)
		bottom_frame.pack(anchor = 'e', pady = 10, padx = 10)
		get_persons(bottom_frame, 15).pack(side = LEFT)
		get_stuff(top_frame, 15).pack(side = LEFT)
		btn_frame_top = Frame(root, bg='red', width = 50, height = 50).pack()

	else:
		top_frame = Frame(root, bg = 'red', width=600, height=580)
		top_frame.pack(anchor = 'e', pady = 10, padx = 10)
		get_stuff(top_frame, 33).pack(side = LEFT)


def create_string_bd(var_log, var_pass, var_role):
	db = sqlite3.connect('persons.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS accounts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		login TEXT,
		passwords TEXT,
		role TEXT
		)""")
	var_id = None
	db.commit()
	sql.execute("SELECT * FROM accounts WHERE login=?", (var_log,))
	if sql.fetchone() is None:
		sql.execute(f"INSERT INTO accounts VALUES (?, ?, ?, ?)", (var_id, var_log, var_pass, var_role))
		db.commit()
		messagebox.showinfo("Успех", "Пользователь успешно зарегистрирован")
		return 0
	else:
		messagebox.showerror("Ошибка", "Пользователь с таким логином уже зарегистрирован")
		return 1

def check_person_bd(var_log, var_pass):
	db = sqlite3.connect('persons.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS accounts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		login TEXT,
		passwords TEXT,
		role TEXT
		)""")
	db.commit()
	sql.execute(f"SELECT login, passwords FROM accounts WHERE login = '{var_log}' AND passwords = '{var_pass}'")
	if sql.fetchone() is None:
		messagebox.showerror("Ошибка", "Пользователь не зарегистрирован/неправильно введены данные")
		return 1
	else:
		if check_adm(var_log) == 1:
			messagebox.showinfo("Успех", "Вы авторизовались как обычный пользователь")
		elif check_adm(var_log) == 0:
			messagebox.showinfo("Успех", "Вы авторизовались как администратор")
		return 0

def check_role(adm_pass):
	if adm_pass == '123':
		return 1
	else:
		return 0

def check_adm(var_log):
	db = sqlite3.connect('persons.db')
	sql = db.cursor()
	sql.execute("""CREATE TABLE IF NOT EXISTS accounts (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		login TEXT,
		passwords TEXT,
		role TEXT
		)""")
	db.commit()
	sql.execute(f"SELECT login, role FROM accounts WHERE login = '{var_log}' AND role = '1'")
	if sql.fetchone() is None:
		return 1
	else:
		return 0
#==============================================================================================================
def reg_open():
	root2 = Toplevel(root)
	root2.title("Регистрация")
	root2.geometry('400x600')
	root2.resizable(width=False, height=False)
	root2.grab_set()
	root2.focus_set()

	header_frame2 = Frame(root2)
	header_frame2.place(height = 150, width=400)

	title2 = Label(header_frame2, text='Регистрация', font=('Roboto', 20, 'bold'), height=4, anchor='s')
	title2.pack()

	basic_frame2 = Frame(root2)
	basic_frame2.place(y=150, height=350, width=400)

	login_name2 = Label(basic_frame2, text='Придумайте логин:', font=('Roboto, 10'), width=27, anchor='w')
	login_name2.pack()
	login_input2 = Entry(basic_frame2, font=('Roboto, 14'))
	login_input2.pack()

	pass_name2 = Label(basic_frame2, text='Придумайте пароль:', font=('Roboto, 10'), width=27, height=2, anchor='sw')
	pass_name2.pack()
	pass_input2 = Entry(basic_frame2, font=('Roboto, 14'))
	pass_input2.pack()


	double_pass_name2 = Label(basic_frame2, text='Повторите пароль:', font=('Roboto, 10'), width=27, height=2, anchor='sw')
	double_pass_name2.pack()
	double_pass_input2 = Entry(basic_frame2, font=('Roboto, 14'))
	double_pass_input2.pack()


	adm_pass_name2 = Label(basic_frame2, text='Пароль администратора:', font=('Roboto, 10'), width=27, height=2, anchor='sw')
	adm_pass_name2.pack()
	adm_pass_input2 = Entry(basic_frame2, font=('Roboto, 14'), show = '*')
	adm_pass_input2.pack()

	def check_reg():
		nonlocal pass1, pass2, log, adm
		pass1 = pass_input2.get()
		pass2 = double_pass_input2.get()
		log = login_input2.get()
		adm = adm_pass_input2.get()
		if (pass1 != "" and pass2 != "" and log != ""):
			if (pass1 == pass2):
				if create_string_bd(log, pass2, check_role(adm)) == 0:
					root2.destroy()
			else:
				messagebox.showwarning("Ошибка", "Введенные пароли не совпадают")
	
	btn_reg2 = Button(basic_frame2, text='Зарегистрироваться', font=('Roboto, 15'), relief=GROOVE, width=19, command = check_reg)
	btn_reg2.pack(pady = 20)

	pass1 = None
	pass2 = None
	log = None
	adm = None
#=============================================================================================================================
root = Tk()
root.title("Авторизация")
root.geometry('400x600')
root.resizable(width=True, height=False)
root.minsize(400,600)
root.maxsize(800,600)

canvas = Canvas(root, width = 300, height = 150)
canvas.place(x=650,y=0)
pic = PhotoImage(file = 'bird.png')
canvas.create_image(0,0, anchor='nw', image = pic)


header_frame = Frame(root)
header_frame.place(height = 150, width=400)
title = Label(header_frame, text='Авторизация', font=('Roboto', 20, 'bold'), height=4, anchor='s')
title.pack()

basic_frame = Frame(root)
basic_frame.place(y=200, height=220, width=400)

login_name = Label(basic_frame, text='Введите логин:', font=('Roboto, 10'), width=27, anchor='w')
login_name.pack()
login_input = Entry(basic_frame, font=('Roboto, 14'))
login_input.pack()
pass_name = Label(basic_frame, text='Введите пароль:', font=('Roboto, 10'), width=27, height=2, anchor='sw')
pass_name.pack()
pass_input = Entry(basic_frame, font=('Roboto, 14'), show='*')
pass_input.pack()

def check_auth():
	var_log = login_input.get()
	var_pass = pass_input.get()
	if (var_log != "" and var_pass != ""):
		if check_person_bd(var_log, var_pass) == 0:
			success_auth(root, var_log)

btn_auth = Button(basic_frame, text='Войти', font=('Roboto, 15'), relief=GROOVE, width=19, command = check_auth)
btn_auth.pack(pady = 20)
btn_reg = Button(basic_frame, text='Регистрация', font=('Roboto, 10'), relief=GROOVE, width=19, height = 1, command=reg_open)
btn_reg.pack(side = BOTTOM)


root.mainloop()
#===================================================================
