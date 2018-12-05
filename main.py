import numpy as np 
from boards import *
from characters import *
import sys,os
import inputchar
from Obstacles import *
import random,math
from Items import *
import subprocess
from colorama import init, Fore, Back, Style
init()
rows=20
cols=240
Mario = Player(15,8,0)
EnemyList=[]
PitList=[]
OverHeadList=[]
ObstacleList=[]
CoinList=[]
BonusCoinList=[]
CloudList=[]
Lives=[3,]
Gunn=[0]
Used=[0]
GameOver='./smb_gameover.wav'
Bonus='./smb_pipe.wav'
Up='./smb_powerup.wav'
class Playzone:
	def __init__(self):
		self.__Score=0

	def getScore(self):
		return self.__Score

	def setScore(self,num):
		self.__Score+=num
	def render(self,index,Gameboard):
		subprocess.call(["printf", "\033c"])
		print("\n")
		print("Score =",self.getScore())
		print("Lives = ",Lives[0])
		if Gunn[0] == 0:
			print("Gun = No")
		else:
			print("Gun = Yes")

		for row in range(rows):
			for col in range(index,index+60):
				if Gameboard.Gamepad[row][col] == "(" or Gameboard.Gamepad[row][col] == "-" or Gameboard.Gamepad[row][col] == ")":
					print(Fore.BLUE+Gameboard.Gamepad[row][col],end=" ")
				elif Gameboard.Gamepad[row][col] == chr(9608):
					print(Fore.MAGENTA+Gameboard.Gamepad[row][col],end=" ")
				elif Gameboard.Gamepad[row][col] == "O":
					print(Fore.CYAN+Gameboard.Gamepad[row][col],end=" ")
				elif Gameboard.Gamepad[row][col] == "#" or Gameboard.Gamepad[row][col] == "_":
					print(Fore.WHITE+Gameboard.Gamepad[row][col],end=" ")	
				elif Gameboard.Gamepad[row][col] == "|" or Gameboard.Gamepad[row][col] == "!":
					print(Fore.YELLOW+Gameboard.Gamepad[row][col],end=" ")
				else: 
					print(Fore.RED+Gameboard.Gamepad[row][col],end=" ")
			print("\n")
		print(Fore.GREEN+"READ ME")
		print("\n")
		print(chr(9608)+" -> These are solid blocks, you can climb over them but not go through them.")
		print("\n")
		print("|"+" -> These are overhead bricks without any bonus things, you can climb over them but not go through them.")
		print("\n")
		print("!" +" -> These are overhead bricks with bonus things, you can climb over them but not go through them.")
		print("\n")
		print(chr(9524) +" -> These are pits, you lose a life if you land up in one.")
		print("\n")
		print(chr(995) +" -> This is the GUN, you get it inside one of the pipes.")
		print("\n")

	def createObstacles(self):
		obstacle1 = obstacles(random.randint(2,3), 20, 30)
		obstacle2 = obstacles(random.randint(2,3), 40, 60)
		obstacle3 = obstacles(random.randint(2,3), 80, 90)
		obstacle4 = obstacles(random.randint(2,3), 100, 110)
		obstacle6 = obstacles(random.randint(2,3), 140, 160)
		obstacle7 = obstacles(random.randint(2,3), 180, 185)
		obstacle1.Build(Gameboard)
		obstacle2.Build(Gameboard)
		obstacle3.Build(Gameboard)
		obstacle4.Build(Gameboard)
		obstacle6.Build(Gameboard)
		obstacle7.Build(Gameboard)
		ObstacleList.append(obstacle1)
		ObstacleList.append(obstacle2)
		ObstacleList.append(obstacle3)
		ObstacleList.append(obstacle4)
		ObstacleList.append(obstacle6)
		ObstacleList.append(obstacle7)

	def createClouds(self,Gameboard):
		cloud1 = Cloud(random.randint(20, 27))
		cloud2 = Cloud(random.randint(35, 54))
		cloud3 = Cloud(random.randint(65, 105))
		cloud4 = Cloud(random.randint(110, 125))
		cloud5 = Cloud(random.randint(130, 150))
		cloud6 = Cloud(random.randint(160, 195))
		CloudList.append(cloud1)
		CloudList.append(cloud2)
		CloudList.append(cloud3)
		CloudList.append(cloud4)
		CloudList.append(cloud5)
		CloudList.append(cloud6)
		self.buildClouds(CloudList)

	def buildClouds(self,list):
		for cloud in list:
			cloud.Build(Gameboard)
	def createOverheads(self):
		overhead1 = Overhead(random.randint(32,39),random.randint(1,3))
		overhead1.Build(Gameboard)
		OverHeadList.append(overhead1)
		overhead2 = Overhead(random.randint(120,150),random.randint(1,3))
		overhead2.Build(Gameboard)
		OverHeadList.append(overhead2)

	def moveEnemy(self,Gameboard,Lives):
		Var=0
		Temp=self.getScore()
		enemy1.remove(Gameboard)
		Var+=enemy1.movement(Gameboard,Mario,EnemyList,PitList,Temp,Lives)
		enemy1.Build(Gameboard,EnemyList)
		enemy2.remove(Gameboard)
		Var+=enemy2.movement(Gameboard,Mario,EnemyList,PitList,Temp,Lives)
		enemy2.Build(Gameboard,EnemyList)
		enemy3.remove(Gameboard)
		Var+=enemy3.movement(Gameboard,Mario,EnemyList,PitList,Temp,Lives)
		enemy3.Build(Gameboard,EnemyList)
		self.setScore(Var)
		
	def reCreatePits(self,Gameboard):
		pit1.Build(Gameboard)
		pit2.Build(Gameboard)
		pit3.Build(Gameboard)

	def checkForPits(self,Lives):
		pit1.Check(Mario,Lives,Gameboard)
		pit2.Check(Mario,Lives,Gameboard)
		pit3.Check(Mario,Lives,Gameboard)
		pit1.Build(Gameboard)
		pit2.Build(Gameboard)
		pit3.Build(Gameboard)

	def createCoins(self):
		coin1 = coin(random.randint(20,30))
		coin1.Build(Gameboard)
		CoinList.append(coin1)
		coin2 = coin(random.randint(40,60))
		coin2.Build(Gameboard)
		CoinList.append(coin2)
		coin3 = coin(random.randint(80,90))
		coin3.Build(Gameboard)
		CoinList.append(coin3)
		coin4 = coin(random.randint(100,110))
		coin4.Build(Gameboard)
		CoinList.append(coin4)
		coin5 = coin(random.randint(120,130))
		coin5.Build(Gameboard)
		CoinList.append(coin5)
		coin6 = coin(random.randint(140,160))
		coin6.Build(Gameboard)
		CoinList.append(coin6)
	def createBonusCoins(self,Gameboard):
		var=0
		for i in range(20,40):
			coin1 = coin(i+var)
			var+=2
			coin1.Build(Gameboard)
			BonusCoinList.append(coin1)

	def reCreateCoins(self):
		for coin in CoinList:
			coin.reBuild(Gameboard)

	def checkBonusPosition(self,Mario,ObstacleList,BonusGameboard,Gunn,Used):
		temp = ObstacleList[5]
		if Mario.heady == temp.getCol()+1 and Mario.headx == 16-temp.getHeight() and Used[0]==0:
			self.createBonusLevel(BonusGameboard,Gunn)
			Used[0]=1
	def createBonusClouds(self,Gameboard):
		cloud1 = Cloud(random.randint(10, 20))
		cloud2 = Cloud(random.randint(25, 35))
		cloud3 = Cloud(random.randint(40, 45))
		cloud4 = Cloud(random.randint(55, 70))
		cloud5 = Cloud(random.randint(80, 100))
		cloud1.Build(Gameboard)
		cloud2.Build(Gameboard)
		cloud3.Build(Gameboard)
		cloud4.Build(Gameboard)
		cloud5.Build(Gameboard)

	def createGun(self,Gameboard,gun):		
		gun.Build(Gameboard)

	def createBonusLevel(self,BonusGameboard,Gunn):
		Key = getch()
		if Key != None:
			Key_pressed = ord(Key)
			if Key_pressed == ord('s'):

				Begin.createBonusClouds(BonusGameboard)
				Begin.createBonusCoins(BonusGameboard)
				gun = Gun(100)
				Begin.createGun(BonusGameboard,gun)
				Marioo=Player(15,5,0)
				subprocess.Popen(['aplay','-q',Bonus])
				while True:
					var=0
					var+=BonusGameboard.CheckAir(Marioo,BonusCoinList)
					var+=BonusGameboard.UpdatePosition(Marioo,PitList,OverHeadList,ObstacleList,BonusCoinList,Castle1,120)
					BonusGameboard.PlayerPosition(Marioo)
					Begin.setScore(var)
					#Begin.Score+=var
					Begin.render(Marioo.index,BonusGameboard)
					if gun.heady == Marioo.heady:
						Gunn[0]=1
						subprocess.Popen(['aplay','-q',Up])
					if Marioo.heady == 100:
						break
	def createCastle(self):
		Castle1.Build(Gameboard)

	def createBossEnemy(self):
		BossEnemy1.Build(Gameboard)


