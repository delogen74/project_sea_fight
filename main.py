import random

# Преобразование координат
def to_coord(letter):
    return ord(letter.upper()) - ord('A') + 1

def to_letter(number):
    return chr(number + ord('A') - 1)

# Определение класса корабля
class Ship:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.hits = []

    def hit(self, shot):
        if shot in self.coordinates:
            self.hits.append(shot)
            return True
        return False

    def is_sunk(self):
        return set(self.hits) == set(self.coordinates)

# Определение класса игровой доски
class Board:
    def __init__(self, size=6):
        self.size = size
        self.grid = [[' ' for _ in range(size)] for _ in range(size)]
        self.ships = []
        self.shots = []

    def add_ship(self, ship):
        self.ships.append(ship)
        for x, y in ship.coordinates:
            self.grid[y-1][x-1] = 'S'

    def shoot_at(self, coord):
        coord = (to_coord(coord[0]), int(coord[1:])) # Преобразование например "A1" в (1,1)
        if coord in self.shots:
            raise ValueError("Вы уже стреляли сюда.")
        self.shots.append(coord)
        for ship in self.ships:
            if ship.hit(coord):
                if ship.is_sunk():
                    return "Уничтожен!"
                return "Попал!"
        return "Мимо!"

    def all_sunk(self):
        return all(ship.is_sunk() for ship in self.ships)

    def display(self, show_ships=False):
        print("  | " + " | ".join(to_letter(i) for i in range(1, self.size + 1)) + " |")
        for i in range(self.size):
            row = str(i+1) + " | "
            for j in range(self.size):
                cell = self.grid[i][j]
                if (j+1, i+1) in self.shots:
                    if any((j+1, i+1) in ship.coordinates for ship in self.ships):
                        row += "X | "
                    else:
                        row += "O | "
                elif show_ships and any((j+1, i+1) in ship.coordinates for ship in self.ships):
                    row += "■ | "
                else:
                    row += "  | "
            print(row)

# Определение класса игры
class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.setup_boards()

    def setup_boards(self):
        for board in [self.player_board, self.computer_board]:
            self.place_ships_on_board(board)

    def place_ships_on_board(self, board):
        ships_sizes = [3, 2, 2, 1, 1, 1, 1]  # Размеры кораблей
        for size in ships_sizes:
            while True:
                ship = self.create_ship(board, size)
                if ship:
                    board.add_ship(ship)
                    break

    def create_ship(self, board, size):
        max_attempts = 100
        for _ in range(max_attempts):
            x = random.randint(1, board.size)
            y = random.randint(1, board.size)
            orientation = random.choice(['horizontal', 'vertical'])
            ship_coords = self.get_ship_coordinates(x, y, size, orientation, board.size)
            if ship_coords and self.is_valid_position(board, ship_coords):
                return Ship(ship_coords)
        return None

    def get_ship_coordinates(self, x, y, size, orientation, board_size):
        ship_coords = []
        if orientation == 'horizontal' and x + size - 1 <= board_size:
            ship_coords = [(x + i, y) for i in range(size)]
        elif orientation == 'vertical' and y + size - 1 <= board_size:
            ship_coords = [(x, y + i) for i in range(size)]
        return ship_coords

    def is_valid_position(self, board, ship_coords):
        for x, y in ship_coords:
            if board.grid[y - 1][x - 1] != ' ':
                return False
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 1 <= nx <= board.size and 1 <= ny <= board.size:
                        if board.grid[ny - 1][nx - 1] == 'S':
                            return False
        return True

    def print_boards(self):
        print("Ваша доска:")
        self.player_board.display(show_ships=True)
        print("\nДоска компьютера:")
        self.computer_board.display()

    def play(self):
        input("Приветствую тебя в водах Карибского моря! Готов к морским сражениям? Нажмите Enter...")
        input("О нет! Пираты напали на вас в тумане! Нажмите Enter...")
        self.print_boards()
        while not self.computer_board.all_sunk() and not self.player_board.all_sunk():
            self.player_turn()
            if self.computer_board.all_sunk():
                break
            self.computer_turn()
            self.print_boards()

        if self.computer_board.all_sunk():
            print("Поздравляем! Вы уничтожили всю армаду пиратов!")
        else:
            print("Увы, пираты победили. Попробуйте еще раз!")

    def player_turn(self):
        while True:
            player_input = input("Произведите выстрел (например, A1): ").strip().upper()
            if len(player_input) < 2 or not player_input[0].isalpha() or not player_input[1:].isdigit():
                print("Неправильный формат. Введите букву и число, например 'A1'.")
                continue
            x, y = player_input[0], player_input[1:]
            if to_coord(x) > self.computer_board.size or int(y) > self.computer_board.size:
                print(f"Неправильные координаты. Введите координаты в пределах {self.computer_board.size}x{self.computer_board.size}.")
                continue
            try:
                result = self.computer_board.shoot_at(player_input)
                print(result)
                break
            except ValueError as e:
                print(e)

    def computer_turn(self):
        while True:
            x = random.randint(1, self.computer_board.size)
            y = random.randint(1, self.computer_board.size)
            try:
                shot = to_letter(x) + str(y)
                result = self.player_board.shoot_at(shot)
                print(f"Компьютер стрелял в {shot} и {result}")
                break
            except ValueError:
                continue

if __name__ == "__main__":
    game = Game()
    game.play()
