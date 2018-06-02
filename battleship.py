from copy import deepcopy

ship_dict = {
    'Carrier':5,
    'Battleship':4,
    'Cruiser':3,
    'Submarine':3,
    'Destroyer':2}

ship_dict = {
    'Tugboat': 2}

def cartesian_to_alphanum(numeric_tuple):
    row, column = numeric_tuple
    row = chr(row+65)
    column = str(column + 1)
    return row+column

def alphanum_to_cartesian(string_pair):
    row = ord(string_pair[0]) - 65
    column = int(string_pair[1:]) - 1
    return (row, column)

class Ship():
    def __init__(self, title, length):
        self.orientation = ''  # 'ns' or 'ew'
        self.position = (0, 0)
        self.map_location = []
        self.title = title
        self.length = length
        self.health = length + 0


class Player():
    def __init__(self, player_id, default_fleet):
        self.id = player_id
        self.ships = []
        for ship_name, ship_length in default_fleet.items():
            self.ships.append(Ship(ship_name, ship_length))

    def show(self):
        print('\nPlayer {}'.format(self.id))
        for ship in self.ships:
            print('\t{} {} {}'.format(ship.title, ship.orientation, ship.position))


class Game():
    def __init__(self, map_size, player_count, default_fleet):
        self.map_size = map_size
        self.maps = {1: [['[ ]' for x in range(map_size)] for x in range(map_size)], 2: [['[ ]' for x in range(map_size)] for x in range(map_size)]}
        self.mapz = Map(10)
        self.players = dict()
        for player_id in range(1, player_count+1):
            self.players[player_id] = Player(player_id, default_fleet)
        self.taken = []

    def draw_map(self, in_game = False, map_id = None):
        for i, map in self.maps.items():
            if map_id == None or map_id == i:
                print('\nMap {}'.format(i))
                column_labels = [str(x) for x in range(1, 1 + self.map_size)]
                print('   '+'   '.join(column_labels))
                row_labels = [chr(x) for x in range(ord('A'), ord('A')+self.map_size)]
                row_labels = iter(row_labels)
                for row in map:
                    if in_game:
                        row_to_print = [x.replace('[t]', '[ ]') for x in row]
                    else:
                        row_to_print = row
                    print(' '.join([next(row_labels)]+row_to_print))

class Map():
    def __init__(self, size):
        self.size = size
        self.locations = [(x, y) for x in range(size) for y in range(size)]

def play():
    # Start a new game
    game = Game(map_size=10, player_count=2, default_fleet=ship_dict)

    # Setup the map
    for player in game.players.values():
        for ship in player.ships:
            # Choose orientation
            raw_input = ''
            game.draw_map(map_id=player.id)
            orientations = ['NS', 'EW']
            while raw_input not in ['NS', 'ns', 'Ns', 'EW', 'ew', 'Ew', '1', '2']:
                print('Please choose the orientation for your {}'.format(ship.title))
                for i, option in enumerate(orientations):
                    print('{}) {}'.format(i+1, option))
                raw_input = input('>>> ')
            if raw_input in ['1', '2']:
                ship.orientation = orientations[int(raw_input)-1]
            else:
                ship.orientation = raw_input.upper()
            # Choose position
            raw_input = ''

            while raw_input == '':
                print('Please choose the position for your {}; Use format <row><column> e.g. A4'.format(ship.title))
                raw_input = input('>>> ')
                row, column = alphanum_to_cartesian(raw_input)
                location = [(row + x, column) for x in range(ship.length)] if ship.orientation == 'NS' else [(row, column + x) for x in range(ship.length)]
                for map_tile in location:
                    if map_tile in game.taken:
                        print('Map tile {} is already occupied\n'.format(map_tile))
                        continue
                if ship.orientation == 'NS':
                    if row < 0 or row > (game.map_size - ship.length + 1):
                        print('Out of Bounds...\n')
                        continue
                    if column < 0 or column > game.map_size:
                        print('Out of Bounds...\n')
                        continue
                elif ship.orientation == 'EW':
                    if row < 0 or row > game.map_size:
                        print('Out of Bounds...\n')
                        continue
                    if column < 0 or column > (game.map_size - ship.length + 1):
                        print("Your {} can't anchor here, the position includes waters outside of your controlled area.\n".format(ship.title))
                        continue
                print('{} will be placed between {} and {}'.format(ship.title, cartesian_to_alphanum(location[0]), cartesian_to_alphanum(location[-1])))
                ship.position = (row, column)
                ship.map_location = location
                for row, column in ship.map_location:
                    game.maps[player.id][row][column] = '[t]'
                game.taken.extend(location)
                game.draw_map(map_id=player.id)
                input('Is this where you want your ship?')

            player.show()
            game.draw_map(map_id=player.id)

    # Game main loop
    print('The War has begun!')
    while True:
        # Set the player's turn
        for player in game.players.values():
            opponent_id = 1 + (player.id % 2)

            # Draw the map, guesses, and hits
            game.draw_map(in_game=True)

            # Prompt the user for a guess
            raw_input = ''
            while raw_input == '':
                print('Player {}, Please choose the location of your strike! Use format <row><column> e.g. A4'.format(player.id))
                raw_input = input('>>> ')
                row, column = alphanum_to_cartesian(raw_input)
                if row < 0 or row > game.map_size:
                    print('You must choose a position within strike range.')
                elif game.maps[opponent_id][row][column] in ['[M]', '[H]']:
                    print('You have previously launched a strike at this position.')
                elif game.maps[opponent_id][row][column] == '[ ]':
                    print('Your strike missed the enemy...')
                    game.maps[opponent_id][row][column] = '[M]'
                else:
                    print('Direct Hit!')
                    game.maps[opponent_id][row][column] = '[H]'
                    for ship in game.players[opponent_id].ships:
                        if (row, column) in ship.map_location:
                            ship.health -= 1
                            if ship.health == 0:
                                print("You sunk the opposition's {}".format(ship.title))
                                game.players[opponent_id].ships.remove(ship)
                                if len(game.players[opponent_id].ships) == 0:
                                    print('Player {}, You have defeated the enemy!'.format(player.id))
                                    exit('Player {} wins the game!'.format(player.id))


play()