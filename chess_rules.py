import time
import pygame
from copy import deepcopy

# Timer settings
turn_time_limit = 15  # seconds
turn_start_time = time.time()

# Flags to track castling rights
white_king_moved = False
white_rook_kingside_moved = False
white_rook_queenside_moved = False

black_king_moved = False
black_rook_kingside_moved = False
black_rook_queenside_moved = False

# Track en passant possibilities
en_passant_possible = None  # Will store (x, y) location where en passant can occur

half_move_clock = 0

def update_half_move_clock(is_capture: bool, is_pawn_move: bool):
    """
    Call this once per half-move.
    - If the move was a capture or a pawn move, reset the counter.
    - Otherwise, increment it by 1.
    """
    global half_move_clock
    if is_capture or is_pawn_move:
        half_move_clock = 0
    else:
        half_move_clock += 1

def is_fifty_move_draw() -> bool:
    """
    Returns True once 100 half-moves (50 full moves) have passed
    without any pawn move or capture.
    """
    return half_move_clock >= 100


def check_king(position, color, white_locations, black_locations, white_pieces, black_pieces, pieces):
    moves_list = []  # Starter med tom liste, og så tilføjer gyldige træk
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1), (1, 0),  (1, 1)]

    # pick friendly vs. enemy lists
    if color == 'white':
        friendly_locs, enemy_locs = white_locations, black_locations
        friendly_pcs, enemy_pcs = white_pieces, black_pieces
    else:
        friendly_locs, enemy_locs = black_locations, white_locations
        friendly_pcs, enemy_pcs = black_pieces, white_pieces

    king_idx = pieces.index('king')

    for dx, dy in directions:
        new_pos = (position[0] + dx, position[1] + dy)
        if not (0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7):
            continue
        if new_pos in friendly_locs:
            continue

        # ── simulate the move & any capture
        sim_white_locs = white_locations.copy()
        sim_black_locs = black_locations.copy()
        sim_white_pcs  = white_pieces.copy()
        sim_black_pcs  = black_pieces.copy()

        if color == 'white':
            sim_white_locs[king_idx] = new_pos
            # remove captured black piece if any
            if new_pos in sim_black_locs:
                i = sim_black_locs.index(new_pos)
                sim_black_locs.pop(i)
                sim_black_pcs.pop(i)
        else:
            sim_black_locs[king_idx] = new_pos
            if new_pos in sim_white_locs:
                i = sim_white_locs.index(new_pos)
                sim_white_locs.pop(i)
                sim_white_pcs.pop(i)

        # ── now only allow if the king is NOT under attack on that simulated board
        if not under_attack(new_pos, color,
                            sim_white_locs, sim_black_locs,
                            sim_white_pcs, sim_black_pcs):
            moves_list.append(new_pos)

    # include castling as before
    moves_list += castling_move(pieces,
                            white_locations if color == 'white' else black_locations,
                            color,
                            white_locations, black_locations,
                            white_pieces, black_pieces)

    return moves_list




def under_attack(square, king_color, white_locations, black_locations, white_pieces, black_pieces):
    """Check if a square is under attack by any enemy piece"""
    # Determine enemy pieces and locations
    if king_color == 'white':
        enemy_color = 'black'
        enemy_pieces = black_pieces  # This needs to be passed properly in actual code
        enemy_locations = black_locations
        friendly_locations = white_locations
    else:
        enemy_color = 'white'
        enemy_pieces = white_pieces  # This needs to be passed properly in actual code
        enemy_locations = white_locations
        friendly_locations = black_locations
    
    # Check for attacks from each enemy piece
    for i in range(len(enemy_pieces)):
        piece = enemy_pieces[i]
        pos = enemy_locations[i]
        
        # Check appropriate piece movement
        if piece == 'pawn':
            # Pawns attack diagonally
            if enemy_color == 'white':
                attacks = [(pos[0]-1, pos[1]+1), (pos[0]+1, pos[1]+1)]
            else:
                attacks = [(pos[0]-1, pos[1]-1), (pos[0]+1, pos[1]-1)]
            if square in attacks:
                return True
                
        elif piece == 'knight':
            attacks = check_knight(pos, enemy_color, white_locations, black_locations)
            if square in attacks:
                return True
                
        elif piece == 'bishop':
            attacks = check_bishop(pos, enemy_color, white_locations, black_locations)
            if square in attacks:
                return True
                
        elif piece == 'rook':
            attacks = check_rook(pos, enemy_color, white_locations, black_locations)
            if square in attacks:
                return True
                
        elif piece == 'queen':
            attacks = check_queen(pos, enemy_color, white_locations, black_locations)
            if square in attacks:
                return True
                
        elif piece == 'king':
            # King attacks adjacent squares
            directions = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1),          (0, 1),
                        (1, -1), (1, 0),  (1, 1)]
            king_attacks = []
            for d in directions:
                new_pos = (pos[0] + d[0], pos[1] + d[1])
                if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    king_attacks.append(new_pos)
            if square in king_attacks:
                return True
    
    return False


