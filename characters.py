import numpy as np
import time
from inputchar import *
import random
from Items import *
import subprocess
BulletList=[]
Stomp='./smb_stomp.wav'
Die='./smb_mariodie.wav'
#By default all the characters are a 2X1 matrix
class Person:
	def __init__(self,charHeady):
		self.heady = charHeady

class Player(Person):
	def __init__(self,charHeadx,charHeady,index):
		Person.__init__(self,charHeady)
		self.headx = charHeadx
		self.index=index
		self.__Gun=0

	def shoot(self):
		bullet=Bullet(self.headx,self.heady)
		BulletList.append(bullet)

	def changeGunStatus(self):
		self.__Gun=1

	def useGunVar(self):
		return self.__Gun

class Enemy(Person):
	def __init__(self, charHeady, Dir):
		Person.__init__(self,charHeady)
		self.headx = 15
		if Dir == 1:
			self.move = 1
		elif Dir == 0:
			self.move = 0
		else:
			self.move = -1
		self.time=time.time()
	def Build(self,obj,EnemyList):
		if obj.Gamepad[self.headx][self.heady] != chr(9608): 
			if self in EnemyList:
				obj.Gamepad[self.headx][self.heady] = "~"
				obj.Gamepad[self.headx+1][self.heady] = "*"
				
	def remove(self,obj):
		if obj.Gamepad[self.headx][self.heady] != chr(9608): 
			obj.Gamepad[self.headx][self.heady] = " "
			obj.Gamepad[self.headx+1][self.heady] = " "

	def movement(self,obj,Mario,EnemyList,PitList,Score,Lives):
		temp=0
		if (self.headx == Mario.headx+2 and self.heady == Mario.heady) or (self.headx == Mario.headx+2 and self.heady == Mario.heady+1) or (self.headx == Mario.headx+2 and self.heady == Mario.heady-1) and self in EnemyList:
				try:
					EnemyList.pop(EnemyList.index(self))
				except: ValueError
				subprocess.Popen(['aplay','-q',Stomp])
				temp=1
		b=time.time()
		
		if obj.Gamepad[self.headx][self.heady+1] != chr(9608) and self.move == 1 and self.heady+1<230:
			self.heady+=1
			if obj.Gamepad[self.headx][self.heady] == "^" and self in EnemyList:
				Lives[0]-=1
				subprocess.Popen(['aplay','-q',Die])
				for i in range(Mario.heady-10,Mario.heady):
					if obj.Gamepad[Mario.headx][i] == " " and obj.Gamepad[Mario.headx+1][i] == " ":
						Mario.heady=i
						Mario.index=i-5
						break
				
		elif obj.Gamepad[self.headx][self.heady+1] == chr(9608) and self.move == 1:
			self.move = 0
		elif obj.Gamepad[self.headx][self.heady-1] != chr(9608) and self.move == 0:
			self.heady-=1
			if obj.Gamepad[self.headx][self.heady] == "^" and self in EnemyList:
				Lives[0]-=1
				subprocess.Popen(['aplay','-q',Die])
				for i in range(Mario.heady-10,Mario.heady):
					if obj.Gamepad[Mario.headx][i] == " " and obj.Gamepad[Mario.headx+1][i] == " ":
						Mario.heady=i
						Mario.index=i-5
						break
		else:
			self.move = 1

		if temp==1:
			return 2
		else: 
			return 0

class BossEnemy(Enemy):
	def __init__(self):
		Enemy.__init__(self,200,-1)
		self.headx=14
		self.__time = time.time()
		self.__hits=4
		self.alive=1
		self.bullet_list=[]

	def Build(self,obj):
		obj.Gamepad[self.headx][self.heady] = "~"
		obj.Gamepad[self.headx+1][self.heady] = "E"
		obj.Gamepad[self.headx+2][self.heady] = "E"

	def movement(self,obj,Mario,Lives):
		if Mario.heady == self.heady and self.alive == 1:
			Lives[0] -= 1
			subprocess.Popen(['aplay','-q',Die])
		b = time.time()
		if b-self.__time >= 2 and self.__hits>0:
			a = random.randint(9,14)
			obj.Gamepad[self.headx][self.heady] = " "
			obj.Gamepad[self.headx+1][self.heady] = " "
			obj.Gamepad[self.headx+2][self.heady] = " "
			self.headx = a
			obj.Gamepad[self.headx][self.heady] = "~"
			obj.Gamepad[self.headx+1][self.heady] = "E"
			obj.Gamepad[self.headx+2][self.heady] = "E"
			if Mario.heady >= 190:
				Fire=BossBullet(self.headx,self.heady)
				self.bullet_list.append(Fire)
			self.time = time.time()

	def completelyRemove(self,obj,Begin):
		obj.Gamepad[self.headx][self.heady] = " "
		obj.Gamepad[self.headx+1][self.heady] = " "
		obj.Gamepad[self.headx+2][self.heady] = " "
		self.alive=0
		for bullet in self.bullet_list:
			obj.Gamepad[bullet.headx][bullet.heady] = " "
		Begin.setScore(100)

	def hitCheck(self,BulletList,obj,Begin):
		for bullet in BulletList:
			if bullet.headx==self.headx or bullet.headx==self.headx+1 or bullet.headx==self.headx+2:
				if bullet.heady==self.heady or bullet.heady+1==self.heady:
					self.__hits-=1
					print(self.__hits)
					if self.__hits==0:
						self.completelyRemove(obj,Begin)  
