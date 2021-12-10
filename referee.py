#!/bin/python3

import os,subprocess


class Board:
	def __init__(self):
		"""
		Initialize the board
		12 11 10 9 8 7 <- her
	13           		6
		0 1 2 3 4 5  <- my

		"""
		self.board = [
			4,4,4,4,4,4,0,
			4,4,4,4,4,4,0
		]
	
	def __str__(self):

		ret="          "
		for i in range(6,0,-1):
			ret+="%2d "% i
		ret+="\n"
		ret+="          "
		for i in range(12,6,-1):
			ret+="%2d "% self.board[i]
		ret+="\n"
		ret+="2nd->  "
		ret+="%2d "% self.board[13]
		ret+=" "*18
		ret+="%2d "% self.board[6]
		ret+="  <-1st\n"
		ret+="          "
		for i in range(0,6):
			ret+="%2d "% self.board[i]
		ret+="\n"
		ret+="          "
		for i in range(1,7):
			ret+="%2d "% i
		ret+="\n"
		return ret

	def mymove(self,move):
		"""
			1<=move<=6
			return true if free turn are allowed , false otherwise
		"""
		if move<1 or move>6:
			raise Exception("Invalid move")
		if self.board[move-1]==0:
			raise Exception("Invalid move! board contains no stone")
		x=self.board[move-1]
		self.board[move-1]=0
		# distribute x pathor to all box counter clockwise
		while x >=1 :
			if move==13:
				move=0
			self.board[move]+=1
			x-=1
			move+=1
		
		# check if last stone in my box
		move-=1
		if move == 6:
			return True
		# check if last stone in my side and empty box
		target=12-move
		if move <=5 and 0<= move and self.board[move]==1 and self.board[target]!=0:
			print("Capturing opponent's stone\a")
			self.board[6]+=self.board[move]
			self.board[6]+=self.board[target]
			self.board[move]=0
			self.board[target]=0
		return False

	def hermove(self,move):

		"""
			1<=move<=6
			return true if free turn are allowed , false otherwise
		"""
		if move<1 or move>6:
			raise Exception("Invalid move")
		move+=7
		if self.board[move-1]==0:
			raise Exception("Invalid move! board contains no stone")
		
		x=self.board[move-1]
		self.board[move-1]=0
		# distribute x pathor to all box counter clockwise
		while x >=1 :
			if move==14:
				move=0
			elif move==6:
				move=7
			self.board[move]+=1
			x-=1
			move+=1
		
		# check if last stone in her box
		move-=1
		if move == 13:
			return True
		# check if last stone in her side and empty box
		target=12-move
		if move <=12 and 7<= move and self.board[move]==1 and self.board[target]!=0:
			print("Capturing opponent's stone\a")
			self.board[13]+=self.board[move]
			self.board[13]+=self.board[target]
			self.board[move]=0
			self.board[target]=0
		return False

	def is_over(self):
		"""
			return true if game is over
		"""
		if all(self.board[i]==0 for i in range(6)):
			return True
		if all(self.board[i]==0 for i in range(7,13)):
			return True
		return False
	
	def my_score(self):
		""" return my score """
		sum=0
		for i in range(7):
			sum+=self.board[i]
		return sum
	def her_score(self):
		""" return her score """
		sum=0
		for i in range(7,14):
			sum+=self.board[i]
		return sum


def play_console():
	"""
		play game with console
	"""
	
	b=Board()
	print(b)
	myTurn=True

	while b.is_over() == False:
		if myTurn:
			move=int(input("Your move: "))
			try:
				myTurn=b.mymove(move)
			except Exception as e:
				print(e)
			print(b)
		else:
			move=int(input("Her move: "))
			try:
				myTurn= not b.hermove(move)
			except Exception as e:
				print(e)
			print(b)

	print ("My score: %d"%b.my_score())
	print ("Her score: %d"%b.her_score())
	if b.my_score()>b.her_score():
		print("You win!")
	elif b.my_score()<b.her_score():
		print("You lose!")
	else:
		print("Draw!")

def play_ai(my_ai_commands_list, her_ai_commands_list):
	"""
		play game with ai
		ai is name of target program
	"""
	my_ai_commands_list.append("1")
	her_ai_commands_list.append("2")
	my_agent=subprocess.Popen(
								my_ai_commands_list,
								stdin=subprocess.PIPE,
								stdout=subprocess.PIPE,
								universal_newlines=True, 
								bufsize=1
							)
	her_agent=subprocess.Popen(
								her_ai_commands_list,
								stdin=subprocess.PIPE,
								stdout=subprocess.PIPE,
								universal_newlines=True, 
								bufsize=1
							)

	
	b=Board()
	print(b)
	myTurn=True

	def get_board_out(board):
		ret=""
		for i in board:
			ret += str(i)+ " "
		return ret

	while b.is_over() == False:
		if myTurn:
			print(get_board_out(b.board) , file=my_agent.stdin, flush=True,end="\n")
			move=int(my_agent.stdout.readline())
			print("my turn:"+str(move))
			try:
				myTurn=b.mymove(move)
			except Exception as e:
				print(e)
			print(b)
		else:
			print(get_board_out(b.board) , file=her_agent.stdin, flush=True,end="\n")
			move=int(her_agent.stdout.readline())
			print("her turn:"+str(move))
			try:
				myTurn= not b.hermove(move)
			except Exception as e:
				print(e)
			print(b)

	my_agent.kill()
	her_agent.kill()

	print ("My score: %d"%b.my_score())
	print ("Her score: %d"%b.her_score())
	if b.my_score()>b.her_score():
		print("You win!")
	elif b.my_score()<b.her_score():
		print("You lose!")
	else:
		print("Draw!")

if __name__ == "__main__":
	# play_console()
	play_ai(["./1.out"],["./1.out"])