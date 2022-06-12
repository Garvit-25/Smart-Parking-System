from parkingSystemAutomation import cursor,login_manager,app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
	query = 'Select * from User where id='+str(user_id) + ';'
	cursor.execute(query)
	# print(query)
	user = cursor.fetchall()
	# print(user)
	u = User(user[0][0],user[0][1], user[0][2], True)
	return u

class User(UserMixin):
	def __init__(self, id, username, email, active=True, admin=False):
		self.id = id
		self.username = username
		self.email = email
		self.active = active
		self.admin = admin

	def is_active(self):
	# Here you should write whatever the code is
	# that checks the database if your user is active
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True
		
	def is_admin(self):
		return self.admin
		
# class Company(UserMixin):
# 	def __init__(self, id, username, email, active=True):
# 		self.id = id
# 		self.username = username
# 		self.email = email
# 		self.active = active

# 	def is_active(self):
# 	# Here you should write whatever the code is
# 	# that checks the database if your user is active
# 		return True

# 	def is_anonymous(self):
# 		return False

# 	def is_authenticated(self):
# 		return True