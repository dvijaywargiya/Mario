import random
import subprocess
Die='./smb_mariodie.wav'
class obstacles:
	def __init__(self,height, lower, upper):
		self.__col = random.randint(lower,upper)
		self.__height = height

	def Build(self,obj):
		for i in range(17-self.__height,17):
			obj.Gamepad[i][self.__col] = chr(9608)
			obj.Gamepad[i][self.__col+1] = chr(9608)
			obj.Gamepad[i][self.__col+2] = chr(9608)
		obj.Gamepad[17-self.__height][self.__col+1] = " "

	def getCol(self):
		return self.__col
	def getHeight(self):
		return self.__height

class Pit:
	def __init__(self,lower,upper):
		self.__col = random.randint(lower,upper)
		self.end = self.__col+3
		
	def getCol(self):
		return self.__col

	def Build(self,obj):
		for i in range(self.__col, self.__col+3):
			obj.Gamepad[16][i] = chr(9524)
		obj.Gamepad[16][self.__col-1]=chr(9608)
		obj.Gamepad[15][self.__col-1]=chr(9608)
		obj.Gamepad[14][self.__col-1]=chr(9608)
		obj.Gamepad[16][self.__col-2]=chr(9608)
		obj.Gamepad[15][self.__col-2]=chr(9608)

		obj.Gamepad[16][self.__col+3]=chr(9608)
		obj.Gamepad[15][self.__col+3]=chr(9608)
		obj.Gamepad[14][self.__col+3]=chr(9608)
		obj.Gamepad[16][self.__col+4]=chr(9608)
		obj.Gamepad[15][self.__col+4]=chr(9608)

	def Check(self,Mario,Lives,obj):
		if self.__col <= Mario.heady and self.end > Mario.heady and Mario.headx == 15:
			Lives[0]-=1
			obj.Gamepad[Mario.headx][Mario.heady]=" "
			subprocess.Popen(['aplay','-q',Die])
			for i in range(Mario.heady-10,Mario.heady):
				if obj.Gamepad[Mario.headx][i] == " " and obj.Gamepad[Mario.headx+1][i] == " ":
					Mario.heady=i
					Mario.index=i-5
					break
