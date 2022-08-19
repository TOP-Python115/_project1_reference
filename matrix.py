from functools import lru_cache
from random import randrange as rr
from shutil import get_terminal_size as gts


class MatrixError(Exception):
    pass

class IteratorNotMatrixError(MatrixError):
    def __init__(self):
        super().__init__("the argument should contain iterators of the same length")

class DimensionError(MatrixError):
    def __init__(self, 
                 message: str = '', 
                 dim1: tuple[int, int] = None, 
                 dim2: tuple[int, int] = None,
                 *args):
        if dim1 and dim2:
            message = f"can't use this operation for matrices of {dim1} and {dim2} dimension"
            super().__init__(message, *args)
        else:
            super().__init__(message, *args)


# переменные для аннотации типов
TypeRow = tuple[str | int | float, ...] | list[str | int | float]
TypeMatrix = tuple[TypeRow, ...] | list[TypeRow]


class Matrix:
    def __init__(self, matrix: TypeMatrix):
        if self.__is_valid(matrix):
            self.n: int = len(matrix)
            self.m: int = len(matrix[0])
            self.origin: TypeMatrix = tuple(tuple(row) for row in matrix)
    
    @staticmethod
    def __is_valid(matrix: TypeMatrix) -> bool:
        """Проверяет, является ли объект корректной матрицей.

        Объект корректной матрицы содержит итераторы одинаковой длины"""
        q = set(len(row) for row in matrix)
        if len(q) == 1 and 0 not in q:
            return True
        else:
            raise IteratorNotMatrixError
    
    @property
    @lru_cache(maxsize=1)
    def transposed(self) -> TypeMatrix:
        """Возвращает транспонированную матрицу"""
        return tuple(tuple(self.origin[i][j] 
                           for i in range(self.n)) 
                     for j in range(self.m))
    
    @property
    @lru_cache(maxsize=1)
    def main_diag(self) -> TypeRow:
        """Возвращает главную диагональ матрицы."""
        return tuple(self.origin[i][i] 
                     for i in range(min(self.n, self.m)))
    
    @property
    @lru_cache(maxsize=1)
    def anti_diag(self) -> TypeRow:
        """Возвращает побочную диагональ матрицы."""
        return tuple(self.origin[i][self.m-i-1] 
                     for i in range(min(self.n, self.m)))
    
    @property
    @lru_cache(maxsize=1)
    def __flat(self) -> TypeRow:
        """Возвращает генератор из всех элементов матрицы."""
        return tuple(num for row in self.origin for num in row)
    
    def __repr__(self) -> str:
        return f"Matrix {self.n}x{self.m}: ({self.origin[0]}, ...)"
    
    def __str__(self) -> str:
        max_width = max(len(str(num)) for num in self.__flat) + 1
        return '\n'.join(''.join(f'{num:>{max_width}}' for num in row) 
                         for row in self.origin)

    def __add__(self, value):
        if not isinstance(value, Matrix):
            raise TypeError(f"can't add objects of types '{self.__class__.__name__}' and '{value.__class__.__name__}'")
        if not self.n == value.n or not self.m == value.m:
            # raise DimensionError("can't add matrices of different dimensions")
            raise DimensionError('',
                                 (self.n, self.m),
                                 (value.n, value.m),
                                 1, 2)
        return self.__elem_operations(value)
    
    def __sub__(self, value):
        if not isinstance(value, Matrix):
            raise TypeError(f"can't subtract '{self.__class__.__name__}' and '{value.__class__.__name__}'")
        if not self.n == value.n or not self.m == value.m:
            raise DimensionError("can't subtract matrices of different dimensions")
        return self.__elem_operations(value, '-')

    def __elem_operations(matr1, value, operation='+'):
        """Выполняет поэлементные операции над матрицами."""
        res = []
        for i in range(matr1.n):
            res += [[]]
            for j in range(matr1.m):
                if operation == '+':
                    res[i] += [matr1.origin[i][j] + value.origin[i][j]]
                elif operation == '-':
                    res[i] += [matr1.origin[i][j] - value.origin[i][j]]
                elif operation == '*':
                    res[i] += [matr1.origin[i][j] * value]
        return Matrix(res)

    def __mul__(self, value):
        if not isinstance(value, Matrix):
            if isinstance(value, (int, float)):
                return self.__elem_operations(value, '*')
            else:
                raise TypeError(f"can't multiply '{self.__class__.__name__}' and '{value.__class__.__name__}'")
        # TODO: умножение матриц
    
    def __radd__(self, value):
        if not isinstance(value, Matrix):
            raise TypeError(f"can't add objects of types '{self.__class__.__name__}' and '{value.__class__.__name__}'")

    def __rsub__(self, value):
        if not isinstance(value, Matrix):
            raise TypeError(f"can't subtract '{self.__class__.__name__}' and '{value.__class__.__name__}'")

    def __rmul__(self, value):
        if not isinstance(value, Matrix):
            if isinstance(value, (int, float)):
                return self.__elem_operations(value, '*')
            else:
                raise TypeError(f"can't multiply '{self.__class__.__name__}' and '{value.__class__.__name__}'")
        # TODO: умножение матриц

    def __contains__(self, value: str | int | float) -> bool:
        if isinstance(value, (str, int, float)):
            return value in self.__flat

    def __iter__(self):
        return iter(self.origin)

    def __getitem__(self, item):
        return self.origin[item]

    def index_of_max(self) -> tuple[int, int]:
        """Находит наибольший элемент в матрице и возвращает его индексы."""
        mx, res = 0, tuple()
        for i in range(self.n):
            for j in range(self.m):
                if mx < self.origin[i][j]:
                    mx, res = self.origin[i][j], (i, j)
        return res

    def is_square(self) -> bool:
        """Проверяет, является ли матрица квадратной."""
        return True if self.n == self.m else False


