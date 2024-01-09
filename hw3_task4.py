from z3 import *

def is_safe_minefield(minefield, row, col):
    # Проверка валидности координат
    if row < 0 or row >= len(minefield) or col < 0 or col >= len(minefield[0]):
        return False

    # Создаем SAT решатель
    solver = Solver()

    # Переменные для каждой ячейки
    cells = [[Bool(f'cell_{r}_{c}') for c in range(len(minefield[0]))] for r in range(len(minefield))]

    # Добавляем условия для всех чисел в поле
    for r in range(len(minefield)):
        for c in range(len(minefield[0])):
            if isinstance(minefield[r][c], int):
                # Получаем соседние ячейки
                neighbors = [(r + dr, c + dc) for dr in (-1, 0, 1) for dc in (-1, 0, 1) if (dr, dc) != (0, 0)]
                neighbors = [(nr, nc) for nr, nc in neighbors if 0 <= nr < len(minefield) and 0 <= nc < len(minefield[0])]
                # Создаем ограничение на количество мин вокруг числа
                solver.add(Sum([If(cells[nr][nc], 1, 0) for nr, nc in neighbors]) == minefield[r][c])

    # Добавляем условия для мин
    for r in range(len(minefield)):
        for c in range(len(minefield[0])):
            if minefield[r][c] == '*':
                solver.add(cells[r][c])

    # Проверяем, что выбранная ячейка пуста
    assert minefield[row][col] == ' ', "Selected cell is not empty!"

    # Проверяем, что пустая ячейка не содержит мины
    solver.add(cells[row][col])

    # Проверяем, существует ли решение
    return solver.check() == sat

# Пример поля игры (0 - без мин вокруг, * - мина)
# minefield = [
#     [1, '*', 0],
#     [2, 2, 1],
#     [' ', 1, '*']
# ]

minefield = [
    [' ', ' ', ' ', 1],
    [' ', ' ', ' ', 1],
    [' ', ' ', '2', 1],
    [1, 1, 1, ' ']
]

# Координаты пустой ячейки
row, col = 2, 1

# Проверяем, безопасна ли пустая ячейка
print("Cell is safe!" if is_safe_minefield(minefield, row, col) else "Cell is not safe!")