class Ship:
    def __init__(self, ship_str):
        size, column, row, direction = ship_str.split()
        self.size = int(size)
        alphabet = 'ABCDEFGHIJ'
        column_num = alphabet.index(column)
        row_num = int(row)
        if column_num + self.size > 10 or row_num + self.size > 11:
            raise IndexError
        
        self.squares = set()
        for i in range(self.size):
            if direction == 'down':
                self.squares.add((column, str(row_num+i)))
            elif direction == 'right':
                self.squares.add((alphabet[column_num+i], row))