def check_queen(position, color, white_locations, black_locations):
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


def check_bishop(position, color, white_locations, black_locations):
    moves_list = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    if color == 'white':
        friendly_locations = white_locations
        enemy_locations = black_locations
    else:
        friendly_locations = black_locations
        enemy_locations = white_locations

    for d in directions:
        for i in range(1, 8):
            new_pos = (position[0] + d[0] * i, position[1] + d[1] * i)
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                if new_pos in friendly_locations:
                    break
                moves_list.append(new_pos)
                if new_pos in enemy_locations:
                    break
       
    return moves_list

def check_rook(position, color, white_locations, black_locations):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def check_pawn(position, color, white_locations, black_locations, last_move=None):
    # Liste over mulige træk for bonden
    global en_passant_target
    moves_list = []
    x, y = position

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

        # En passant for white
        if y == 4 and last_move:  # White pawn on 5th rank
            last_from, last_to = last_move
            # Check if last move was a black pawn double move
            if last_from[1] == 6 and last_to[1] == 4 and abs(last_to[0] - x) == 1:
                # Check if the piece is next to us
                if last_to[0] == x + 1 or last_to[0] == x - 1:
                    moves_list.append((last_to[0], y + 1))  # Capture diagonally

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

    # En passant for black
        if y == 3 and last_move:  # Black pawn on 4th rank
            last_from, last_to = last_move
            # Check if last move was a white pawn double move
            if last_from[1] == 1 and last_to[1] == 3 and abs(last_to[0] - x) == 1:
                # Check if the piece is next to us
                if last_to[0] == x + 1 or last_to[0] == x - 1:
                    moves_list.append((last_to[0], y - 1))  # Capture diagonally
    return moves_list


def check_knight(position, color, white_locations, black_locations):
    moves_list = []
    directions = [(-2, -1), (-1, -2), (1, -2), (2, -1),
    (2, 1), (1, 2), (-1, 2), (-2, 1)]

    if color == 'white': # Identificerer hvilke brækker der er på ens holkd og hvilke der er mod en
        friendly_locations = white_locations
    else:
        friendly_locations = black_locations

    for d in directions:
        new_pos = (position[0] + d[0], position[1] + d[1])
        if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
            # Tjek at der ikke står en venlig brik
            if new_pos not in friendly_locations:
                moves_list.append(new_pos)

    return moves_list

def reset_turn_timer():
    global turn_start_time
    turn_start_time = time.time()

def turn_timer(turn_step):
    global turn_start_time
    elapsed = time.time() - turn_start_time
    time_left = max(0, int(turn_time_limit - elapsed))
    
    if elapsed >= turn_time_limit:
        if turn_step == 1:
            return 2, 100, [], time_left
        elif turn_step == 3:
            return 0, 100, [], time_left
    return turn_step, None, None, time_left


def pawn_promotion(pieces, locations, color):
    # Find all pawns on the last rank
    promotion_index = []
    for i in range(len(pieces)):
        if pieces[i] == 'pawn':
            if color == 'white' and locations[i][1] == 7:
                promotion_index.append(i)
            elif color == 'black' and locations[i][1] == 0:
                promotion_index.append(i)

    for idx in promotion_index:
        choice = choose_promotion()
        pieces[idx] = choice

def choose_promotion():
    choosing = True
    clock = pygame.time.Clock()
    font = pygame.font.Font('freesansbold.ttf', 30)
    while choosing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return 'queen'
                elif event.key == pygame.K_r:
                    return 'rook'
                elif event.key == pygame.K_b:
                    return 'bishop'
                elif event.key == pygame.K_k:
                    return 'knight'

        pygame.display.get_surface().fill((0, 0, 0))
        text = font.render('Promote to (Q)ueen, (R)ook, (B)ishop, (K)night', True, (255, 255, 255))
        pygame.display.get_surface().blit(text, (100, 400))
        pygame.display.update()
        clock.tick(60)

