from pysat.solvers import Solver

# Определение функции для генерации уникальных целочисленных идентификаторов переменных
def var_name(i, j, c, n, k):
    assert 1 <= i <= n
    assert 1 <= j <= n
    assert 1 <= c <= k
    return (i - 1) * n * k + (j - 1) * k + c

# Функция для создания формулы и решения её с помощью SAT-солвера
def create_formula_and_solve(n, k):
    # Создание нового экземпляра SAT-солвера
    solver = Solver()

    # Добавление условий, что каждая пара (i, j) должна быть окрашена хотя бы в один цвет
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):  # Рассмотрим только уникальные пары i < j, чтобы избежать дублирования
            solver.add_clause([var_name(i, j, c, n, k) for c in range(1, k + 1)])

    # Добавление условий, что ни один треугольник из рёбер клики не раскрашен в один цвет
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            for l in range(j + 1, n + 1):  # Опять же рассматриваем только уникальные тройки i < j < l
                for c in range(1, k + 1):
                    # Для каждого цвета c добавляем клаузу, что хотя бы одно из рёбер i-j, j-l или i-l не окрашено в цвет c
                    solver.add_clause([-var_name(i, j, c, n, k), -var_name(j, l, c, n, k), -var_name(i, l, c, n, k)])

    # Попытка найти решение
    solved = solver.solve()

    # Вывод результата
    if solved:
        print("Решение найдено:")
        model = solver.get_model()
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                for c in range(1, k + 1):
                    if var_name(i, j, c, n, k) in model:
                        print(f"Пара ({i}, {j}) окрашена в цвет {c}")
    else:
        print("Решение не найдено.")

# Запуск функции с n = 3 и k = 3
create_formula_and_solve(5, 2)