from parkingSystemAutomation import cursor,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	print('MADARCHOD')
	query = 'Select * from User where id='+str(user_id) + ';'
	cursor.execute(query)
	print(query)
	user = cursor.fetchall()
	b = Behnchod(user[0][1],user[0][0],True)
	return b

class Behnchod(UserMixin):
	def __init__(self, name, id, active=True):
		self.name = name
		self.id = id
		self.active = active

	def is_active(self):
	# Here you should write whatever the code is
	# that checks the database if your user is active
		return self.active

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True