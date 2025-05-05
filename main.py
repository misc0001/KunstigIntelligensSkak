import pygame
import chess_rules
from chess_rules import update_half_move_clock, is_fifty_move_draw
from chess_rules import record_position, is_threefold_repetition_draw


pygame.init()

WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
menu_state = True
save_string = ''
input_active = False
input_text = ''
check_message_timer = 0
CHECK_MESSAGE_DURATION = 60  # frames (1 sekund at 60 FPS)


white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
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
en_passant_possible = None 

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
last_move = None
en_passant_possible = None

def draw_menu():
    screen.fill('light gray')
    title = big_font.render("Velkommen til Skak!", True, 'black')
    new_game = font.render("Tryk 'N' for nyt spil", True, 'black')
    load_game = font.render("Tryk 'L' for at loade spil via streng", True, 'black')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(new_game, (WIDTH // 2 - new_game.get_width() // 2, 300))
    screen.blit(load_game, (WIDTH // 2 - load_game.get_width() // 2, 350))

def draw_text_input(text):
    input_label = font.render("Indtast gemt spilstreng og tryk Enter:", True, 'black')
    input_box = pygame.Rect(WIDTH // 2 - 200, 450, 400, 40)
    pygame.draw.rect(screen, 'white', input_box)
    pygame.draw.rect(screen, 'black', input_box, 2)
    input_text_surface = font.render(text, True, 'black')
    screen.blit(input_label, (WIDTH // 2 - input_label.get_width() // 2, 400))
    screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))


def check_options(pieces, locations, turn, last_move):
    moves_list = []
    all_moves_list = []
    if turn == 'white':
        enemy_pieces = black_pieces
        enemy_locations = black_locations
    else:
        enemy_pieces = white_pieces
        enemy_locations = white_locations
    
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = chess_rules.check_pawn(location, turn, white_locations, black_locations, last_move)
        elif piece == 'rook':
            moves_list = chess_rules.check_rook(location, turn, white_locations, black_locations)
        elif piece == 'queen':
            moves_list = chess_rules.check_queen(location, turn, white_locations, black_locations)
        elif piece == 'king':
            moves_list = chess_rules.check_king(
                location, turn,
                white_locations, black_locations,
                white_pieces, black_pieces,
                pieces
            )
        elif piece == 'knight':
            moves_list = chess_rules.check_knight(location, turn, white_locations, black_locations)
        elif piece == 'bishop':
            moves_list = chess_rules.check_bishop(location, turn, white_locations, black_locations)
        safe_moves = chess_rules.valid_moves(i, moves_list, pieces, locations,
                                             enemy_pieces, enemy_locations, turn, draw_check)
        all_moves_list.append(safe_moves)


    return all_moves_list

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
        # Highlight king if in check
    if draw_check(white_pieces, white_locations, black_pieces, black_locations, 'white'):
        king_index = white_pieces.index('king')
        king_pos = white_locations[king_index]
        pygame.draw.rect(screen, 'red', [king_pos[0]*100 + 1, king_pos[1]*100 + 1, 98, 98], 4)

    if draw_check(black_pieces, black_locations, white_pieces, white_locations, 'black'):
        king_index = black_pieces.index('king')
        king_pos = black_locations[king_index]
        pygame.draw.rect(screen, 'red', [king_pos[0]*100 + 1, king_pos[1]*100 + 1, 98, 98], 4)


def check_options(pieces, locations, turn, last_move):
    moves_list = []
    all_moves_list = []
    if turn == 'white':
        enemy_pieces = black_pieces
        enemy_locations = black_locations
    else:
        enemy_pieces = white_pieces
        enemy_locations = white_locations
    
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = chess_rules.check_pawn(location, turn, white_locations, black_locations, last_move)
        elif piece == 'rook':
            moves_list = chess_rules.check_rook(location, turn, white_locations, black_locations)
        elif piece == 'queen':
            moves_list = chess_rules.check_queen(location, turn, white_locations, black_locations)
        elif piece == 'king':
            moves_list = chess_rules.check_king(
                location, turn,
                white_locations, black_locations,
                white_pieces, black_pieces,
                pieces
            )
        elif piece == 'knight':
            moves_list = chess_rules.check_knight(location, turn, white_locations, black_locations)
        elif piece == 'bishop':
            moves_list = chess_rules.check_bishop(location, turn, white_locations, black_locations)
        safe_moves = chess_rules.valid_moves(i, moves_list, pieces, locations,
                                             enemy_pieces, enemy_locations, turn, draw_check)
        all_moves_list.append(safe_moves)


    return all_moves_list


def check_valid_moves(white_pieces, black_pieces):
    if turn_step < 2:
        options_list = white_options
        pieces = white_pieces
        locations = white_locations
        enemy_pieces = black_pieces
        enemy_locations = black_locations
        color = 'white'
    else:
        options_list = black_options
        pieces = black_pieces
        locations = black_locations
        enemy_pieces = white_pieces
        enemy_locations = white_locations
        color = 'black'

    # If in check, filter only safe moves
    if selection == 100 or selection >= len(options_list):
        return []
    
    valid_moves = options_list[selection]

    # Add en passant moves when appropriate
    if pieces[selection] == 'pawn' and en_passant_possible:
        piece_pos = locations[selection]
        if color == 'white' and piece_pos[1] == 4:  # White pawn on the 5th rank
            if abs(piece_pos[0] - en_passant_possible[0]) == 1:  # Adjacent column
                valid_moves.append(en_passant_possible)
        elif color == 'black' and piece_pos[1] == 3:  # Black pawn on the 4th rank
            if abs(piece_pos[0] - en_passant_possible[0]) == 1:  # Adjacent column
                valid_moves.append(en_passant_possible)

    # Filter out moves where the king moves to a square under attack
    if pieces[selection] == 'king':
        valid_moves_filtered = []
        for move in valid_moves:
        # Simulate moving the king
            temp_white = white_locations.copy()
            temp_black = black_locations.copy()
            temp_white_pieces = white_pieces.copy()
            temp_black_pieces = black_pieces.copy()

            if color == 'white':
                temp_white[selection] = move
            else:
                temp_black[selection] = move

            if not chess_rules.under_attack(move, color, temp_white, temp_black, temp_white_pieces, temp_black_pieces):
                valid_moves_filtered.append(move)
            valid_moves = valid_moves_filtered

    # If player is in check, filter valid moves to only those that fix the check
    if draw_check(pieces, locations, enemy_pieces, enemy_locations, color):
        valid_moves = chess_rules.valid_moves(selection, valid_moves, pieces, locations, enemy_pieces, enemy_locations, color, draw_check)
        
    if en_passant_possible and (en_passant_possible[0], en_passant_possible[1] + 1) in valid_moves:
        valid_moves.append((en_passant_possible[0], en_passant_possible[1] + 1))

    
    return valid_moves

def draw_valid(moves):
    if turn_step < 2:
        color = 'white'
    else:
        color = 'black'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

def draw_captured():
    pass

def draw_check(friendly_pieces, friendly_locations, enemy_pieces, enemy_locations, color):
    global check_message_timer
    if 'king' not in friendly_pieces:
        return True  # Definitely in check if the king was captured
    # Find king location
    king_pos = friendly_locations[friendly_pieces.index('king')]
    enemy_color = 'black' if color == 'white' else 'white'


    for idx in range(len(enemy_pieces)):
        piece = enemy_pieces[idx]
        pos = enemy_locations[idx]
        if piece == 'pawn':
            attacks = chess_rules.check_pawn(pos, enemy_color, white_locations, black_locations, last_move)
        elif piece == 'rook':
            attacks = chess_rules.check_rook(pos, enemy_color, white_locations, black_locations)
        elif piece == 'knight':
            attacks = chess_rules.check_knight(pos, enemy_color, white_locations, black_locations)
        elif piece == 'bishop':
            attacks = chess_rules.check_bishop(pos, enemy_color, white_locations, black_locations)
        elif piece == 'queen':
            attacks = chess_rules.check_queen(pos, enemy_color, white_locations, black_locations)
        elif piece == 'king':
            attacks = chess_rules.check_king(
                pos, enemy_color,
                white_locations, black_locations,
                white_pieces, black_pieces,
                (white_pieces if enemy_color=='white' else black_pieces)
            )

        if king_pos in attacks:
            check_message_timer = CHECK_MESSAGE_DURATION
            return True
    return False

def draw_game_over():
    if winner == 'white':
        text = big_font.render('Checkmate! White wins!', True, 'red')
    elif winner == 'black':
        text = big_font.render('Checkmate! Black wins!', True, 'red')
    else:
        text = big_font.render('Stalemate! Draw.', True, 'gray')
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_timer(time_left):
    timer_text = big_font.render(f'Time: {time_left}', True, 'black')
    text_rect = timer_text.get_rect (center=(900, 50))  # Draw timer on the right
    screen.blit(timer_text, text_rect)

def draw_check_message():
    global check_message_timer
    if check_message_timer > 0:
        check_message_timer -= 1
        alpha = int(255 * (check_message_timer / CHECK_MESSAGE_DURATION))
        text_surface = big_font.render("CHECK!", True, (255, 0, 0))
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (820, 200))  # Position beside board

def draw_promotion_message():
    promotion_text = font.render('Promote: (Q)ueen, (R)ook, (B)ishop, (K)night', True, 'black')
    text_rect = promotion_text.get_rect(center=(900, 120))
    screen.blit(promotion_text, text_rect)


black_options = check_options(black_pieces, black_locations, 'black', last_move)
white_options = check_options(white_pieces, white_locations, 'white', last_move)
run = True
while run:
    timer.tick(fps)
    screen.fill('light gray')
    turn_step, selection_reset, valid_moves_reset, time_left = chess_rules.turn_timer(turn_step)
    
    draw_board()
    draw_pieces()
    draw_timer(time_left)  # 👈 Show timer after board and pieces
    draw_check_message()


    # Check if time expired

    if selection_reset is not None:
        selection = selection_reset
        valid_moves = valid_moves_reset
        black_options = check_options(black_pieces, black_locations, 'black', last_move)
        white_options = check_options(white_pieces, white_locations, 'white', last_move)
        chess_rules.reset_turn_timer()

    if selection != 100:
        valid_moves = check_valid_moves(white_pieces, black_pieces)
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
                if selection != 100 and valid_moves and click_coords in valid_moves:
                    old_pos = white_locations[selection]
                    white_locations[selection] = click_coords
                    last_move = (old_pos, click_coords)


                     # 50-move rule: reset on pawn-move or capture, else increment
                    update_half_move_clock(
                        click_coords in black_locations,
                        white_pieces[selection] == 'pawn'
                    )
                    if is_fifty_move_draw():
                        game_over = True
                        winner   = 'draw'

                     # 🛠 Check for castling move
                    if white_pieces[selection] == 'king':
                        old_pos = white_locations[selection]
                        if click_coords == (6, 0) and old_pos == (4, 0): # Kingside castling
                            if (6, 0) in valid_moves:  # This ensures all castling conditions are met
                                rook_index = white_locations.index((7, 0))
                                white_locations[rook_index] = (5, 0)
                        elif click_coords == (2, 0) and old_pos == (4, 0):  # Queenside castling
                            if (2, 0) in valid_moves:
                                rook_index = white_locations.index((0, 0))
                                white_locations[rook_index] = (3, 0)

                    chess_rules.update_castling_rights(white_pieces[selection], old_pos, 'white')
                    
                    # Check for en passant capture
                    if white_pieces[selection] == 'pawn' and old_pos[1] == 4 and abs(click_coords[0] - old_pos[0]) == 1 and click_coords[1] == 5:
                        # This is a diagonal pawn move - could be en passant
                        capture_pos = (click_coords[0], 4)  # The black pawn's position (same column as destination, row 4)
                        if capture_pos in black_locations and (click_coords not in black_locations):
                            # It's an en passant capture!
                            idx = black_locations.index(capture_pos)
                            if black_pieces[idx] == 'pawn':
                                captured_pieces_white.append(black_pieces[idx])
                                black_pieces.pop(idx)
                                black_locations.pop(idx)
                    
                    # Set en passant flag if this was a double move
                    if white_pieces[selection] == 'pawn' and abs(click_coords[1] - old_pos[1]) == 2:
                        en_passant_possible = (click_coords[0], click_coords[1] - 1)
                    else:
                        en_passant_possible = None
                                

                    
                    # Hvis der står en sort brik der, skal den fjernes
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        if black_pieces[black_piece] == 'king':
                            pass  # Don't allow capturing the king
                        captured_pieces_white.append(black_pieces[black_piece])

                        # Fjern sort brik fra spillet
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)

                        last_move = (old_pos, click_coords)

                    chess_rules.pawn_promotion(white_pieces, white_locations, 'white')

                    # Before resetting turn
                    if white_pieces[selection] == 'pawn' and abs(click_coords[1] - old_pos[1]) == 2:
                        en_passant_possible = (click_coords[0], click_coords[1] - 1)  # square behind pawn
                    else:
                        en_passant_possible = None

                    # Opdater muligheder for begge farver
                    black_options = check_options(black_pieces, black_locations, 'black', last_move)
                    white_options = check_options(white_pieces, white_locations, 'white', last_move)

                    # threefold-repetition: record and immediately check
                    if record_position(
                            white_pieces,   white_locations,
                            black_pieces,   black_locations,
                            'white',        en_passant_possible
                        ) >= 3:
                        game_over = True
                        winner   = 'draw'

                    # Skift tur til sort
                    turn_step = 2
                    selection = 100 # Ingen brik er længere valgt
                    valid_moves = [] # Ryd listen over gyldige træk
                    chess_rules.reset_turn_timer() # Reset timer

                    if chess_rules.check_stalemate(black_pieces, black_locations, white_pieces, white_locations, 'black', 
                                                   draw_check, white_locations, black_locations, white_pieces, black_pieces):
                        game_over = True
                        winner = 'draw'
                    elif chess_rules.check_checkmate(black_pieces, black_locations, white_pieces, white_locations,
                                 'black', draw_check, white_locations, black_locations,
                                 white_pieces, black_pieces):
                        game_over = True
                        winner = 'white'



            # Sorts tur (turn_step 2 og 3)        
            if turn_step > 1:
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    old_pos = black_locations[selection]

                    if click_coords in white_locations:
                            idx = white_locations.index(click_coords)
                            if white_pieces[idx] != 'king':  # optional: forbid king captures
                                captured_pieces_black.append(white_pieces[idx])
                                white_pieces.pop(idx)
                                white_locations.pop(idx)
                            black_locations[selection] = click_coords


                    if black_pieces[selection] == 'king':
                        old_pos = black_locations[selection]
                        

                        if click_coords == (6, 7):
                            old_pos = black_locations[selection]
                            if click_coords == (6, 7) and old_pos == (4, 7):  # Kongeside 
                                if (6, 7) in valid_moves:  # Verifikation
                                    rook_index = black_locations.index((7, 7))
                                    black_locations[rook_index] = (5, 7)
                            elif click_coords == (2, 7) and old_pos == (4, 7):  # Dronning side
                                if (2, 7) in valid_moves:
                                    rook_index = black_locations.index((0, 7))
                                    black_locations[rook_index] = (3, 7)

                    black_locations[selection] = click_coords

                    update_half_move_clock(
                        click_coords in white_locations,
                        black_pieces[selection] == 'pawn'
                    )
                    if is_fifty_move_draw():
                        game_over = True
                        winner   = 'draw'

                    chess_rules.update_castling_rights(
                       black_pieces[selection], old_pos, 'black')

                    chess_rules.pawn_promotion(
                       black_pieces, black_locations, 'black')
                        
                    if (black_pieces[selection] == 'pawn'
                        and old_pos[1] == 3
                        and abs(click_coords[0] - old_pos[0]) == 1
                        and click_coords[1] == 2):
                        capture_pos = (click_coords[0], 3)
                        if capture_pos in white_locations and click_coords not in white_locations:
                            idx = white_locations.index(capture_pos)
                            captured_pieces_black.append(white_pieces[idx])
                            white_pieces.pop(idx)
                            white_locations.pop(idx)

                    # 4) En passant *target* (double-step)
                    if black_pieces[selection] == 'pawn' and old_pos[1] and abs(click_coords[1] - old_pos[1]) == 2:
                        en_passant_possible = (click_coords[0], click_coords[1] + 1)
                    else:
                        en_passant_possible = None

                    
                    last_move = (old_pos, click_coords)

                   # Track black double pawn move for en passant
                    if black_pieces[selection] == 'pawn' and abs(click_coords[1] - old_pos[1]) == 2:
                        en_passant_possible = (click_coords[0], click_coords[1] + 1)
                    else:
                        en_passant_possible = None

                    black_options = check_options(black_pieces, black_locations, 'black', last_move)
                    white_options = check_options(white_pieces, white_locations, 'white', last_move)

                    if record_position(
                            white_pieces,   white_locations,
                            black_pieces,   black_locations,
                            'black',        en_passant_possible
                        ) >= 3:
                        game_over = True
                        winner   = 'draw'

                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    chess_rules.reset_turn_timer()

                    if chess_rules.check_stalemate(white_pieces, white_locations, black_pieces, black_locations, 'white',
                                                   draw_check, white_locations, black_locations, white_pieces, black_pieces):
                        game_over = True
                        winner = 'draw'
                    elif chess_rules.check_checkmate(white_pieces, white_locations, black_pieces, black_locations,
                                 'white', draw_check, white_locations, black_locations,
                                 white_pieces, black_pieces):
                        game_over = True
                        winner = 'black'
                    if game_over:
                        draw_game_over()


    pygame.display.flip()
pygame.quit()



