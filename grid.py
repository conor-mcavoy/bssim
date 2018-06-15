# this class is probably irrelevant and can be removed eventually
class Grid:
    def __init__(self):
        self.ships = set()

    def __str__(self):
        alphabet = 'ABCDEFGHIJ'
        numbers = map(str, range(1, 11)) # numbers 1-10
        full_grid = [(col, row) for row in numbers for col in alphabet]
        occupied = self.occupied_squares()
        output = '   ' + alphabet + '\n 1|'
        last_row = '1'
        row_count = 1
        for s in full_grid:
            if last_row != s[1]:
                output += '|{:2d}\n{:2d}|'.format(row_count, row_count+1)
                row_count += 1
                last_row = s[1]
            if s in occupied:
                output += 'X'
            else:
                output += ' '
        return output + '|10\n   ' + alphabet

    def add_ship(self, ship):
        occupied = self.occupied_squares()
        if occupied.intersection(ship.squares) == set():
            self.ships.add(ship)

    def occupied_squares(self):
        all_squares = set()
        for ship in self.ships:
            all_squares.update(ship.squares)
        return all_squares

    def query(self, square):
        return square in self.occupied_squares():
