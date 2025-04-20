import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60

white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []

black_queen = pygame.image.load('images/black_queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('images/black_king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('images/black_rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('images/black_bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('images/black_knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('images/black_pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('images/white_queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('images/white_king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('images/white_rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('images/white_bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('images/white_knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('images/white_pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']

counter = 0
winner = ''
game_over = False

def check_options():
    pass

def draw_board():
    for i in range(32): 
    # Vi tegner kun de mørke firkanter på et 8x8 skakbræt. 

        column = i % 4 
        # Hver række har kun 4 mørke firkanter
        row = i // 4
        # Hver 4 mørke firkant udgør én række

        if row % 2 == 0:
            pygame.draw.rect(screen, 'dark gray', [600 - (column * 200), row * 100, 100, 100])
            # Hvis rækken er lige (0, 2, 4...), starter de mørke firkanter i kolonne 0
        else:
            pygame.draw.rect(screen, 'dark gray', [700 - (column * 200), row * 100, 100, 100])
            # Hvis rækken er ulige (1, 3, 5...), starter de mørke firkanter i kolonne 1
        for i in range(9):
             # Vi tegner 9 linjer for at få et 8x8 grid
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            # Vandrette linjer: starter ved venstre kant (x = 0), og går til højre kant (x = 800)
            # y-koordinatet ændres for hver række (100 pixels mellem linjerne)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
            # Lodrette linjer: starter ved top (y = 0), og går ned til bunden (y = 800)
            # x-koodinaterne ændres ligesom før

def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'white', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'white', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)

def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        ''' elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn) '''
        all_moves_list.append(moves_list)
    return all_moves_list

def check_king(position, color):
    moves_list = []  # Starter med tom liste, og så tilføjer gyldige træk
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0),  (1, 1)]

    if color == 'white': # Identificerer hvilke brækker der er på ens holkd og hvilke der er mod en
        friendly_locations = white_locations
        enemy_locations = black_locations
    else:
        friendly_locations = black_locations
        enemy_locations = white_locations

    for d in directions:
        new_pos = (position[0] + d[0], position[1] + d[1])
        if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7: # Tjekker om nu position er indenfor brættet
            if new_pos not in friendly_locations:
                moves_list.append(new_pos)

    return moves_list


def check_queen(position, color):
    moves_list = [] # Igen, starter med en tom liste og tilføjer gyldige træk bagefter
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1),
                  (-1, -1), (-1, 1), (1, -1), (1, 1)]

    if color == 'white': # Skelner hvem der er med eller mod en igen
        friendly_locations = white_locations
        enemy_locations = black_locations
    else:
        friendly_locations = black_locations
        enemy_locations = white_locations

    for d in directions:
        for i in range(1, 8): 
            new_pos = (position[0] + d[0]*i, position[1] + d[1]*i) # Rykker dronningen
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                if new_pos in friendly_locations: # Ugyldigt træk, går igennem venlig brik
                    break
                moves_list.append(new_pos) # Gyldigt træk
                if new_pos in enemy_locations: # Gyldigt træk men kan ikke gå videre. Slår en modspillers brik
                    break
            else: # Ude for brættet
                break

    return moves_list


def check_bishop():
    pass

def check_rook():
    pass

def check_pawn(position, color):
    # Liste over mulige træk for bonden
    moves_list = []

    # Hvis bonden er hvid
    if color == 'white':
        # Tjek om feltet foran bonden er tomt og inden for brættets grænse
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            # Tilføj feltet som et muligt træk
            moves_list.append((position[0], position[1] + 1))

        # Tjek om bonden står på sin startposition og begge felter foran er tomme
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            # Tilføj dobbeltspring som muligt træk
            moves_list.append((position[0], position[1] + 2))

        # Tjek om der er en sort brik skråt frem til højre, som kan slås
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))

        # Tjek om der er en sort brik skråt frem til venstre, som kan slås
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

    # Hvis bonden er sort
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))

        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))

        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))

        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))

    # Returnér listen med alle mulige træk for bonden
    return moves_list


def check_knight():
    pass

def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_moves = options_list[selection]
    return valid_moves

def draw_valid(moves):
    if turn_step < 2:
        color = 'white'
    else:
        color = 'white'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

def draw_captured():
    pass

def draw_check():
    pass

def draw_game_over():
    pass


black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    screen.fill('light gray')
    draw_board()
    draw_pieces()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # hvis venstre museknap trykkes ned og spillet ikke er slut
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # Udregn koodinaterne på brættet baseret på musepositionen
            x_coord = event.pos[0] // 100 # Dividerer med 100 fordi hver felt er 100 pixels
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord) # Gem klik-koordinaterne som en tuple

            # Hvids tur (turn_step 0 og 1)
            if turn_step <= 1:
                # Hvis man klikker på en hvid brik
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords) # Find hvilken brik der blev valgt
                    if turn_step == 0:
                        turn_step = 1 # Gå til næste trin: vælge felt at flytte til

                # Hvis man klikker på et gyldigt felt
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    # Hvis der står en sort brik der, skal den fjernes
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])

                        # Fjern sort brik fra spillet
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    
                    # Opdater muligheder for begge farver
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

                    # Skift tur til sort
                    turn_step = 2
                    selection = 100 # Ingen brik er længere valgt
                    valid_moves = [] # Ryd listen over gyldige træk

            # Sorts tur (turn_step 2 og 3)        
            if turn_step > 1:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []

    pygame.display.flip()
pygame.quit()
