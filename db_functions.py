import sqlite3
import sys



################## Подключение к базе SQLite ##################

try:
	db = sqlite3.connect('bd/birthdays.db', check_same_thread = False)
	sql = db.cursor()

except Exception as e:
	print(f"Error: {e}")
	sys.exit(1)

###############################################################




############ Добавление нового пользователя в базу ############

def new_user(user_id):
	try:
		sql.execute('SELECT * FROM users WHERE id = ?', (user_id, ))
		_user = sql.fetchone()
		if _user is None:
			sql.execute('INSERT INTO users VALUES (?, ?, ?)', (user_id, 'menu', None))
			db.commit()

	except Exception as e:
		print(f'Error: {e}')

###############################################################



################ Смена языка интерфейса #######################

def lang_change(user_id, lang):
	try:
		sql.execute('UPDATE users SET language = ? WHERE id = ?', (lang, user_id))
		db.commit()

	except Exception as e:
		print(f'Error: {e}')

###############################################################



################ Получение языка интерфейса ###################
 
def lang_get(user_id):
	try:
		sql.execute('SELECT language FROM users WHERE id = ?', (user_id, ))
		language = sql.fetchone()
		if language is None:
			return None

		return language[0]

	except Exception as e:
		print(f'Error: {e}')

###############################################################



###################### Смена состояния ########################

def state_change(user_id, state):
	try:
		sql.execute('UPDATE users SET state = ? WHERE id = ?', (state, user_id))
		db.commit()

	except Exception as e:
		print(f'Error: {e}')

###############################################################



################### Получение состояния #######################

def state_get(user_id):
	try:
		sql.execute('SELECT state FROM users WHERE id = ?', (user_id, ))
		return sql.fetchone()[0]

	except Exception as e:
		print(f'Error: {e}')

###############################################################



################# Получение кода маркета ######################

def code_get(sap_id):
	try:
		sql.execute('SELECT code FROM stores WHERE sap_id = ?', (sap_id, ))
		code = sql.fetchone()
		if code is None:
			return code

		return code[0]

	except Exception as e:
		print(F'Error: {e}')

############################################################### 

def name_and_group_get(current_date):
	try:
		db = sqlite3.connect('bd/birthdays.db', check_same_thread=False)
		sql = db.cursor()

	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)

	try:
		#sql.execute('SELECT * FROM birthdays WHERE SUBSTR(date_, 1,2) = "17" AND SUBSTR(date_, 4,2) = "10"')
		sql.execute(f"SELECT * FROM birthdays WHERE SUBSTR(date_, 1,5) = {str(current_date)}")
		names = sql.fetchall()
		if names is None:
			return names

		return names

	except Exception as e:
		print(F'Error: {e}')