import win32com.client as client
import pyinputplus as pyip
import inflect
from datetime import date
from dotenv import load_dotenv
import os

load_dotenv()
domain = os.environ.get("DOMAIN")
class User:
	def __init__(self, userName, userAlias, mirrorName, mirrorAlias, suite, startDate):
		self.userName = userName
		self.userAlias = userAlias
		self.mirrorName = mirrorName
		self.mirrorAlias = mirrorAlias
		self.suite = suite
		self.startDate = startDate

def initPrompt():
	num = pyip.inputInt('How many people are starting?\n')
	return num
def UserGen(number):
	check = 'no'
	while check == 'no':
		userList = [] 
		p = inflect.engine()
		for x in range(number):
			name = pyip.inputStr('What is the name of the {} person?\n'.format(p.ordinal(x+1)))
			alias = pyip.inputStr('What is {}\'s alias?\n'.format(name))
			suite = pyip.inputStr('What suite is {} going to be in?\n'.format(name))
			startdate = pyip.inputDate('When is their start date? (month/date)\n', formats=['%m/%d'])
			mirrorname = pyip.inputStr('Who should {} mirror? \n'.format(name))
			mirroralias =  pyip.inputStr('What is {}\'s alias?\n'.format(mirrorname))
			userList.append(User(name.title(),alias, mirrorname.title(), mirroralias, suite, startdate.strftime('%m/%d')))
		for x in range(len(userList)):
			print('{} ({}@{}.org) is starting on {} in {}\'s suite and their account will mirror {} ({}@{}.org)\n'.format(userList[x].userName, userList[x].userAlias, domain, userList[x].startDate,userList[x].suite, userList[x].mirrorName,userList[x].mirrorAlias, domain ))
		check = pyip.inputYesNo('Does this look correct?\n')
		if check == 'yes':
			print('Now sending emails......\n\n')
		else:
			print('Restarting user entry......\n\n')
	return userList

def Emailer(userlist):
	outlook = client.Dispatch('Outlook.Application')
	today = date.today()
	emailDomain= '@{}.org'.format(domain)
	Help = 'help'+ emailDomain
	signature = '- ' + str(outlook.Session.Accounts[0].CurrentUser)
	for x in range(3):
		message = outlook.CreateItem(0)
		message.CC = Help
		message.Subject = 'New Hires ' + today.strftime("%m/%d")
		if x == 0:
			message.To = 'efactshelp@{}.zendesk.com'.format(domain)
			message.Body = 'hello\n\n'+ signature
			message.Display()
		elif x == 1:
			message.To = '{}'.format(os.environ.get("LIBRARY")) + emailDomain
			message.Body = 'hello\n\n'+signature
			message.Display()
		else:
			message.To = 'OSCA-helpdesk'+ emailDomain
			message.CC = message.CC + '; {}'.format(os.environ.get("OIT"))+emailDomain
			message.Body = 'hello\n\n'+signature
			message.Display()


def main():
	num = initPrompt()
	userList= UserGen(num)
	Emailer(userList)


if __name__ == "__main__":
	main()

