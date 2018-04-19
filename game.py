
ship_dict = {
    'destroyer': 3,
    'battleship': 5
}


class Ship():
    def __init__(self, title, length):
        self.orientation = 'nesw'
        self.position = (0, 0)
        self.map_location = []
        self.title = title
        self.length = length
        self.damage = ['0'] * self.length

    def place_ship(self, position, orientation):
        pass


class Player():
    def __init__(self, player_id):
        self.guesses = []  # Misses/Hits
        self.id = player_id
        self.ships = []
        for ship_name, ship_length in ship_dict.items():
            self.ships.append(Ship(ship_name, ship_length))

    def position_orders(self):
        for ship in self.ships:
            ship.position = input('Enter a position for {} e.g. (row, col):'.format(ship.title))

    def guess(self):
        new_guess =         input('Enter a position for {} e.g. (row, col):'.format(ship.title)))


    def sink_ship(self, title):
        del self.ships[title]
        print('Player {}''s {} has been sunk!')

    def ship_inventory(self):
        if self.ships = []:
            return 'Player {} has lost the game!'.format(self.id)
        else:
            return 'ongoing'


class Game():
    def __init__(self, map_size, player_count):
        self.players = []
        self.map = [['0']*map_size]*map_size
        for player_id in range(1, player_count+1):
            self.players.append(Player(player_id))
        self.state = 'ongoing'

    def draw_map(self):
        print('Map Current State')
        for row in self.map:
            print(' '.join(row))


def game_play():
    # Start a new game
    new_game = Game(map_size=8, player_count=2)

    # Setup the Map
    for player in new_game.players:
        print('Player {}, place your ships'.format(player.id))
        player.position_orders()

    while new_game.state == 'ongoing':
        # Set the player's turn
        for player in new_game.players:

            # Draw the map & ship
            new_game.draw_map()

            # Draw the guesses/hits


            # Prompt the user for a guess
            player.guess()

            # Evaluate if guess
                # Sunk a ship
                # Won the game

            # Check if the player has remaining ships
            new_game.state = player.ship_inventory()

game_play()