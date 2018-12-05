import random
import math
class Cloud():
	def __init__(self, Position):
		self.__position = Position
		self.__height = random.randint(3,5)

	def Build(self,obj):
		obj.Gamepad[self.__height+2][self.__position] = "-"
		obj.Gamepad[self.__height+2][self.__position+1] = "-"
		obj.Gamepad[self.__height+2][self.__position+2] = "-"
		obj.Gamepad[self.__height+2][self.__position+3] = "-"
		obj.Gamepad[self.__height+1][self.__position-1] = "("
		obj.Gamepad[self.__height+1][self.__position+4] = ")"
		obj.Gamepad[self.__height][self.__position] = "-"
		obj.Gamepad[self.__height][self.__position+1] = "-"
		obj.Gamepad[self.__height][self.__position+2] = "-"
		obj.Gamepad[self.__height][self.__position+3] = "-"

class Overhead():
	def __init__(self,Position, length):
		self.__position = Position
		self.length=length
		self.__height = 13
	def getCol(self):
		return self.__position
	def Build(self,obj):
		temp1 = self.__position
		temp2 = self.length
		speciality=random.randint(0,self.length) 
		while temp2 > 0:
			if temp2 != speciality:
				for i in range(11,self.__height):
					obj.Gamepad[i][temp1] = "|"
					obj.Gamepad[i][temp1+1] = "|"
					obj.Gamepad[i][temp1+2] = "|"
			else:
				for i in range(11,self.__height):
					obj.Gamepad[i][temp1] = "!"
					obj.Gamepad[i][temp1+1] = "!"
					obj.Gamepad[i][temp1+2] = "!"
			temp2-=1
			temp1+=3
	def remove(self,obj,yindex):
		temp1 = self.__position
		temp2 = self.length
		var = math.floor((yindex-temp1)/3)
		special=2
		if obj.Gamepad[11][temp1+(var*3)] == " ":
			return 0
		if obj.Gamepad[11][temp1+(var*3)] != "!":
			special=0
		else:
			special=1
		for i in range(11,self.__height):
			obj.Gamepad[i][temp1+(var*3)] = " "
			obj.Gamepad[i][temp1+(var*3)+1] = " "
			obj.Gamepad[i][temp1+(var*3)+2] = " "
		if special==0:
			return 1
		else:
			return 2

class coin():
	def __init__(self,heady):
		self.heady = heady

	def Build(self,obj):
		for i in range(self.heady,self.heady+5):
			if obj.Gamepad[16][i] == " ":
				obj.Gamepad[16][i] = "O"
				self.heady = i
				break
	def reBuild(self,obj):
		obj.Gamepad[16][self.heady]="O"

class Gun():
	def __init__(self,heady):
		self.heady = heady

	def Build(self,obj):
		obj.Gamepad[16][self.heady] = chr(995)

class Castle():
	def __init__(self,heady):
		self.heady = heady
		self.Entrance = self.heady+3
	def Build(self,obj):
		obj.Gamepad[16][self.heady] = "("
		obj.Gamepad[15][self.heady] = "("
		obj.Gamepad[14][self.heady] = "("
		obj.Gamepad[13][self.heady] = "-"
		obj.Gamepad[13][self.heady+1] = "-"
		obj.Gamepad[13][self.heady+2] = "-"
		obj.Gamepad[13][self.heady+3] = "-"
		obj.Gamepad[13][self.heady+4] = "-"
		obj.Gamepad[13][self.heady+5] = "-"
		obj.Gamepad[13][self.heady+6] = "-"
		obj.Gamepad[14][self.heady+6] = ")"
		obj.Gamepad[15][self.heady+6] = ")"
		obj.Gamepad[16][self.heady+6] = ")"
		obj.Gamepad[16][self.heady+3] = chr(9601)
		obj.Gamepad[15][self.heady+3] = chr(9601)

class Bullet:
	def __init__(self,headx,heady):
		self.headx=headx
		self.heady=heady

	def move(self):
		self.heady+=2

	def remove(self,obj):
		if self.heady<=239:
			obj.Gamepad[self.headx][self.heady] = " "

	def build(self,obj):
		if self.heady<=239:
			obj.Gamepad[self.headx][self.heady] = "*"

class BossBullet(Bullet):
	def __init__(self,headx,heady):
		Bullet.__init__(self,headx+1,heady)

	def move(self):
		self.heady-=1

	def build(self,obj):
		if self.heady<=239:
			obj.Gamepad[self.headx][self.heady] = "="