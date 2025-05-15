import pygame
import chess_rules
from chess_rules import update_half_move_clock, is_fifty_move_draw
from chess_rules import record_position, is_threefold_repetition_draw
from chess_rules import valid_moves


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
CHECK_MESSAGE_DURATION = 60

piece_values = {
    'pawn': 1,
    'knight': 3,
    'bishop': 3,
    'rook': 5,
    'queen': 9,
    'king': 0 
}


white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

captured_pieces_white = []
captured_pieces_black = []

turn_step = 0
selection = 100
valid_moves = []
en_passant_possible = None 
player_color = None  # 'white' or 'black'
color_selection_active = True  # New state to manage color selection screen

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


def draw_text_input(text):
    input_label = font.render("Indtast gemt spilstreng og tryk Enter:", True, 'black')
    input_box = pygame.Rect(WIDTH // 2 - 200, 450, 400, 40)
    pygame.draw.rect(screen, 'white', input_box)
    pygame.draw.rect(screen, 'black', input_box, 2)
    input_text_surface = font.render(text, True, 'black')
    screen.blit(input_label, (WIDTH // 2 - input_label.get_width() // 2, 400))
    screen.blit(input_text_surface, (input_box.x + 10, input_box.y + 5))

def draw_color_selection():
    screen.fill('light gray')
    title = big_font.render("Vælg farve", True, 'black')
    white_option = font.render("Tryk 'W' for at spille som hvid", True, 'black')
    black_option = font.render("Tryk 'B' for at spille som sort", True, 'black')
    load_game_from_string = font.render("Tryk 'L' for at loade et spil", True, 'black')
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(white_option, (WIDTH // 2 - white_option.get_width() // 2, 300))
    screen.blit(black_option, (WIDTH // 2 - black_option.get_width() // 2, 350))
    screen.blit(load_game_from_string, (WIDTH // 2 - load_game_from_string.get_width() // 2, 500))


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


def evaluate_board(white_pieces, white_locations, black_pieces, black_locations):
    piece_values = {
        'pawn': 1,
        'knight': 3,
        'bishop': 3,
        'rook': 5,
        'queen': 9,
        'king': 0
    }
 
    center_weight_table = [
        [0, 1, 2, 3, 3, 2, 1, 0],
        [1, 2, 3, 4, 4, 3, 2, 1],
        [2, 3, 4, 5, 5, 4, 3, 2],
        [3, 4, 5, 6, 6, 5, 4, 3],
        [3, 4, 5, 6, 6, 5, 4, 3],
        [2, 3, 4, 5, 5, 4, 3, 2],
        [1, 2, 3, 4, 4, 3, 2, 1],
        [0, 1, 2, 3, 3, 2, 1, 0]
    ]
 
    white_score = 0
    black_score = 0
 
    for piece, loc in zip(white_pieces, white_locations):
        base = piece_values.get(piece, 0)
        x, y = loc
        white_score += base
        white_score += center_weight_table[y][x] * 0.1  # Positional bonus
        if chess_rules.under_attack(loc, 'white', white_locations, black_locations, white_pieces, black_pieces):
            attackers = check_options(black_pieces, black_locations, 'black', last_move)
            total_threat_value = 0
            for i, moves in enumerate(attackers):
                if loc in moves:
                    total_threat_value += piece_values.get(black_pieces[i], 0)
            white_score -= base + 0.4 * total_threat_value
 
    for piece, loc in zip(black_pieces, black_locations):
        base = piece_values.get(piece, 0)
        x, y = loc
        black_score += base
        black_score += center_weight_table[7 - y][x] * 0.1  # Mirror table for black
        if chess_rules.under_attack(loc, 'black', black_locations, white_locations, black_pieces, white_pieces):
            attackers = check_options(black_pieces, black_locations, 'black', last_move)
            total_threat_value = 0
            for i, moves in enumerate(attackers):
                if loc in moves:
                    total_threat_value += piece_values.get(white_pieces[i], 0)
            black_score -= base + 0.4 * total_threat_value
 
    # Encourage putting the enemy king in check
    if draw_check(black_pieces, black_locations, white_pieces, white_locations, 'white'):
        black_score += 1.5  # reward checking white king
    if draw_check(white_pieces, white_locations, black_pieces, black_locations, 'black'):
        white_score += 1.5  # reward checking black king
 
    return white_score - black_score



def minimax(depth, is_maximizing, alpha, beta, white_pieces, white_locations, black_pieces, black_locations):
    if depth == 0:
        return evaluate_board(white_pieces, white_locations, black_pieces, black_locations)
 
    # Assign state depending on turn
    if is_maximizing:
        best_score = float('-inf')
        pieces, locations = white_pieces, white_locations
        enemy_pieces, enemy_locations = black_pieces, black_locations
        turn = 'white'
    else:
        best_score = float('inf')
        pieces, locations = black_pieces, black_locations
        enemy_pieces, enemy_locations = white_pieces, white_locations
        turn = 'black'
 
    options = check_options(pieces, locations, turn, last_move)

    
 
    for piece_idx, moves in enumerate(options):
        for move in moves:
            # Clone state
            new_white_pieces = white_pieces[:]
            new_white_locations = white_locations[:]
            new_black_pieces = black_pieces[:]
            new_black_locations = black_locations[:]

            trade_bonus = 0
            if is_maximizing and move in black_locations:
                capture_idx = black_locations.index(move)
                captured_value = piece_values.get(black_pieces[capture_idx], 0)
                own_value = piece_values.get(white_pieces[piece_idx], 0)
                trade_bonus = (captured_value - own_value) * 0.4
            elif not is_maximizing and move in white_locations:
                capture_idx = white_locations.index(move)
                captured_value = piece_values.get(white_pieces[capture_idx], 0)
                own_value = piece_values.get(black_pieces[piece_idx], 0)
                trade_bonus = (captured_value - own_value) * 0.4
 
            # Make the move
            if is_maximizing:
                new_white_locations[piece_idx] = move
                if move in black_locations:
                    capture_idx = black_locations.index(move)
                    new_black_pieces.pop(capture_idx)
                    new_black_locations.pop(capture_idx)
            else:
                new_black_locations[piece_idx] = move
                if move in white_locations:
                    capture_idx = white_locations.index(move)
                    new_white_pieces.pop(capture_idx)
                    new_white_locations.pop(capture_idx)
 
            # --- Simulér modstanderens næste træk og vurder faren ---
            if is_maximizing:
                simulated_threats = check_options(new_black_pieces, new_black_locations, 'black', last_move)
                for threat_idx, moves in enumerate(simulated_threats):
                    for m in moves:
                        if m in new_white_locations:
                            piece = new_white_pieces[new_white_locations.index(m)]
                            score_penalty = piece_values.get(piece, 0)
                            best_score -= score_penalty * 0.4  # Straf for udsat brik
            else:
                simulated_threats = check_options(new_white_pieces, new_white_locations, 'white', last_move)
                for threat_idx, moves in enumerate(simulated_threats):
                    for m in moves:
                        if m in new_black_locations:
                            piece = new_black_pieces[new_black_locations.index(m)]
                            score_penalty = piece_values.get(piece, 0)
                            best_score += score_penalty * 0.4
 
            # Recursive call
            score = minimax(depth - 5, not is_maximizing, alpha, beta,
                            new_white_pieces, new_white_locations,
                            new_black_pieces, new_black_locations) + trade_bonus
 
            # Update best score and prune
            if is_maximizing:
                if score > best_score:
                    best_score = score
                alpha = max(alpha, best_score)
            else:
                if score < best_score:
                    best_score = score
                beta = min(beta, best_score)
 
            if beta <= alpha:
                return best_score  # immediate cutoff
           
            if is_maximizing:
                if move in black_locations:
                    capture_idx = black_locations.index(move)
                    captured_value = piece_values.get(black_pieces[capture_idx], 0)
                    own_value = piece_values.get(white_pieces[piece_idx], 0)
                    score += (captured_value - own_value) * 0.5  # Belønning for god byttehandel
            else:
                if move in white_locations:
                    capture_idx = white_locations.index(move)
                    captured_value = piece_values.get(white_pieces[capture_idx], 0)
                    own_value = piece_values.get(black_pieces[piece_idx], 0)
                    score += (captured_value - own_value) * 0.5
 
 
    return best_score



def find_best_move(white_pieces, white_locations, black_pieces, black_locations, depth, is_white_turn):
    best_score = float('-inf') if is_white_turn else float('inf')
    best_piece_idx = -1
    best_move = None
    alpha = float('-inf')
    beta = float('inf')
   
    if is_white_turn:
        pieces = white_pieces
        locations = white_locations
        options = check_options(white_pieces, white_locations, 'white', last_move)
        enemy_pieces = black_pieces
        enemy_locations = black_locations
    else:
        pieces = black_pieces
        locations = black_locations
        options = check_options(black_pieces, black_locations, 'black', last_move)
        enemy_pieces = white_pieces
        enemy_locations = white_locations
   
    for piece_idx in range(len(pieces)):
        legal_moves = chess_rules.valid_moves(
            piece_idx, options[piece_idx],
            pieces, locations,
            enemy_pieces, enemy_locations,
            'white' if is_white_turn else 'black',
            draw_check
        )
        for move in legal_moves:
            new_white_pieces = white_pieces.copy()
            new_white_locations = white_locations.copy()
            new_black_pieces = black_pieces.copy()
            new_black_locations = black_locations.copy()
           
            if is_white_turn:
                new_white_locations[piece_idx] = move
                if move in black_locations:
                    captured_idx = black_locations.index(move)
                    new_black_pieces.pop(captured_idx)
                    new_black_locations.pop(captured_idx)
            else:
                new_black_locations[piece_idx] = move
                if move in white_locations:
                    captured_idx = white_locations.index(move)
                    new_white_pieces.pop(captured_idx)
                    new_white_locations.pop(captured_idx)
           
            score = minimax(depth - 1, not is_white_turn, alpha, beta,
                           new_white_pieces, new_white_locations,
                           new_black_pieces, new_black_locations)
           
            if (is_white_turn and score > best_score) or (not is_white_turn and score < best_score):
                best_score = score
                best_piece_idx = piece_idx
                best_move = move
           
            if is_white_turn:
                alpha = max(alpha, best_score)
            else:
                beta = min(beta, best_score)
           
            if beta <= alpha:
                break
       
        if beta <= alpha:
            break
   
    return best_piece_idx, best_move

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

def print_board_state():
    board_state = []

    for piece, loc in zip(white_pieces, white_locations):
        board_state.append(f"W_{piece}@{loc[0]}{loc[1]}")
    for piece, loc in zip(black_pieces, black_locations):
        board_state.append(f"B_{piece}@{loc[0]}{loc[1]}")

    print(" | ".join(board_state))

def load_game_from_string(save_string):
    global white_pieces, white_locations, black_pieces, black_locations, turn_step, player_color
    white_pieces.clear()
    white_locations.clear()
    black_pieces.clear()
    black_locations.clear()

    if ':' in save_string:
        player_color_prefix, save_data = save_string.split(':', 1)
        player_color = 'white' if player_color_prefix.upper() == 'W' else 'black'
    else:
        save_data = save_string
        player_color = 'white'  # fallback

    pieces = save_data.strip().split('|')
    for entry in pieces:
        entry = entry.strip()
        if not entry:
            continue
        color_piece, pos = entry.split('@')
        color, piece = color_piece.split('_')
        x, y = int(pos[0]), int(pos[1])
        if color == 'W':
            white_pieces.append(piece)
            white_locations.append((x, y))
        elif color == 'B':
            black_pieces.append(piece)
            black_locations.append((x, y))

    turn_step = 0 if player_color == 'white' else 2

    global white_options, black_options
    white_options = check_options(white_pieces, white_locations, 'white', last_move)
    black_options = check_options(black_pieces, black_locations, 'black', last_move)



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

    if selection == 100 or selection >= len(options_list):
        return []

    valid_moves = options_list[selection][:]

    # --- Castling ---
    if pieces[selection] == 'king':
        valid_moves += chess_rules.castling_move(
            pieces, locations, color,
            white_locations, black_locations,
            white_pieces, black_pieces
        )

    # --- King safety: can't move into attacked square
    if pieces[selection] == 'king':
        valid_moves = [
            move for move in valid_moves
            if not chess_rules.under_attack(
                move, color,
                white_locations, black_locations,
                white_pieces, black_pieces
            )
        ]

    # --- In-check: only allow moves that resolve check ---
    if draw_check(pieces, locations, enemy_pieces, enemy_locations, color):
        valid_moves = []
        king_index = pieces.index('king')
        king_pos = locations[king_index]

        for i in range(len(pieces)):
            simulated_moves = chess_rules.valid_moves(
                i, options_list[i],
                pieces, locations,
                enemy_pieces, enemy_locations,
                color, draw_check
            )
            if i == selection:
                valid_moves.extend(simulated_moves)

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

def check_valid_moves_for_index(pieces, enemy_pieces, index, is_white):
    options = check_options(
        pieces,
        white_locations if is_white else black_locations,
        'white' if is_white else 'black',
        last_move
    )
    locations = white_locations if is_white else black_locations
    enemy_locations = black_locations if is_white else white_locations
    color = 'white' if is_white else 'black'
    
    return chess_rules.valid_moves(index, options[index], pieces, locations, enemy_pieces, enemy_locations, color, draw_check)


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
# Initialize color selection variables
color_selection_active = True
player_color = None

while run:
    timer.tick(fps)
    
    if color_selection_active:
        screen.fill('light gray')
        draw_color_selection()
        if input_active:
            draw_text_input(input_text)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        load_game_from_string(input_text)
                        input_text = ''
                        input_active = False
                        color_selection_active = False
                        # Player color is set based on loaded string
                        turn_step = 0 if player_color == 'white' else 2
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        # Handle paste (Ctrl+V)
                        if event.key == pygame.K_v and pygame.key.get_mods() & pygame.KMOD_CTRL:
                            try:
                                import pyperclip
                                paste_data = pyperclip.paste()
                                input_text += paste_data
                            except:
                                pass  # fallback if pyperclip not available
                        elif len(input_text) < 100:
                            input_text += event.unicode
                else:
                    if event.key == pygame.K_w:
                        player_color = 'white'
                        color_selection_active = False
                        turn_step = 0  # White goes first
                    elif event.key == pygame.K_b:
                        player_color = 'black'
                        color_selection_active = False
                        turn_step = 0  # Black's turn (AI will play white first)
                    elif event.key == pygame.K_l:
                        input_active = True
        pygame.display.flip()
        continue  # Skip the rest of the game loop

    
    # Existing game code follows...
    screen.fill('light gray')
    selection_reset = None
    valid_moves_reset = []
    
    draw_board()
    draw_pieces()
    #draw_timer(time_left)  # Show timer after board and pieces
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

    # Handle AI move after a player's move or when it's AI's turn
    if ((player_color == 'white' and turn_step > 1) or (player_color == 'black' and turn_step <= 1)) and not game_over:
        # AI move logic
        if player_color == 'white':
            # AI is black
            piece_idx, move = find_best_move(white_pieces, white_locations, black_pieces, black_locations, 
                                             depth=6, is_white_turn=False)
            if piece_idx != -1 and move is not None:
                selection = piece_idx
                old_pos = black_locations[selection]
                
                # Handle capture
                if move in white_locations:
                    white_piece = white_locations.index(move)
                    captured_pieces_black.append(white_pieces[white_piece])
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                
                # Handle castling
                if black_pieces[selection] == 'king':
                    if move == (6, 7) and old_pos == (4, 7):  # Kingside
                        selection = black_pieces.index('king')  # <-- Set selection first
                        if (6, 7) in check_valid_moves(black_pieces, white_pieces):
                            rook_index = black_locations.index((7, 7))
                            black_locations[rook_index] = (5, 7)
                    elif move == (2, 7) and old_pos == (4, 7):  # Queenside
                        selection = black_pieces.index('king')  # <-- Set selection again
                        if (2, 7) in check_valid_moves(black_pieces, white_pieces):
                            rook_index = black_locations.index((0, 7))
                            black_locations[rook_index] = (3, 7)
                
                # En passant capture
                if (black_pieces[selection] == 'pawn'
                    and old_pos[1] == 3
                    and abs(move[0] - old_pos[0]) == 1
                    and move[1] == 2):
                    capture_pos = (move[0], 3)
                    if capture_pos in white_locations and move not in white_locations:
                        idx = white_locations.index(capture_pos)
                        captured_pieces_black.append(white_pieces[idx])
                        white_pieces.pop(idx)
                        white_locations.pop(idx)
                
                # Make the move
                black_locations[selection] = move
                last_move = (old_pos, move)
                

                
                # Update en passant possibility
                if black_pieces[selection] == 'pawn' and abs(move[1] - old_pos[1]) == 2:
                    en_passant_possible = (move[0], move[1] + 1)
                else:
                    en_passant_possible = None
                
                # Update half-move clock
                update_half_move_clock(
                    move in white_locations,
                    black_pieces[selection] == 'pawn'
                )
                
                # Handle promotion
                chess_rules.pawn_promotion(black_pieces, black_locations, 'black')
                
                # Update castling rights
                chess_rules.update_castling_rights(black_pieces[selection], old_pos, 'black')
                
                # Update game state
                black_options = check_options(black_pieces, black_locations, 'black', last_move)
                white_options = check_options(white_pieces, white_locations, 'white', last_move)
                
                # Check for repetition
                if record_position(
                        white_pieces, white_locations,
                        black_pieces, black_locations,
                        'black', en_passant_possible
                    ) >= 3:
                    game_over = True
                    winner = 'draw'
                
                # Switch turn
                turn_step = 0
                selection = 100
                valid_moves = []
                chess_rules.reset_turn_timer()
                
                # Check game over conditions
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
        else:
            # AI is white
            piece_idx, move = find_best_move(white_pieces, white_locations, black_pieces, black_locations, 
                                             depth=6, is_white_turn=True)
            if piece_idx != -1 and move is not None:
                selection = piece_idx
                old_pos = white_locations[selection]
                
                # Handle capture
                if move in black_locations:
                    black_piece = black_locations.index(move)
                    if black_pieces[black_piece] != 'king':  # Don't allow capturing the king
                        captured_pieces_white.append(black_pieces[black_piece])
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                
                # Handle castling
                if white_pieces[selection] == 'king':
                    if move == (6, 0) and old_pos == (4, 0):  # Kingside
                        if (6, 0) in check_valid_moves(white_pieces, black_pieces, selection):
                            rook_index = white_locations.index((7, 0))
                            white_locations[rook_index] = (5, 0)
                    elif move == (2, 0) and old_pos == (4, 0):  # Queenside
                        if (2, 0) in check_valid_moves(white_pieces, black_pieces, selection):
                            rook_index = white_locations.index((0, 0))
                            white_locations[rook_index] = (3, 0)
                
                # En passant capture
                if white_pieces[selection] == 'pawn' and old_pos[1] == 4 and abs(move[0] - old_pos[0]) == 1 and move[1] == 5:
                    capture_pos = (move[0], 4)
                    if capture_pos in black_locations and move not in black_locations:
                        idx = black_locations.index(capture_pos)
                        if black_pieces[idx] == 'pawn':
                            captured_pieces_white.append(black_pieces[idx])
                            black_pieces.pop(idx)
                            black_locations.pop(idx)
                
                # Make the move
                white_locations[selection] = move
                last_move = (old_pos, move)
                
                # Update en passant possibility
                if white_pieces[selection] == 'pawn' and abs(move[1] - old_pos[1]) == 2:
                    en_passant_possible = (move[0], move[1] - 1)
                else:
                    en_passant_possible = None
                
                # Update half-move clock
                update_half_move_clock(
                    move in black_locations,
                    white_pieces[selection] == 'pawn'
                )
                
                # Handle promotion
                chess_rules.pawn_promotion(white_pieces, white_locations, 'white')
                
                # Update castling rights
                chess_rules.update_castling_rights(white_pieces[selection], old_pos, 'white')
                
                # Update game state
                black_options = check_options(black_pieces, black_locations, 'black', last_move)
                white_options = check_options(white_pieces, white_locations, 'white', last_move)
                
                # Check for repetition
                if record_position(
                        white_pieces, white_locations,
                        black_pieces, black_locations,
                        'white', en_passant_possible
                    ) >= 3:
                    game_over = True
                    winner = 'draw'
                
                # Switch turn
                turn_step = 2
                selection = 100
                valid_moves = []
                chess_rules.reset_turn_timer()
                
                # Check game over conditions
                if chess_rules.check_stalemate(black_pieces, black_locations, white_pieces, white_locations, 'black',
                                            draw_check, white_locations, black_locations, white_pieces, black_pieces):
                    game_over = True
                    winner = 'draw'
                elif chess_rules.check_checkmate(black_pieces, black_locations, white_pieces, white_locations,
                            'black', draw_check, white_locations, black_locations,
                            white_pieces, black_pieces):
                    game_over = True
                    winner = 'white'
                
                if game_over:
                    draw_game_over()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Mouse click and player's turn based on selected color
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # Calculate board coordinates from mouse position
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            
            # Player's turn - only handle input if it's the player's turn
            if (player_color == 'white' and turn_step <= 1) or (player_color == 'black' and turn_step > 1):
                if player_color == 'white':
                    # White player's turn
                    if turn_step <= 1:
                        # Handle piece selection
                        if click_coords in white_locations:
                            selection = white_locations.index(click_coords)
                            if turn_step == 0:
                                turn_step = 1
                        
                        # Handle move
                        if selection != 100 and valid_moves and click_coords in valid_moves:
                            old_pos = white_locations[selection]
                            white_locations[selection] = click_coords
                            last_move = (old_pos, click_coords)
                            print_board_state()

                            
                            # 50-move rule
                            update_half_move_clock(
                                click_coords in black_locations,
                                white_pieces[selection] == 'pawn'
                            )
                            if is_fifty_move_draw():
                                game_over = True
                                winner = 'draw'
                                
                            # Handle castling
                            if white_pieces[selection] == 'king':
                                if click_coords == (6, 0) and old_pos == (4, 0):  # Kingside
                                    if (6, 0) in valid_moves:
                                        rook_index = white_locations.index((7, 0))
                                        white_locations[rook_index] = (5, 0)
                                elif click_coords == (2, 0) and old_pos == (4, 0):  # Queenside
                                    if (2, 0) in valid_moves:
                                        rook_index = white_locations.index((0, 0))
                                        white_locations[rook_index] = (3, 0)
                            
                            chess_rules.update_castling_rights(white_pieces[selection], old_pos, 'white')
                            
                            # En passant capture
                            if white_pieces[selection] == 'pawn' and old_pos[1] == 4 and abs(click_coords[0] - old_pos[0]) == 1 and click_coords[1] == 5:
                                capture_pos = (click_coords[0], 4)
                                if capture_pos in black_locations and (click_coords not in black_locations):
                                    idx = black_locations.index(capture_pos)
                                    if black_pieces[idx] == 'pawn':
                                        captured_pieces_white.append(black_pieces[idx])
                                        black_pieces.pop(idx)
                                        black_locations.pop(idx)
                            
                            # Set en passant flag
                            if white_pieces[selection] == 'pawn' and abs(click_coords[1] - old_pos[1]) == 2:
                                en_passant_possible = (click_coords[0], click_coords[1] - 1)
                            else:
                                en_passant_possible = None
                            
                            # Handle capture
                            if click_coords in black_locations:
                                black_piece = black_locations.index(click_coords)
                                if black_pieces[black_piece] == 'king':
                                    pass  # Don't allow capturing the king
                                else:
                                    captured_pieces_white.append(black_pieces[black_piece])
                                    black_pieces.pop(black_piece)
                                    black_locations.pop(black_piece)
                            
                            chess_rules.pawn_promotion(white_pieces, white_locations, 'white')
                            
                            # Update options
                            black_options = check_options(black_pieces, black_locations, 'black', last_move)
                            white_options = check_options(white_pieces, white_locations, 'white', last_move)
                            
                            # Check for repetition
                            if record_position(
                                    white_pieces, white_locations,
                                    black_pieces, black_locations,
                                    'white', en_passant_possible
                                ) >= 3:
                                game_over = True
                                winner = 'draw'
                            
                            # Switch to black's turn
                            turn_step = 2
                            selection = 100
                            valid_moves = []
                            #chess_rules.reset_turn_timer()
                            
                            # Check for stalemate/checkmate
                            if chess_rules.check_stalemate(black_pieces, black_locations, white_pieces, white_locations, 'black', 
                                                        draw_check, white_locations, black_locations, white_pieces, black_pieces):
                                game_over = True
                                winner = 'draw'
                            elif chess_rules.check_checkmate(black_pieces, black_locations, white_pieces, white_locations,
                                        'black', draw_check, white_locations, black_locations,
                                        white_pieces, black_pieces):
                                game_over = True
                                winner = 'white'
                                
                            if game_over:
                                draw_game_over()
                else:
                    # Black player's turn
                    if turn_step > 1:
                        # Handle piece selection
                        if click_coords in black_locations:
                            selection = black_locations.index(click_coords)
                            if turn_step == 2:
                                turn_step = 3
                        
                        # Handle move
                        if click_coords in valid_moves and selection != 100:
                            old_pos = black_locations[selection]
                            print_board_state()
                            
                            # Handle capture
                            if click_coords in white_locations:
                                idx = white_locations.index(click_coords)
                                if white_pieces[idx] != 'king':
                                    captured_pieces_black.append(white_pieces[idx])
                                    white_pieces.pop(idx)
                                    white_locations.pop(idx)
                            
                            # Handle castling
                            if black_pieces[selection] == 'king':
                                if click_coords == (6, 7) and old_pos == (4, 7):  # Kingside
                                    if (6, 7) in valid_moves:
                                        rook_index = black_locations.index((7, 7))
                                        black_locations[rook_index] = (5, 7)
                                elif click_coords == (2, 7) and old_pos == (4, 7):  # Queenside
                                    if (2, 7) in valid_moves:
                                        rook_index = black_locations.index((0, 7))
                                        black_locations[rook_index] = (3, 7)
                            
                            # Make the move
                            black_locations[selection] = click_coords
                            
                            # Update 50-move rule
                            update_half_move_clock(
                                click_coords in white_locations,
                                black_pieces[selection] == 'pawn'
                            )
                            if is_fifty_move_draw():
                                game_over = True
                                winner = 'draw'
                            
                            # Update castling rights
                            chess_rules.update_castling_rights(
                                black_pieces[selection], old_pos, 'black')
                            
                            # Handle promotion
                            chess_rules.pawn_promotion(
                                black_pieces, black_locations, 'black')
                            
                            # En passant capture
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
                            
                            # Set en passant flag
                            if black_pieces[selection] == 'pawn' and abs(click_coords[1] - old_pos[1]) == 2:
                                en_passant_possible = (click_coords[0], click_coords[1] + 1)
                            else:
                                en_passant_possible = None
                            
                            last_move = (old_pos, click_coords)
                            
                            # Update options
                            black_options = check_options(black_pieces, black_locations, 'black', last_move)
                            white_options = check_options(white_pieces, white_locations, 'white', last_move)
                            
                            # Check for repetition
                            if record_position(
                                    white_pieces, white_locations,
                                    black_pieces, black_locations,
                                    'black', en_passant_possible
                                ) >= 3:
                                game_over = True
                                winner = 'draw'
                            
                            # Switch to white's turn
                            turn_step = 0
                            selection = 100
                            valid_moves = []
                            #chess_rules.reset_turn_timer()
                            
                            # Check for stalemate/checkmate
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