def draw_matrices(matrix: Matrix,
                  *matrices: Matrix,
                  left_margin: int = 1,
                  right: bool = False,
                  outer_borders: bool = False,
                  inner_borders: bool = True) -> str:
    """Возвращает в строковом виде одно или несколько игровых полей, расположенных на одном уровне, заполненных на основе переданных аргументами матриц."""
    matrices = (matrix,) + matrices
    num_of_matrices = len(matrices)
    if len(set(b.n for b in matrices)) != 1 or len(set(matr.m for matr in matrices)) != 1:
        raise DimensionError
    # для каждой матрицы вычисляет наибольшее количество символов в ячейке
    width_cells = tuple(max(max(len(str(cell)) for cell in row) for row in matrix) + 2
                        for matrix in matrices)
    # для каждой матрицы вычисляет количество символов, занимаемое всей матрицей в ширину
    width_boards = tuple(matrices[i].m * (width_cells[i] + inner_borders) - inner_borders
                         for i in range(num_of_matrices))
    pad = 5
    margin = (left_margin, gts()[0] - 1 - sum(width_boards) - pad * (num_of_matrices - 1))[right]
    # формирует строки со значениями и вертикальными разделителями
    value_lines = ()
    ob = ('', '|')[outer_borders]
    ib = ('', '|')[inner_borders]
    for i in range(matrices[0].n):
        # записывает в кортеж строки значений из каждой переданной матрицы
        values = (ob + ib.join(str(cell).center(width_cells[j]) for cell in matrices[j][i]) + ob
                  for j in range(num_of_matrices))
        # формирует полную строку с отступами слева и между строками значений
        value_lines += (' '*margin + (' '*pad).join(values), )
    # формирует строку с горизонтальными разделителями матриц и отступами слева и между ними
    ob = ('', '—')[outer_borders]
    horiz_line = ' '*margin + (' '*pad).join(ob + '—'*wd + ob for wd in width_boards)
    if outer_borders:
        return (f'{horiz_line}\n'
                + ('\n', f'\n{horiz_line}\n')[inner_borders].join(value_lines)
                + f'\n{horiz_line}')
    else:
        return ('\n', f'\n{horiz_line}\n')[inner_borders].join(value_lines)


# m1 = Matrix([[rr(0, 15) for _ in range(3)] for _ in range(5)])
# m2 = Matrix([[rr(0, 15) for _ in range(3)] for _ in range(5)])

# print(draw_matrices(m1, m2, outer_borders=True, right=True), end='\n\n')

# def other_default(func_object):
#     def _wrapper(*args, **kwargs):
#         if 'outer_borders' in kwargs:
#             return func_object(*args, **kwargs)
#         else:
#             return func_object(*args, outer_borders=False, **kwargs)
#     return _wrapper

# draw_matrices = other_default(draw_matrices)

# print(draw_matrices(m1, m2, ), end='\n\n')
# print(draw_matrices(m1, m2, outer_borders=True, inner_borders=False), end='\n\n')
# print(draw_matrices(m1, m2, outer_borders=True, inner_borders=True), end='\n\n')

# print(m1, m2, sep='\n\n', end='\n\n\n')

# m3 = m1 * 3
# m4 = 2 * m2
# print(m3, m4, sep='\n\n', end='\n\n')

# print(1 in m1)