def valid_moves(piece_index, move_list, own_pieces, own_locations, enemy_pieces, enemy_locations, color, draw_check_fn):
    safe_moves = []

    for move in move_list:
        # Deep copy positions
        new_own_locations = own_locations[:]
        new_enemy_pieces = enemy_pieces[:]
        new_enemy_locations = enemy_locations[:]

        old_pos = new_own_locations[piece_index]

        # Simulate the move
        new_own_locations[piece_index] = move
        if move in enemy_locations:
            idx = enemy_locations.index(move)
            new_enemy_pieces.pop(idx)
            new_enemy_locations.pop(idx)

        if color == 'white':
            still_in_check = draw_check_fn(own_pieces, new_own_locations, new_enemy_pieces, new_enemy_locations, 'white')
        else:
            still_in_check = draw_check_fn(own_pieces, new_own_locations, new_enemy_pieces, new_enemy_locations, 'black')

        if not still_in_check:
            safe_moves.append(move)

    return safe_moves




def update_castling_rights(piece, start_pos, color):
    global white_king_moved, white_rook_kingside_moved, white_rook_queenside_moved
    global black_king_moved, black_rook_kingside_moved, black_rook_queenside_moved

    if piece == 'king':
        if color == 'white':
            white_king_moved = True
        else:
            black_king_moved = True
    if piece == 'rook':
        if color == 'white':
            if start_pos == (7, 0):
                white_rook_kingside_moved = True
            if start_pos == (0, 0):
                white_rook_queenside_moved = True
        else:
            if start_pos == (7, 7):
                black_rook_kingside_moved = True
            if start_pos == (0, 7):
                black_rook_queenside_moved = True

def check_stalemate(pieces, locations, enemy_pieces, enemy_locations, color, check_func, white_locations, black_locations, white_pieces, black_pieces):
    for i in range(len(pieces)):
        piece = pieces[i]
        pos = locations[i]

        # Get all possible moves for this piece
        if piece == 'pawn':
            all_moves = check_pawn(pos, color, white_locations, black_locations, None)
        elif piece == 'rook':
            all_moves = check_rook(pos, color, white_locations, black_locations)
        elif piece == 'bishop':
            all_moves = check_bishop(pos, color, white_locations, black_locations)
        elif piece == 'knight':
            all_moves = check_knight(pos, color, white_locations, black_locations)
        elif piece == 'queen':
            all_moves = check_queen(pos, color, white_locations, black_locations)
        elif piece == 'king':
            all_moves = check_king(pos, color, white_locations, black_locations, white_pieces, black_pieces, pieces)
        else:
            continue

        # Filter illegal moves (ones that leave the king in check)
        safe_moves = valid_moves(i, all_moves, pieces, locations, enemy_pieces, enemy_locations, color, check_func)
        if safe_moves:
            return False  # Not stalemate: at least one legal move

    return not check_func(pieces, locations, enemy_pieces, enemy_locations, color)  # No moves AND not in check

def check_checkmate(pieces, locations,
                    enemy_pieces, enemy_locations,
                    color, check_func,
                    white_locations, black_locations,
                    white_pieces, black_pieces):
    # not even in check → not mate
    if not check_func(pieces, locations,
                      enemy_pieces, enemy_locations,
                      color):
        return False

    # try *every* friendly piece
    for i, piece in enumerate(pieces):
        pos = locations[i]

        # 1) generate its pseudolegal moves
        if piece == 'pawn':
            moves = check_pawn(pos, color,
                               white_locations, black_locations,
                               None)
        elif piece == 'rook':
            moves = check_rook(pos, color,
                               white_locations, black_locations)
        elif piece == 'knight':
            moves = check_knight(pos, color,
                                 white_locations, black_locations)
        elif piece == 'bishop':
            moves = check_bishop(pos, color,
                                 white_locations, black_locations)
        elif piece == 'queen':
            moves = check_queen(pos, color,
                                white_locations, black_locations)
        elif piece == 'king':
            moves = check_king(pos, color,
                               white_locations, black_locations,
                               white_pieces, black_pieces,
                               pieces)
        else:
            continue

        # 2) filter with your existing safe-move test
        safe = valid_moves(i, moves,
                          pieces, locations,
                          enemy_pieces, enemy_locations,
                          color, check_func)
        if safe:
            return False  # found at least one legal response

    # no legal response and in check → checkmate
    return True


