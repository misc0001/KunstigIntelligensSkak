def pos_to_notation(pos):
    files = 'abcdefgh'
    return files[pos[0]] + str(pos[1] + 1)

def notation_to_pos(notation):
    files = 'abcdefgh'
    return (files.index(notation[0]), int(notation[1]) - 1)

def get_game_string():
    game_data = []
    for i in range(len(white_pieces)):
        code = 'w' + white_pieces[i][0] + ':' + pos_to_notation(white_locations[i])
        game_data.append(code)
    for i in range(len(black_pieces)):
        code = 'b' + black_pieces[i][0] + ':' + pos_to_notation(black_locations[i])
        game_data.append(code)
    return ','.join(game_data)

def load_game_from_string(save_str):
    global white_pieces, white_locations, black_pieces, black_locations
    white_pieces = []
    white_locations = []
    black_pieces = []
    black_locations = []
    
    piece_codes = {'p': 'pawn', 'r': 'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king'}

    entries = save_str.split(',')
    for entry in entries:
        if ':' not in entry:
            continue
        side_piece, notation = entry.split(':')
        color = side_piece[0]
        code = side_piece[1]
        pos = notation_to_pos(notation)

        if color == 'w':
            white_pieces.append(piece_codes[code])
            white_locations.append(pos)
        else:
            black_pieces.append(piece_codes[code])
            black_locations.append(pos)

if event.key == pygame.K_RETURN:
    print("Load string:", input_text)
    load_game_from_string(input_text)
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    menu_state = False
    input_active = False

if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_s:
        print("Save string:", get_game_string())


while run:
    timer.tick(fps)
    screen.fill('light gray')

    if menu_state:
        draw_menu()
        if input_active:
            draw_text_input(input_text)
    else:
        draw_board()
        draw_pieces()
        if selection != 100:
            valid_moves = check_valid_moves()
            draw_valid(valid_moves)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if menu_state:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_n:
                    menu_state = False  # Start nyt spil
                if event.key == pygame.K_l:
                    input_active = True
                if input_active:
                    if event.key == pygame.K_RETURN:
                        print("Load string:", input_text)
                        # Her skal du implementere logik til at parse og loade spillet
                        menu_state = False
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode
            continue  # Gå ikke videre til resten af spillet hvis i menuen

        # Eksisterende event-håndtering for spillet (som du allerede har)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            # ... din eksisterende klik-logik
            pass

    pygame.display.flip()

pygame.quit()



