import os

BLANK = "_"

class Game:

	def __init__(self, players, board_size, simulating = None):
		self.rows = board_size[0]
		self.columns = board_size[1]

		# This will be the real board the only gets changed when a player
		# decides to make a move
		self.board = self.make_board()

		# When players are considering how a certain move might play out,
		# they will be using this imaginary board, so as not to effect our real board
		self.imaginary_board = None
		self.player1 = players[0]
		self.player2 = players[1]
		self.player1.assignToken("X")
		self.player2.assignToken("O")
		self.player_to_move = self.player1
		self.imaginary_player_to_move = None
		self.playing = True

		# Work-around to fix default argument in python (need to fix)
		self.simulating = simulating if simulating is not None else simulating

	def make_board(self):
		board = [[BLANK for j in range(self.columns)] for i in range(self.rows)]
		return board

	def print_board(self, board = None):

		# Work-around to fix default argument in python (need to fix)
		board = board if board is not None else self.board

		for row in range(len(board)):
			for col in range(len(board[0])):
				print(board[row][col], end=' ')
			print()

		for col in range(self.columns):
			print(col + 1, end=' ')
		print()
		print()

	def move(self, slot, board, player_to_move = None):

		# Work-around to fix default argument in python (need to fix)
		player_to_move = player_to_move if player_to_move is not None else self.player_to_move

		if slot < self.columns and slot >= 0:
			if board[0][slot] != BLANK:
				# print("slot is full u fuck, try again")
				return False
			else:
				height = self.rows - 1
				while board[height][slot] != BLANK and height > 0:
					height -= 1;
				board[height][slot] = player_to_move.token
				return True
		elif slot == "q" or slot == "Q" or slot == "quit":
			self.playing = False
			return True
		else:
			# print("U fucked up. not a slot")
			return False

	# Check for victory (i.e. 4-in-a-row)
	def check_board(self, board = None, imaginary = False):

		# Work-around to fix default argument in python (need to fix)
		board = board if board is not None else self.board

		# Check horizontal
		for row in range(self.rows):
			count = 1
			curr_val = board[row][0]
			for column in range(1, len(board[row])):
				if curr_val == board[row][column] and curr_val != BLANK:
					count += 1
					if count == 4:
						if not imaginary:
							self.winner_name = self.player_to_move.name
							self.playing = False
						if self.player_to_move == self.player1:
							return 1
						else:
							return -1
				else:
					count = 1
				curr_val = board[row][column]

		# Check vertical connect 4
		# Iterate through each of the columns
		for column in range(self.columns):
			# Initialize count to 1 and set the current value to the top cell in each column
			count = 1
			curr_val = board[0][column]
			# Go down the rows and check if there are 4 tiles of the same color in a row
			for row in range(1, len(board)):
				# If next value in column is the same as the previous value
				if curr_val == board[row][column] and curr_val != BLANK:
					# Increment count
					count += 1
					# If this is the fourth of the same tile in a row,
					# Then that player has won
					if count == 4:
						if not imaginary:
							# Print the winner
							self.winner_name = self.player_to_move.name
							# Set playing to false so the game knows not to play anymore
							self.playing = False
						# Exit the function
						if self.player_to_move == self.player1:
							return 1
						else:
							return -1
				# If the next value in the column is different from the previous value
				else:
					# Reset count to 1
					count = 1
				# Set the new current value to value of the tile we just checked
				curr_val = board[row][column]

		# Check diagonal
		for row in range(self.rows - 3):
			for column in range(self.columns - 3):
				if board[row][column] == board[row+1][column+1] == \
				   board[row+2][column+2] == board[row+3][column+3] != BLANK:
					if not imaginary:
						self.winner_name = self.player_to_move.name
						self.playing = False
					if self.player_to_move == self.player1:
						return 1
					else:
						return -1

		for row in range(4, self.rows):
			for column in range(self.columns - 3):
				if board[row][column] == board[row-1][column+1] == \
				   board[row-2][column+2] == board[row-3][column+3] != BLANK:
					if not imaginary:
						self.winner_name = self.player_to_move.name
						self.playing = False
					if self.player_to_move == self.player1:
						return 1
					else:
						return -1

		# Check if board is full
		full = True
		for column in range(self.columns):
			if board[0][column] == BLANK:
				full = False
		if full == True:
			if not imaginary:
				self.playing = False
				self.winner_name = "Tie"
			return 0

		# If no one has won, return None
		return None

	def is_playing(self):
		return self.playing

	def get_board(self):
		return self.board

	def get_player_to_move(self):
		return self.player_to_move

	def play(self):
		""" Runs gameplay until the game is over, then scores bonus Blocks.
		"""

		# Runs game until a player has won
		while self.is_playing():

			# Display board
			if not self.simulating:
				# os.system('clear')
				self.print_board()

			# Let the player choose their move
			chosen_move = self.player_to_move.chooseMove(self)

			# Execute move
			self.move(int(chosen_move) - 1, self.get_board())

			# Check board
			self.check_board()

			# Switch whose turn it is
			if self.player_to_move == self.player1:
				self.player_to_move = self.player2
			else:
				self.player_to_move = self.player1

		# Print final board configuration
		if not self.simulating:
			# os.system('clear')
			print(self.winner_name, "wins!")
			self.print_board()
