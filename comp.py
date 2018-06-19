import copy

import grid
import random
import ship

class Computer:
    def __init__(self):
        self.grid = grid.Grid()
        self.generate_ships()
        self.occupied = self.grid.occupied_squares()
        self.shots_taken = set()
        
        self.shots_sent = set()
        self.shots_hit = set()
        self.shots_missed = set()
        
        self.defeated = False

    def generate_ships(self):
        """Initialize ship positions randomly."""
        
        alphabet = 'ABCDEFGHIJ'
        numbers = map(str, range(1, 11))
        full_grid = [(col, row) for row in numbers for col in alphabet]
        sizes = [5, 4, 3, 3, 2]
        for size in sizes:
            occupied = self.grid.occupied_squares()
            # this is inefficient but it's so fast it doesn't matter
            ship_size = str(size)
            while True:
                col, row = random.choice(full_grid)
                direction = random.choice(['right', 'down'])
                ship_str = ' '.join(ship_size, col, row, direction)
                try:
                    s = ship.Ship(ship_str)
                except IndexError:
                    continue
                if occupied.intersection(s.squares) == set():
                    self.add_ship(s)
                    break

    def add_ship(self, s):
        self.grid.add_ship(s)

    def query(self, square):
        """Respond to a shot from the player."""
        
        self.shots_taken.add(square)
        self.defeated = (self.occupied <= self.shots_taken)
        return self.grid.query(square)
    
    def prep_simulation(self):
        """Prepare to do simulations by generating a dictionary of possible locations for each ship size."""
        
        sizes = [5, 4, 3, 2]
        alphabet = 'ABCDEFGHIJ'
        numbers = map(str, range(1, 11))
        full_grid = [(col, row) for row in numbers for col in alphabet]
        possibilities = {5: [], 4: [], 3: [], 2: []}
        for size in sizes:
            for starting_square in full_grid:
                col_num = alphabet.index(starting_square[0])
                row_num = int(starting_square[1])
                if col_num + size <= 10:
                    for i in range(size):
                        current_square = (alphabet[col_num+i],
                                          starting_square[1])
                        if current_square in self.shots_missed:
                            # in the future, squares that cause a break
                            # can be cached for speed improvement
                            break
                    else:
                        possibilities[size].append((starting_square, 'right'))
                if row_num + size <= 11:
                    for i in range(size):
                        current_square = (starting_square[0],
                                          str(row_num+i))
                        if current_square in self.shots_missed:
                            break
                    else:
                        possibilities[size].append((starting_square, 'down'))
        return possibilities

    def simulate_player(self, possibilities, sunk_ships):
        sunk_ships_copy = copy.deepcopy(sunk_ships)
        ship_sizes = [5, 4, 3, 3, 2]
        random.shuffle(ship_sizes)
        temp_grid = grid.Grid()
        for size in ship_sizes:
            if size in sunk_ships_copy:
                possible_locations = [sunk_ships_copy[size]]
                sunk_ships_copy.pop(size)
            else:
                possible_locations = list(possibilities[size])
                random.shuffle(possible_locations)
            ship_added = False
            for location in possible_locations:
                square, direction = location
                col, row = square
                ship_str = ' '.join([str(size), col, row, direction])
                new_ship = ship.Ship(ship_str)
                    
                if temp_grid.add_ship(new_ship):
                    ship_added = True
                    break
            if not ship_added: # ran out of locations
                return []
        if self.shots_hit <= temp_grid.occupied_squares():
            return list(temp_grid.occupied_squares())
        return []

    def accumulate_simulations(self, sunk_ships):
        square_frequency = {}
        possibilities = self.prep_simulation()
        successful_sims = 0
        while successful_sims < 100:
            square_data = self.simulate_player(possibilities, sunk_ships)
            if not square_data:
                continue
            successful_sims += 1
            for square in square_data:
                if square in square_frequency:
                    square_frequency[square] += 1
                else:
                    square_frequency[square] = 1
        return square_frequency
                    
    
    def make_shot(self, sunk_ships):
        """Generate a shot to send to player."""
        
        square_tuples = sorted(self.accumulate_simulations(sunk_ships).items(),
                             key=lambda x: x[1], reverse=True)
        for square_tuple in square_tuples:
            square, freq = square_tuple
            if square not in self.shots_sent:
                self.shots_sent.add(square)
                return square

    def register_shot(self, shot, hit):
        """Register and record a hit or miss response from player."""
        
        if hit:
            self.shots_hit.add(shot)
        else:
            self.shots_missed.add(shot)

    def show(self, game):
        font = game.font.SysFont(game.font.get_default_font(), 22)
        alphabet = 'ABCDEFGHIJ'
        black = (0, 0, 0)
        blue = (0, 0, 255)
        red = (255, 0, 0)
        white = (255, 255, 255)
        screen = game.display.get_surface()

        header = "Computer's grid"
        width = font.size(header)[0]
        render = font.render(header, True, black)
        screen.blit(render, (660 - width // 2, 5))
        
        offset = 0

        for letter in alphabet:
            width = font.size(letter)[0]
            render = font.render(letter, True, black)
            screen.blit(render, (480 + offset - width // 2, 25))
            offset += 40

        offset = 0
        numbers = map(str, range(1, 11))
        for number in numbers:
            height = font.size(number)[1]
            render = font.render(number, True, black)
            screen.blit(render, (442, 60 + offset - height//2))
            offset += 40

        full_grid = [(col, row) for row in numbers for col in alphabet]
        for square in full_grid:
            col, row = square
            col_num = alphabet.index(col)
            left_side = 460 + 40 * col_num
            row_num = int(row)
            top_side = 40 * row_num

            rect = game.Rect(left_side, top_side, 40, 40)
            if square in self.shots_taken:
                if square in self.occupied:
                    color = red
                else:
                    color = blue
            else:
                color = white
                
            game.draw.rect(screen, color, rect)
            game.draw.rect(screen, black, rect, 1)

        game.draw.rect(screen, black, self.grid_rect(game), 2)

    def pos_to_square(self, pos):
        x, y = pos
        alphabet = 'ABCDEFGHIJ'
        col_num = (x - 460) // 40
        col = alphabet[col_num]
        row_num = y // 40
        return (col, str(row_num))

    def grid_rect(self, game):
        return game.Rect(460, 40, 400, 400)
