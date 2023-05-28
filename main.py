# Importing packages
import random
import os

# Printing the Minesweeper Layout
def print_mines_layout():

	global mine_values
	global n

	print()
	print("\t\t\tСАПЕР!\n")

	st = "   "
	for i in range(n):
		st = st + "     " + str(i + 1)
	print(st)

	for r in range(n):
		st = "     "
		if r == 0:
			for c in range(n):
				st = st + "______"
			print(st)

		st = "     "
		for c in range(n):
			st = st + "|     "
		print(st + "|")

		st = "  " + str(r + 1) + "  "

		for c in range(n):
			st = st + "|  " + str(mine_values[r][c]) + "  "
		print(st + "|")

		st = "     "
		for c in range(n):
			st = st + "|_____"
		print(st + '|')

	print()

# Функция установки мин на поле
def set_mines():

	global numbers
	global mines_no
	global n

	# Счетчик поставленых мин
	count = 0
	while count < mines_no:

		# Рамдомное число для всех ячеек сетки
		val = random.randint(0, n*n-1)

		# Generating row and column from the number
		r = val // n
		c = val % n

		# Установка мины, при условии что ее там еще нет
		if numbers[r][c] != -1:
			count = count + 1
			numbers[r][c] = -1

# Функция установки значений ячеек для остальной сетки
def set_values():

	global numbers
	global n

	# Подсчет значений ячеек
	for r in range(n):
		for c in range(n):

			# Пропуск если это мина
			if numbers[r][c] == -1:
				continue

			# Верхняя
			if r > 0 and numbers[r-1][c] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Нижняя
			if r < n-1  and numbers[r+1][c] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Левая
			if c > 0 and numbers[r][c-1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Правая
			if c < n-1 and numbers[r][c+1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Верхняя левая
			if r > 0 and c > 0 and numbers[r-1][c-1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Верхняя правая
			if r > 0 and c < n-1 and numbers[r-1][c+1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Нижняя левая
			if r < n-1 and c > 0 and numbers[r+1][c-1] == -1:
				numbers[r][c] = numbers[r][c] + 1
			# Нижняя правая
			if r < n-1 and c < n-1 and numbers[r+1][c+1] == -1:
				numbers[r][c] = numbers[r][c] + 1

# Рекурсивная функция для отображения всех полей без мин рядом
def neighbours(r, c):

	global mine_values
	global numbers
	global vis

	# Проверка не была ли она уже открыта
	if [r,c] not in vis:

		# Помечаем открытой
		vis.append([r,c])

		# Если значение ячейки 0
		if numbers[r][c] == 0:

			# Показываем пользователю
			mine_values[r][c] = numbers[r][c]

			# Рекурсивные вызовы для соседних ячеек
			if r > 0:
				neighbours(r-1, c)
			if r < n-1:
				neighbours(r+1, c)
			if c > 0:
				neighbours(r, c-1)
			if c < n-1:
				neighbours(r, c+1)
			if r > 0 and c > 0:
				neighbours(r-1, c-1)
			if r > 0 and c < n-1:
				neighbours(r-1, c+1)
			if r < n-1 and c > 0:
				neighbours(r+1, c-1)
			if r < n-1 and c < n-1:
				neighbours(r+1, c+1)

		# If the cell is not zero-valued
		if numbers[r][c] != 0:
				mine_values[r][c] = numbers[r][c]

# Очистка терминала
def clear():
	os.system("clear")

# Отображение инструкции
def instructions():
	print("Инструкция:")
	print("1. Введите строку и столбец нужной ячейки, например: \"2 3\"")
	print("2. Для того что бы отметить флагом ячейку введите F после адреса ячейки, например: \"2 3 F\"")

# Проверка не закончена ли игра
def check_over():
	global mine_values
	global n
	global mines_no

	# Счетчик для ячеек которые участвуют в игре
	count = 0

	# Проверка каждой ячейки
	for r in range(n):
		for c in range(n):

			# Не пустая или флаг, значит участвует в игре
			if mine_values[r][c] != ' ' and mine_values[r][c] != 'F':
				count = count + 1

	# Проверка на окончание игры
	if count == n * n - mines_no:
		return True
	else:
		return False

def show_mines():
	global mine_values
	global numbers
	global n

	for r in range(n):
		for c in range(n):
			if numbers[r][c] == -1:
				mine_values[r][c] = 'M'


if __name__ == "__main__":
	# Размер поля
	n = 10
	# Количество мин
	mines_no = 10

	# The actual values of the grid
	numbers = [[0 for y in range(n)] for x in range(n)]
	# The apparent values of the grid
	mine_values = [[' ' for y in range(n)] for x in range(n)]
	# Отмеченые флагами позиции
	flags = []

	# Устанавливаем мины
	set_mines()

	# Устанавливаем значения ячеек
	set_values()

	# Отображаем инструкцию
	instructions()

	# Переменная окончания игры
	over = False

	# Основной цикл игры
	while not over:
		print_mines_layout()

		# Пользовательский ввод
		inp = input("Введи номер строки и столбца через пробел: ").split()

		# Проверка ввода на int
		if len(inp) == 2:
			try:
				val = list(map(int, inp))
			except ValueError:
				clear()
				print("Неправильный ввод!")
				instructions()
				continue

		# Проверка ввода на флаг (дальше все тоже к вводу с флагом)
		elif len(inp) == 3:
			if inp[2] != 'F' and inp[2] != 'f':
				clear()
				print("Неправильный ввод!")
				instructions()
				continue

			# Проверка что первые два символа int
			try:
				val = list(map(int, inp[:2]))
			except ValueError:
				clear()
				print("Неправильный ввод!")
				instructions()
				continue

			# Проверка не выходим ли за поле
			if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
				clear()
				print("Неправильный ввод!")
				instructions()
				continue

			# Получаем строку и колонку
			r = val[0]-1
			c = val[1]-1

			# Если ячейка уже была флагом
			if [r, c] in flags:
				clear()
				print("Флаг уже был установлен")
				continue

			# Если ячейка уде была отображена
			if mine_values[r][c] != ' ':
				clear()
				print("Ячейка уже открыта")
				continue

			# Проверка количества флагов
			if len(flags) < mines_no:
				clear()
				print("Флаг установлен")

				# Добавляем в список флагов
				flags.append([r, c])

				# Устанавливаем флаг для отображения на поле
				mine_values[r][c] = 'F'
				continue
			else:
				clear()
				print("Флаги кончились")
				continue

		else:
			clear()
			print("Неправильный ввод!")
			instructions()
			continue


		# Проверка не выходим ли за поле
		if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
			clear()
			print("Неправильный ввод!")
			instructions()
			continue

		# Получаем строку и столбец
		r = val[0]-1
		c = val[1]-1

		# Убираем флаг если он уже установлен
		if [r, c] in flags:
			flags.remove([r, c])

		# Попадание на мину
		if numbers[r][c] == -1:
			mine_values[r][c] = 'M'
			show_mines()
			print_mines_layout()
			print("ТЫ ПОДОРВАЛСЯ НА МИНЕ. ИГРА ОКОНЧЕНА!!!!!")
			over = True
			continue

		# Попадание в ячейку с нулевым значением
		elif numbers[r][c] == 0:
			vis = []
			mine_values[r][c] = '0'
			neighbours(r, c)

		# Если хотя бы одна мина есть рядом
		else:
			mine_values[r][c] = numbers[r][c]

		# Проверка на выигрыш
		if(check_over()):
			show_mines()
			print_mines_layout()
			print("Congratulations!!! YOU WIN")
			over = True
			continue
		clear()
