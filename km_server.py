from threading import Thread
from time import sleep
import socket

ks=socket.socket()
host=socket.gethostname()
kport=8096
ks.bind((host,kport))
ks.listen(5)
kcon=0

ms=socket.socket()
mport=8095
ms.bind((host,mport))
ms.listen(5)
mcon=0
	
gs=socket.socket()
gport=8094
gs.bind((host,gport))
gs.listen(5)
gcon=0


def log(str):
	with open("km_log.txt","a") as logfile:
		logfile.write(str+"\n")
	
def sendto(conn,st):
	if conn!=0:
		try:
			conn.send(st+'~')
		except Exception, e:
			conn=0
			# print str(e)


def listen_k():
	
	txt=""
	print "Waiting for connection from K..."
	while True:
		try:
			global kcon
			global mcon
			global gcon
			kcon,addr=ks.accept()
			print "K connected"
			log("K connected")
			
			if mcon!=0 and gcon!=0:
				sendto(mcon,'`cK')
				sendto(gcon,'`cK')
				sendto(kcon,'`oM')
				sendto(kcon,'`oG')
			elif mcon!=0:
				sendto(mcon,'`cK')
				sendto(kcon,'`oM')
			elif gcon!=0:
				sendto(gcon,'`cK')
				sendto(kcon,'`oG')

			while True:
				txt= kcon.recv(1024)
				print "from k :"+txt ##
				if txt.strip()=="":
					kcon.close()
					print "K disconnected"
					log("K disconnected")
					kcon=0
					sendto(mcon,'`dK')
					sendto(gcon,'`dK')
					break
				if txt[0]!="`":	log("K : "+txt)
				sendto(mcon,"K : "+txt)
				sendto(gcon,"K : "+txt)
					
		except Exception,e:
			# print str(e)
			try:
				sendto(mcon,'`dK')
				sendto(gcon,'`dK')
				log("K disconnected")
				kcon.close()
				kcon=0
			except Exception,e2:
				pass
				# print "e2",str(e2)

	
def listen_g():
	
	txt=""
	print "Waiting for connection from G..."
	while True:
		try:
			global kcon
			global mcon
			global gcon
			gcon,addr=gs.accept()
			print "G connected"
			log("G connected")
			
			if mcon!=0 and kcon!=0:
				sendto(mcon,'`cG')
				sendto(kcon,'`cG')
				sendto(gcon,'`oM')
				sendto(gcon,'`oK')
			elif mcon!=0:
				sendto(mcon,'`cG')
				sendto(gcon,'`oM')
			elif kcon!=0:
				sendto(kcon,'`cG')
				sendto(gcon,'`oK')

			while True:
				txt= gcon.recv(1024)
				print "from g :"+txt ##
				if txt.strip()=="":
					gcon.close()
					print "G disconnected"
					log("G disconnected")
					gcon=0
					sendto(mcon,'`dG')
					sendto(kcon,'`dG')
					break
				if txt[0]!="`":	log("G : "+txt)
				sendto(mcon,"G : "+txt)
				sendto(kcon,"G : "+txt)
					
		except Exception,e:
			# print str(e)
			try:
				sendto(mcon,'`dG')
				sendto(kcon,'`dG')
				log("G disconnected")
				gcon.close()
				gcon=0
			except Exception,e2:
				# print "e2",str(e2)
				pass


def listen_m():
	
	txt=""
	print "Waiting for connection from M..."
	while True:
		try:
			global kcon
			global mcon
			global gcon
			mcon,addr=ms.accept()
			print "M connected"
			log("M connected")
			
			if gcon!=0 and kcon!=0:
				sendto(gcon,'`cM')
				sendto(kcon,'`cM')
				sendto(mcon,'`oG')
				sendto(mcon,'`oK')
			elif gcon!=0:
				sendto(gcon,'`cM')
				sendto(mcon,'`oG')
			elif kcon!=0:
				sendto(kcon,'`cM')
				sendto(mcon,'`oK')

			while True:
				txt= mcon.recv(1024)
				print "from m :"+txt ##
				if txt.strip()=="":
					mcon.close()
					print "M disconnected"
					log("m disconnected")
					mcon=0
					sendto(gcon,'`dM')
					sendto(kcon,'`dM')
					break
				if txt[0]!="`":	log("M : "+txt)
				sendto(gcon,"M : "+txt)
				sendto(kcon,"M : "+txt)
					
		except Exception,e:
			# print str(e)
			try:
				sendto(gcon,'`dM')
				sendto(kcon,'`dM')
				log("M disconnected")
				mcon.close()
				mcon=0
			except Exception,e2:
				pass
				# print "e2",str(e2)
				



tk=Thread(target=listen_k,args=())
tm=Thread(target=listen_m,args=())
tg=Thread(target=listen_g,args=())

tk.start()
#t1.join()

tm.start()
tg.start()
#t2join()
