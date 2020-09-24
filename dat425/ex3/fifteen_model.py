import random


class FifteenModel:
	def __init__(self):
		self.state = []
		numbers = list(range(1, 16))
		taken_numbers = []
		for row in range(4):
			self.state.append([])
			for col in range(4):
				if row == 3 and col == 3:
					self.state[-1].append(0)
					self.hole = row, col
					continue
				found = False
				i = None
				while not found:
					i = random.randint(0, len(numbers)-1)
					if i not in taken_numbers:
						found = True
				self.state[row].append(numbers[i])
				taken_numbers.append(i)

	def getValue(self, row, col):
		return self.state[row][col]

	def tryMove(self, row, col):
		abs_row = abs(row-self.hole[0])
		abs_col = abs(col-self.hole[1])
		if (abs_row == 1 and abs_col == 0) or (abs_row == 0 and abs_col == 1):
			val = self.state[row][col]
			self.state[row][col] = 0
			self.state[self.hole[0]][self.hole[1]] = val
			self.hole = row, col
			return True
		else:
			return False

	def shuffle(self):
		for _ in range(1000):
			rand_row = random.randint(0, 3)
			rand_col = random.randint(0, 3)
			self.tryMove(rand_row, rand_col)
