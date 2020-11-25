import socket
import sys
import argparse
import requests
from bs4 import BeautifulSoup
max_byte=65500
class server:
	def __init__(self,host,port):
		self.host=host
		self.port=port

	def connect(self):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		sock.bind((self.host,self.port))
		sock.listen(1)
		print("listening at",sock.getsockname())
		while True:
			sc,sockname=sock.accept()
			print("We have acccepted a connection from",sockname)
			
			data=sc.recv(max_byte)
			print("incoming url is:",data.decode("utf-8"))
			mes=data.decode("utf-8")

			img_count=self.count_img(mes)
			leaf_count=self.leaf(mes)
			
			data="The number of image is:"+ str(img_count)+"\n"+"The number of leaves is:"+str(leaf_count)
			sc.sendall(data.encode("utf-8"))
			sc.close()


	def count_img(self,url_adr):
		page=requests.get(url_adr)
		
		sp=BeautifulSoup(page.text,'html.parser')
		count=0
		imgs=sp.find_all("img")
		for i in imgs:
			count+=1
		return count

	def leaf(self,url_adr):
		page=requests.get(url_adr)
		sp=BeautifulSoup(page.text,'html.parser')
		count=0
		lf=sp.find_all('p')
		for i in lf:
			if not i.find_all('p'):
				count+=1

		return count




class client:
	def __init__(self,host,port):
		self.host=host
		self.port=port

	def connect(self,url_addr):
		sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect((self.host,self.port))

		print("Client is assigned socketname:",sock.getsockname())
		sock.sendall(url_addr.encode('utf-8'))
		mes=sock.recv(max_byte).decode("utf-8")

		print(mes)
		sock.close()


if __name__=="__main__":
	choices={'client':client,'server':server}
	parser=argparse.ArgumentParser()
	parser.add_argument('role',choices=choices)
	parser.add_argument('-i',type=str,default='127.0.0.1')
	parser.add_argument('-p',type=int,default=1060)
	if sys.argv[1]=="client":
		parser.add_argument("url",type=str)
	args=parser.parse_args()
	if args.role=="server":
		server(args.i,args.p).connect()
	elif args.role=="client":
		client(args.i,args.p).connect(args.url)
	
	
