import argparse
import random
import sys
import time

import pygame

import comp
import grid
import player
import ship


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help='path to file with ship locations')
    args = parser.parse_args()

    p = player.Player()
    computer = comp.Computer()
    with open(args.filename, 'r') as f:
        for line in f:
            p.add_ship(ship.Ship(line))

    black = (0, 0, 0)
    white = (255, 255, 255)
            
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Battleship')
    icon = pygame.image.load('images/icon.bmp')
    pygame.display.set_icon(icon)
    
    screen = pygame.display.set_mode((880, 480))
    screen.fill(white)
    pygame.display.update()

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 22)
    message = font.render('Your turn.', True, black)
    
    players_turn = True
    need_to_wait = False

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif players_turn and event.type == pygame.MOUSEBUTTONDOWN\
                 and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                computer_grid = computer.grid_rect(pygame)
                if computer_grid.collidepoint(mouse_pos):
                    players_turn = False
                    square = computer.pos_to_square(mouse_pos)
                    response = computer.query(square)
                    if response:
                        message_text = "Hit! Computer's turn."
                    else:
                        message_text = "Miss! Computer's turn."
                    message = font.render(message_text, True, black)        

        screen.fill((255, 255, 255))

        screen.blit(message, (20, 455))
        p.show(pygame)
        computer.show(pygame)
        
        pygame.display.flip()

        if need_to_wait:
            time.sleep(0.8)
            need_to_wait = False

        if players_turn:
            message = font.render('Your turn.', True, black)
            mouse_pos = pygame.mouse.get_pos()
            computer_grid = pygame.Rect(460, 40, 400, 400)
            if computer_grid.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(*pygame.cursors.diamond)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            computer_shot = computer.make_shot(p.ships_sunk())
            player_response = p.query(computer_shot)
            computer.register_shot(computer_shot, player_response)
            players_turn = True
            need_to_wait = True
            
        while computer.defeated or p.defeated:
            clock.tick(60)
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            if computer.defeated:
                message_text = 'Game over, you win!'
            elif p.defeated:
                message_text = 'Game over, you lose!'
            message = font.render(message_text, True, black)
            
            screen.fill((255, 255, 255))
            screen.blit(message, (20, 455))
            p.show(pygame)
            computer.show(pygame)
            pygame.display.flip()
            
                

if __name__ == '__main__':
    main()
