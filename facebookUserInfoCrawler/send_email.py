#import os
import zipfile
import smtplib
from email import encoders
#from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart   

def zip_file(file):
	# zf =zipfile.ZipFile("tutor.zip", 'w')
	# zf.write("tutor.py")
	name = file.split("\\.")[0]
	with zipfile.ZipFile(name + ".zip", 'w') as new_zip:
		new_zip.write(file)
	return name + ".zip"

def send_zipfile(zipped_file, recipient, sender = "python@pythonmail.com"):
	themsg = MIMEMultipart()
	themsg['Subject'] = "file " + zipped_file
	themsg['To'] = recipient
	#themsg.preamble = 'I am not using a MIME-aware mail reader.\n'
	with open(zipped_file, 'rb') as fp:
		msg = MIMEBase('application', 'zip')
		msg.set_payload(fp.read())
	encoders.encode_base64(msg)
	themsg.attach(msg)

	fromaddr = 'ufchemistry111@gmail.com'
	toaddrs  = 'alexgre@ufl.edu'
	debuglevel = 0
	smtp = smtplib.SMTP()
	smtp.set_debuglevel(debuglevel)
	smtp = smtplib.SMTP('smtp.gmail.com:587')
	smtp.ehlo()
	smtp.starttls()
	smtp.login("ufchemistry111@gmail.com", "gator123456")
	smtp.sendmail(fromaddr, toaddrs, themsg.as_string())
	smtp.quit()


def main():
	file = "test1.py"
	zipped_file = zip_file(file)
	send_zipfile(zipped_file, "alexgre@ufl.edu")

if __name__ == '__main__':
	main()