Gameboard = Game_Board(rows,cols)
BonusGameboard = Game_Board(rows,120)
BonusGameboard.Windows()
Begin = Playzone()
Gameboard.Windows()
Begin.createObstacles()
Begin.createClouds(Gameboard)
Begin.createOverheads()
Begin.createCoins()
BossEnemy1 = BossEnemy()
Begin.createBossEnemy()
Castle1 = Castle(223)
enemy1 = Enemy(random.randint(32, 39),random.randint(0,1))
enemy1.Build(Gameboard,EnemyList)
EnemyList.append(enemy1)
enemy2 = Enemy(random.randint(92, 98),random.randint(0,1))
EnemyList.append(enemy2)
enemy2.Build(Gameboard,EnemyList)
enemy3 = Enemy(random.randint(132, 139),random.randint(0,1))
EnemyList.append(enemy3)
enemy3.Build(Gameboard,EnemyList)

pit1=Pit(65, 75)
pit1.Build(Gameboard)
pit2=Pit(112, 119)
pit2.Build(Gameboard)
pit3=Pit(165, 175)
pit3.Build(Gameboard)
PitList.append(pit1)
PitList.append(pit2)
PitList.append(pit3)

while Lives[0]>0:
	if Gunn[0]==1:
		Mario.changeGunStatus()
	var=0
	for bullet in BulletList:
		bullet.remove(Gameboard)
		bullet.move()
		bullet.build(Gameboard)
	for bullet in BossEnemy1.bullet_list:
		bullet.remove(Gameboard)
		bullet.move()
		bullet.build(Gameboard)

	for bullet in BossEnemy1.bullet_list:
		if bullet.heady == Mario.heady and (bullet.headx == Mario.headx or bullet.headx == Mario.headx+1):
			Lives[0]-=1
		for b in BulletList:
			if bullet.heady == b.heady and bullet.headx == b.headx:
				BulletList.pop(BulletList.index(b))
				BossEnemy1.bullet_list.pop(BossEnemy1.bullet_list.index(bullet))
	if BossEnemy1.alive == 1:
		BossEnemy1.movement(Gameboard,Mario,Lives)
		BossEnemy1.hitCheck(BulletList,Gameboard,Begin)
	Begin.checkBonusPosition(Mario,ObstacleList,BonusGameboard,Gunn,Used)
	Begin.checkForPits(Lives)
	Begin.moveEnemy(Gameboard,Lives)
	var+=Gameboard.CheckAir(Mario,CoinList)
	var+=Gameboard.UpdatePosition(Mario,PitList,OverHeadList,ObstacleList,CoinList,Castle1,cols)
	Gameboard.PlayerPosition(Mario)
	Begin.setScore(var)
	Begin.createCastle()
	Begin.buildClouds(CloudList)
	Begin.render(Mario.index,Gameboard)
	Begin.reCreatePits(Gameboard)
	Begin.reCreateCoins()

if Lives[0] == 0:
	subprocess.Popen(['aplay','-q',GameOver])
	exit()
