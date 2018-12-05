import numpy as np
from characters import *
from inputchar import getch
import sys
import subprocess

LevelEnd='./smb_world_clear.wav'
BreakBlock='./smb_breakblock.wav'
Coin='./smb_coin.wav'
Jump='./smb_jump-super.wav'
#Number of rows and columns
rows=20
cols=240
#Mario = Player(15,4)
class Game_Board:
	def __init__(self,rows,cols):
		self.Nrows = rows
		self.Ncols = cols
		self.Gamepad = np.full((rows,cols),"#")
		self.Gamepad[17][:] = "_"

	def Windows(self):
		for row in range(2,rows-3):
			for col in range(0,self.Ncols):
				self.Gamepad[row][col]=" "

	def PlayerPosition(self,Mario):
		self.Gamepad[Mario.headx][Mario.heady] = "^"
		self.Gamepad[Mario.headx+1][Mario.heady] = "M"
		
	def CheckAir(self,Mario,CoinList):
		if Mario.headx < 15 and self.Gamepad[Mario.headx+2][Mario.heady] != chr(9608) and self.Gamepad[Mario.headx+2][Mario.heady] != "|" and self.Gamepad[Mario.headx+2][Mario.heady] != "!" :
			flag=0
			self.Gamepad[Mario.headx][Mario.heady] = " "
			if self.Gamepad[Mario.headx+2][Mario.heady]=="O":
				for coin in CoinList:
					if coin.heady == Mario.heady:
						flag=1
						subprocess.Popen(['aplay','-q',Coin])
						CoinList.pop(CoinList.index(coin))
						break
			Mario.headx+=1
			if flag==1:
				return 2
			else: 
				return 0
		return 0

	def UpdatePosition(self,Mario,PitList,OverHeadList,ObstacleList,CoinList,Castle,cols):
		Key = getch()
		if Key != None:
			Key_pressed = ord(Key)
			if (Key_pressed == ord('d') or Key_pressed == ord('D')) and self.Gamepad[Mario.headx][Mario.heady+1] != chr(9608) and self.Gamepad[Mario.headx+1][Mario.heady+1] != chr(9608) and self.Gamepad[Mario.headx+1][Mario.heady+1] != "|" and self.Gamepad[Mario.headx+1][Mario.heady+1] != "!" and self.Gamepad[Mario.headx][Mario.heady+1] != "|" and self.Gamepad[Mario.headx][Mario.heady+1] != "!":
				flag=0
				if self.Gamepad[Mario.headx+1][Mario.heady+1]=="O":
					flag=1
					for coin in CoinList:
						if coin.heady == Mario.heady+1:
							subprocess.Popen(['aplay','-q',Coin])
							CoinList.pop(CoinList.index(coin))
				self.Gamepad[Mario.headx][Mario.heady] = " "
				self.Gamepad[Mario.headx+1][Mario.heady] = " "						
				Mario.heady+=1
				if Mario.heady<=cols-60-1:
					Mario.index+=1
				if Mario.heady == Castle.Entrance:
					subprocess.Popen(['aplay','-q',LevelEnd])
					exit()
				if flag==1:
					return 2
			elif Key_pressed == ord('a') or Key_pressed == ord('A'):
				flag=0
				if Mario.heady >= 0 and self.Gamepad[Mario.headx][Mario.heady-1] != chr(9608) and self.Gamepad[Mario.headx+1][Mario.heady-1] != chr(9608) and self.Gamepad[Mario.headx+1][Mario.heady-1] != "!" and self.Gamepad[Mario.headx+1][Mario.heady-1] != "|" and self.Gamepad[Mario.headx][Mario.heady-1] != "!" and self.Gamepad[Mario.headx][Mario.heady-1] != "|": 
					if self.Gamepad[Mario.headx+1][Mario.heady-1]=="O":
						flag=1
						for coin in CoinList:
							if coin.heady == Mario.heady-1:
								subprocess.Popen(['aplay','-q',Coin])
								CoinList.pop(CoinList.index(coin))
					self.Gamepad[Mario.headx][Mario.heady] = " "
					self.Gamepad[Mario.headx+1][Mario.heady] = " "
					Mario.heady-=1
					Mario.index-=1
					if flag==1:
						return 2
			elif Key_pressed == ord('w') or Key_pressed == ord('W'):
				if self.Gamepad[Mario.headx][Mario.heady] == "^":
					self.Gamepad[Mario.headx+1][Mario.heady] = " "
					self.Gamepad[Mario.headx][Mario.heady] = " "
					if Mario.headx != 15:
						subprocess.Popen(['aplay','-q',Jump])
						flag=2
						for obs in ObstacleList:
							for oh in OverHeadList:
								if Mario.heady>= oh.getCol() and Mario.heady<=(oh.getCol()+(oh.length*3))-1:
									#Mario.headx-=2
									var=oh.remove(self,Mario.heady)
									if var != 0:
										subprocess.Popen(['aplay','-q',BreakBlock])
									if var==0:
										Mario.headx-=4
									else:
										Mario.headx-=2
									flag=1
									break
							if flag==1:
								break		
							if (Mario.heady == obs.getCol() or Mario.heady == obs.getCol()+1 or Mario.heady == obs.getCol()+2) and flag==2:
								Mario.headx-=6;
								flag=3
								break
						if flag==2:
							Mario.headx-=6
					else:
						subprocess.Popen(['aplay','-q',Jump])
						flag=0
						var=3
						for oh in OverHeadList:
							if Mario.heady>= oh.getCol() and Mario.heady<=(oh.getCol()+(oh.length*3))-1:
								var=oh.remove(self,Mario.heady)
								if var!=0:
									subprocess.Popen(['aplay','-q',BreakBlock])
								if var==0:
									Mario.headx-=6
								else:
									Mario.headx-=2
								flag=1
								break
						if flag==0:
							Mario.headx-=6
						if flag==1 and var==1:
							return 1
						elif flag==1 and var==2:
							return 4
						else:
							return 0
			elif (Key_pressed == ord('g') or Key_pressed == ord('G')) and Mario.useGunVar()==1:
				Mario.shoot()

			elif Key_pressed == ord('q') or Key_pressed == ord('Q'):
				exit()
		return 0
