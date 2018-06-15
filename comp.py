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

    def __str__(self):
        return str(self.grid)

    def generate_ships(self):
        alphabet = 'ABCDEFGHIJ'
        numbers = map(str, range(1, 11))
        full_grid = [(col, row) for row in numbers for col in alphabet]
        sizes = [5, 4, 3, 3, 2]
        for size in sizes:
            occupied = self.grid.occupied_squares()
            while True:
                ship_list = [str(size)]
                location = random.choice(full_grid)
                ship_list.extend(location)
                ship_list.append(random.choice(('right', 'down')))
                ship_str = ' '.join(ship_list)
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
        self.defeated = self.occupied <= self.shots_taken:
        return self.grid.query(square)

    def prep_simulation(self):
        sizes = [5, 4, 3, 3, 2]
        alphabet = 'ABCDEFGHIJ'
        numbers = map(str, range(1, 11))
        full_grid = [(col, row) for row in numbers for col in alphabet]
        for size in sizes:
            for starting_square in full_grid:
                # right
                for i in range(size):
                    pass
                # down
            break
        
    
    def make_shot(self):
        """Generate a shot to send to player."""
        
        alphabet = 'ABCDEFGHIJ'
        numbers = map(str, range(1, 11))
        full_grid = set((col, row) for row in numbers for col in alphabet)
        possibilities = list(full_grid - self.shots_sent)
        shot = random.choice(possibilities)
        self.shots_sent.add(shot)
        return shot

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
