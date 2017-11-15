import socket
import select
import sys
import getpass
import MySQLdb
#from cryptography.fernet import Fernet
<<<<<<< HEAD

#GLOBAL Variable
username = 'null'
password = 'null'
#/

def conn(sql):
	#localhost,root,password,nama data base
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()
	db.close()

#masuk akun
def login():
	print "Login Akun"
	username = raw_input ("username akun : ")
	password = getpass.getpass ("masukan password : ")
	cek = cekpwd()
	if cek == 0:
		print "gagal login"
	else :
		return 1

#menambah satu akun
def daftar():
	print "Daftar Akun Baru"
	username = raw_input ("username akun : ")
	password = getpass.getpass ("masukan password : ")
	sql ="INSERT INTO users (id,username,password,status,grup,private) VALUES ('null','%s','%s',0,0,0)"%(username, password)
	conn(sql)
=======
>>>>>>> 3bcfe408e8d4c18447249861001d895b427c793e

#menemukan pengguna yang online
def cekstatus():
	db = MySQLdb.connect("localhost", "root", "","TESTDB")
        cursor =db.cursor()

        #mencari status pada db yang bernilai satu
        sql ="SELECT username FROM users WHERE status = 1"
        cursor.execute(sql)
	cek = cursor.fetchall()
	for row in cek:
		#mencetak semua yang online
		print row[0] + ' online'

 #merubah status menjadi offline
def logoutstatus(username, password):
	db = MySQLdb.connect("localhost", "root", "","TESTDB")
        cursor =db.cursor()
	sql="UPDATE users SET status = 0 WHERE username = '%s' AND password = '%s'" %(username, password)
        cursor.execute(sql)
	db.commit()

#merubah status menjadi online
def loginstatus(username, password):
	db = MySQLdb.connect("localhost", "root", "","TESTDB")
        cursor =db.cursor()
        sql="UPDATE users SET status = 1 WHERE username = '%s' AND password = '%s'" %(username, password)
        cursor.execute(sql)
	db.commit()

#cek ketersediaan akun
def cekpwd(username, password):
	db = MySQLdb.connect("localhost", "root", "","TESTDB")
	cursor =db.cursor()

	sql ="SELECT * FROM users WHERE username = '%s' AND password = '%s'"%(username, password)
	cursor.execute(sql)
	cek = cursor.rowcount
	
	if cek ==1:
		#jika ditemukan satu akun
		return 1
	else:
		return 0

<<<<<<< HEAD
def private(kode):
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor =db.cursor()
	sql ="SELECT * FROM users WHERE private = '%s'"%(kode)
	cursor.execute(sql)
 
#MAIN PROGRAM
=======
>>>>>>> 3bcfe408e8d4c18447249861001d895b427c793e
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print "Correct usage: script, IP address, port number"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

username = raw_input ("username : ")
password = getpass.getpass("password : ")
server.connect((IP_address, Port))

<<<<<<< HEAD
	if cek==1:
		loginstatus()
		while True:
	    		sockets_list = [sys.stdin, server]
	    		read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
	    		for socks in read_sockets:
	        		if socks == server:
	            			message = socks.recv(2048)
	            			print message
	        		else:
	            			message = sys.stdin.readline()
					if message == 'logout\n':
						print "berhasil logout"
						server.send(username + " offline")
						logoutstatus()
						break #kembali ke menu pilihan
					elif message == 'status\n':
						cekstatus()
					elif message == 'private\n':
						kode = raw_input("masukan kode private chat : ")
						private(kode)
					else :
						message2 = "<"+ username+"> " + message
						server.send(message2)
						sys.stdout.write("<You>")
						sys.stdout.write(message)
						sys.stdout.flush()
=======
a = cekpwd(username,password)
if a==0:
	print "gagal login"
else:
	loginstatus(username, password)
	while True:
    		sockets_list = [server]
    		read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
    		for socks in read_sockets:
        		if socks == server:
            			message = socks.recv(2048)
            			print message
        		else:
            			message = readline()
				if message == 'logout\n':
					print "berhasil logout"
					server.send(username + " offline")
					logoutstatus(username, password)
					exit()
				elif message == 'status\n':
					cekstatus()
				else :
	    				message2 = "<"+ username+"> " + message
            				server.send(message2)
            				sys.stdout.write("<Kamu>")
            				sys.stdout.write(message)
            				sys.stdout.flush()
>>>>>>> 3bcfe408e8d4c18447249861001d895b427c793e
server.close()
