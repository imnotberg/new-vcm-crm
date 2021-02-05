from datetime import datetime

LEAD_STATUS = []

NOTECHOICES = []

YEAR_CHOICES = [('','')] + [(x,x) for x in range(2016,datetime.now().year+1)]
EMAIL_TEMPLATES = [('','')]

def get_value(value):
	try:
		return value[0]
	except:
		return None
login_url = 'contact_management:login'