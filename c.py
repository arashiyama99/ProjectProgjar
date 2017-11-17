import socket
import select
import sys
import getpass
import MySQLdb
#from cryptography.fernet import Fernet

#GLOBAL Variable
#username = 'null'
#password = 'null'
#/

def conn(sql):
	#localhost,root,password,nama data base
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor = db.cursor()
	cursor.execute(sql)
	db.commit()
	db.close()

#masuk akun
def login(username, password):
	#print "Login Akun"
	#username = raw_input ("username akun : ")
	#password = getpass.getpass ("masukan password : ")
	cek = cekpwd(username, password)
	if cek == 0:
		return 0
	else :
		loginstatus(username, password)
		return 1

#menambah satu akun
def daftar():
	print "Daftar Akun Baru"
	username = raw_input ("username akun : ")
	password = getpass.getpass ("masukan password : ")
	sql ="INSERT INTO users (username,password,status) VALUES ('%s','%s',0)"%(username, password)
	sql2 = "UPDATE users set pin_user = FLOOR( 1 + RAND( ) *100000 ) where username = '%s'"%(username)
	conn(sql)
	conn(sql2)

#menemukan pengguna yang online
def cekstatus():
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor =db.cursor()
	#mencari status pada db yang bernilai satu
	sql ="SELECT username FROM users WHERE status = 1"
	cursor.execute(sql)
	cek = cursor.fetchall()
	for row in cek:
		#mencetak semua yang online
		print row[0] + ' online'

def cekprofile(username):
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor =db.cursor()
	#mencari status pada db yang bernilai satu
	sql ="SELECT username, pin_user FROM users WHERE username = '%s' "%(username)
	cursor.execute(sql)
	cek = cursor.fetchall()
	for row in cek:
		#mencetak semua yang online
		print 'username : ', row[0]
		print 'user pin : ', row[1]

 #merubah status menjadi offline
def logoutstatus(username, password):
	sql="UPDATE users SET status = 0 WHERE username = '%s' AND password = '%s'" %(username, password)
	conn(sql)

#merubah status menjadi online
def loginstatus(username, password):
	sql="UPDATE users SET status = 1 WHERE username = '%s' AND password = '%s'" %(username, password)
	conn(sql)

#cek ketersediaan akun
def cekpwd(username, password):
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor =db.cursor()
	sql ="SELECT * FROM users WHERE username = '%s' AND password = '%s'"%(username, password)
	cursor.execute(sql)
	cek = cursor.rowcount
		#jika ditemukan satu akun
	if cek == 1:
		return 1
	else:
		return 0

def private(kode, username):
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor =db.cursor()
	sql ="SELECT pin_user FROM users WHERE username='%s'"%(username)
	cursor.execute(sql)
	cek = cursor.fetchall()
	for row in cek:
		finalpin = row[0]

	if str(finalpin) == str(kode) :
		return 1
	else :
		return 0

def privatestatus(kode,username,password):
	sql="UPDATE users SET private = '%s' WHERE username = '%s' AND password = '%s'" %(kode,username, password)
	conn(sql)
	chatprivate(kode)
 
def chatprivate(kode):
	message = sys.stdin.readline()
	while message != ('quit'):
		message = sys.stdin.readline()
		message2 = kode+"$"+"<"+ username+"> " + message
		server.send(message2)
		sys.stdout.write("P~<You>")
		sys.stdout.write(message)
		sys.stdout.flush()
 
#MAIN PROGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print "Correct usage: script, IP address, port number"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])


flag1= False
flag2= False

while True:
	print "\n1. Login"
	print "2. Daftar"
	print "3. Keluar"
	pilihan = raw_input ("Masukan pilihan : ")
	if pilihan == "2":
		daftar()
		
	elif pilihan == "1":
		print "silahkan login"
		username = raw_input ("username akun : ")
		password = getpass.getpass ("masukan password : ")
		cek = login(username, password)
		if cek == 1:
			#loginstatus()
			server.connect((IP_address, Port))
			while True:
				sockets_list = [sys.stdin, server]
				read_sockets,write_socket, error_socket = select.select(sockets_list, [], [])
				for socks in read_sockets:
					if socks == server:
						message = socks.recv(2048)
						test = message
						priv, sisa = test.split("$")
						if priv == "private":
							kode, test2 = sisa.split(">")
							#print kode, test2
							cek = private(kode, username)
							if cek == 1:
								print test2
							else :
								break
						else :
							print message
					else:
						message = sys.stdin.readline()
						if message == 'logout\n':
							print "berhasil logout"
							server.send(username + " offline")
							logoutstatus(username, password)
							exit()


							#break #kembali ke menu pilihan
						elif message == 'status\n':
							cekstatus()
						elif message == 'profile\n':
							cekprofile(username)
						elif message == 'private\n':
							kode = raw_input("masukan kode private chat : ")			
							message = raw_input("masukan pesan : ")
							messagefinal = "private$" + kode +">"+ message
							server.send(messagefinal)
							#private(kode, message)
						else :
							message2 = "<"+ username+">$ " + message
							server.send(message2)
							sys.stdout.write("<You>")
							sys.stdout.write(message)
							sys.stdout.flush()
	elif pilihan =="3":
		print "terimakasih , anda telah keluar sistem"
		exit()
	else:
		print "pilihan salah, silahkan pilih lagi "
server.close()
