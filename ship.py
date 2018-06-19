class Ship:
    def __init__(self, ship_str):
        self.sunk = False
        size, column, row, direction = ship_str.split()
        self.size = int(size)
        self.square = (column, row)
        self.direction = direction
        alphabet = 'ABCDEFGHIJ'
        column_num = alphabet.index(column)
        row_num = int(row)
        if column_num + self.size > 10 and direction == 'right'\
           or row_num + self.size > 11 and direction == 'down':
            raise IndexError
        
        self.squares = set()
        for i in range(self.size):
            if direction == 'down':
                self.squares.add((column, str(row_num+i)))
            elif direction == 'right':
                self.squares.add((alphabet[column_num+i], row))
