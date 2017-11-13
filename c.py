import socket
import select
import sys
import getpass
import MySQLdb
from cryptography.fernet import Fernet

#GLOBAL Variable
username = 'null'
password = 'null'
#/

def conn(sql):
	#localhost,root,password,nama data base
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
    cursor =db.cursor()
    cek = cursor.execute(sql)
    if cek :
    	db.commit()
    else :
    	print "query gagal dieksekusi"
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

 #merubah status menjadi offline
def logoutstatus():
	sql="UPDATE users SET status = 0 WHERE username = '%s' AND password = '%s'" %(username, password)
    conn(sql)

#merubah status menjadi online
def loginstatus():
    sql="UPDATE users SET status = 1 WHERE username = '%s' AND password = '%s'" %(username, password)
    conn(sql)

#cek ketersediaan akun
def cekpwd():
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

def private():
	db = MySQLdb.connect("localhost", "root", "password","TESTDB")
	cursor =db.cursor()
	sql ="SELECT private FROM users WHERE username = '%s' AND password = '%s'"%(username, password)
	cursor.execute(sql)

#MAIN PROGRAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
	print "Correct usage: script, IP address, port number"
	exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])

while True:
	print "1. Login\n"
	print "2. Daftar\n"
	pilihan = raw_input ("Masukan pilihan : ")
	if pilihan == "2":
		daftar()
	cek = login()
	server.connect((IP_address, Port))

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
						private()
					else :
	    				message2 = "<"+ username+"> " + message
            				server.send(message2)
            				sys.stdout.write("<You>")
            				sys.stdout.write(message)
            				sys.stdout.flush()
server.close()
