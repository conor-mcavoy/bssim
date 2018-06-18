import grid

class Player:
    def __init__(self):
        self.grid = grid.Grid()
        self.occupied = set()
        self.shots_taken = set()
        self.defeated = False

    def __str__(self):
        return str(self.grid)

    def add_ship(self, s):
        self.grid.add_ship(s)
        self.occupied.update(self.grid.occupied_squares())

    def query(self, square):
        self.ships_sunk()
        self.shots_taken.add(square)
        if self.occupied <= self.shots_taken:
            self.defeated = True
            print('Game over, you lose.')
            return
        return self.grid.query(square)

    def ships_sunk(self):
        sunk = {}
        for s in self.grid.ships:
            if s.squares <= self.shots_taken:
                sunk[s.size] = (s.square, s.direction)
        return sunk
    
    def show(self, game):
        font = game.font.SysFont(game.font.get_default_font(), 22)
        alphabet = 'ABCDEFGHIJ'
        black = (0, 0, 0)
        blue = (0, 0, 255)
        dark_blue = (0, 0, 128)
        gray = (128, 128, 128)
        red = (255, 0, 0)
        
        screen = game.display.get_surface()

        header = "Player's grid"
        width = font.size(header)[0]
        render = font.render(header, True, black)
        screen.blit(render, (220 - width // 2, 5))
        
        offset = 0

        for letter in alphabet:
            width = font.size(letter)[0]
            render = font.render(letter, True, black)
            screen.blit(render, (40 + offset - width // 2, 25))
            offset += 40

        offset = 0
        numbers = map(str, range(1, 11))
        for number in numbers:
            height = font.size(number)[1]
            render = font.render(number, True, black)
            screen.blit(render, (2, 60 + offset - height//2))
            offset += 40

        
        full_grid = [(col, row) for row in numbers for col in alphabet]
        for square in full_grid:
            col, row = square
            col_num = alphabet.index(col)
            left_side = 20 + 40 * col_num
            row_num = int(row)
            top_side = 40 * row_num

            rect = game.Rect(left_side, top_side, 40, 40)
            if square in self.occupied:
                if square in self.shots_taken:
                    color = red
                else:
                    color = gray
            else:
                if square in self.shots_taken:
                    color = dark_blue
                else:
                    color = blue
                
            game.draw.rect(screen, color, rect)
            game.draw.rect(screen, black, rect, 1)

        big_rect = game.Rect(20, 40, 400, 400)
        game.draw.rect(screen, black, big_rect, 2)