def castling_move(pieces, locations, color, white_locations, black_locations, white_pieces, black_pieces):
    moves = []

    if color == 'white' and not white_king_moved and (4, 0) in white_locations:
        # Kingside
        if not white_rook_kingside_moved and (7, 0) in white_locations:
            if all((x, 0) not in white_locations + black_locations for x in [5, 6]):
                if not any(under_attack((x, 0), 'white', white_locations, black_locations, white_pieces, black_pieces)
                           for x in [4, 5, 6]):
                    moves.append((6, 0))
        # Queenside
        if not white_rook_queenside_moved and (0, 0) in white_locations:
            if all((x, 0) not in white_locations + black_locations for x in [1, 2, 3]):
                if not any(under_attack((x, 0), 'white', white_locations, black_locations, white_pieces, black_pieces)
                           for x in [2, 3, 4]):
                    moves.append((2, 0))

    if color == 'black' and not black_king_moved and (4, 7) in black_locations:
        # Kingside
        if not black_rook_kingside_moved and (7, 7) in black_locations:
            if all((x, 7) not in white_locations + black_locations for x in [5, 6]):
                if not any(under_attack((x, 7), 'black', white_locations, black_locations, white_pieces, black_pieces)
                           for x in [4, 5, 6]):
                    moves.append((6, 7))
        # Queenside
        if not black_rook_queenside_moved and (0, 7) in black_locations:
            if all((x, 7) not in white_locations + black_locations for x in [1, 2, 3]):
                if not any(under_attack((x, 7), 'black', white_locations, black_locations, white_pieces, black_pieces)
                           for x in [2, 3, 4]):
                    moves.append((2, 7))

    return moves



def en_passant(color, last_move, white_pieces, white_locations, black_pieces, black_locations):
    moves = []
    if color == 'white':
        enemy_pawns = [(pos, idx) for idx, (piece, pos) in enumerate(zip(black_pieces, black_locations)) if piece == 'pawn']
    else:
        enemy_pawns = [(pos, idx) for idx, (piece, pos) in enumerate(zip(white_pieces, white_locations)) if piece == 'pawn']

    if last_move:
        last_from, last_to = last_move
        if abs(last_from[1] - last_to[1]) == 2:  # double move
            if color == 'white' and last_to[1] == 4:
                moves.append((last_to[0], 5))
            if color == 'black' and last_to[1] == 3:
                moves.append((last_to[0], 2))
    return moves

def en_passant_capture(old_pos, new_pos, color, white_pieces, white_locations, black_pieces, black_locations):
    """Handle en passant capture - returns True if a capture was made"""
    captured = False
    
    if color == 'white' and old_pos[1] == 4 and new_pos[1] == 5:
        # Check if this is a diagonal move (potential en passant)
        if abs(new_pos[0] - old_pos[0]) == 1:
            # Look for a black pawn at the same column but one row below
            capture_pos = (new_pos[0], new_pos[1] - 1)
            if capture_pos in black_locations:
                idx = black_locations.index(capture_pos)
                if black_pieces[idx] == 'pawn':
                    # Remove the captured pawn
                    captured_piece = black_pieces.pop(idx)
                    black_locations.pop(idx)
                    captured = True
    
    elif color == 'black' and old_pos[1] == 3 and new_pos[1] == 2:
        # Check if this is a diagonal move (potential en passant)
        if abs(new_pos[0] - old_pos[0]) == 1:
            # Look for a white pawn at the same column but one row above
            capture_pos = (new_pos[0], new_pos[1] + 1)
            if capture_pos in white_locations:
                idx = white_locations.index(capture_pos)
                if white_pieces[idx] == 'pawn':
                    # Remove the captured pawn
                    captured_piece = white_pieces.pop(idx)
                    white_locations.pop(idx)
                    captured = True
    
    return captured

# --- threefold-repetition rule ---

# maps each unique position key to how many times it's occurred
position_counts = {}

def record_position(white_pieces, white_locations,
                    black_pieces, black_locations,
                    turn, en_passant):
    """
    Must be called once, immediately after each move (after all captures,
    promotions, castling rights, en-passant flag, etc. have been applied).
    Returns the count for this position (>=1).
    """
    global position_counts

    # build a hashable key: side to move + piece/type placements +
    # castling-rights flags from this module + en_passant square
    key = (
        turn,
        tuple(zip(white_pieces, white_locations)),
        tuple(zip(black_pieces, black_locations)),
        white_king_moved, white_rook_kingside_moved, white_rook_queenside_moved,
        black_king_moved, black_rook_kingside_moved, black_rook_queenside_moved,
        en_passant
    )

    position_counts[key] = position_counts.get(key, 0) + 1
    return position_counts[key]

def is_threefold_repetition_draw() -> bool:
    """
    True if any position in the game has now occurred 3+ times.
    """
    return any(count >= 3 for count in position_counts.values())
