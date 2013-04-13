class User:
# state represents the board, next piece to be played, and other relevant info
    def __init__(self, user_id, friends, tickets):
    	self.user_id = user_id
    	self.friends = friends
    	self.tickets = tickets

    def get_balance(self):
    	balance = 0
    	for ticket in tickets:
    		balance = balance + ticket.get_value()
    	return balance
    
class Ticket:
	def __init__(self, id, label, value, date, user, active):
		self.id = id
		self,label = label
		self.value = value
		self.date = date
		self.user = users

	def get_value(self):
		return self.value()

	def get_date(self):
		return self.date()

	def get_label(self):
		return self.label()

	def get_users(self):
		return self.users()

class Label:
	def __init__(self, image, title, description):
		self.image = image
		self.title = title
		self.description = description

	def get_image(self):
		return self.image

	def get_title(self):
		return self.title

	def get_description(self):
		return self.description





    

# end of program
