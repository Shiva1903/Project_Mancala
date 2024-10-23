import time
import random

class Palankuzhi:
    def __init__(self):
        self.board = [
            [5, 5, 5, 5, 5, 5, 5],  # Player 1's pits (row 0)
            [5, 5, 5, 5, 5, 5, 5]   # Player 2's pits (row 1)
        ]
        self.player_coins = [0, 0]  # Stores for Player 1 and Player 2
        self.player1_coin_on_board = 35
        self.player2_coin_on_board = 35

    def check_for_win(self):
        coin_on_side1 = sum(self.board[0])
        coin_on_side2 = sum(self.board[1])

        if coin_on_side1 == 0 or coin_on_side2 == 0:
            self.player_coins[0] += coin_on_side1
            self.player_coins[1] += coin_on_side2
            winner = None
            if self.player_coins[0] > self.player_coins[1]:
                print("Player 1 Wins!!!")
                winner = 0
            elif self.player_coins[0] < self.player_coins[1]:
                print("Player 2 Wins!!!")
                winner = 1
            else:
                print("It's a Draw!!!")

            print("Final Stats:")
            self.print_stats()
            return True, winner

        return False, -1

    def valid_move(self, player_id, index):
        if self.board[player_id][index] == 0:
            return False
        return True

    def print_board(self):
        print(f"P1 --> {self.board[0]}")
        print(f"P2 --> {self.board[1]}")

    def print_stats(self):
        print(f"Player 1's Store: {self.player_coins[0]}")
        print(f"Player 2's Store: {self.player_coins[1]}\n")

    def check_for_pasu(self):
        for player_id in [0, 1]:
            while 4 in self.board[player_id]:
                index = self.board[player_id].index(4)
                self.player_coins[player_id] += 4
                self.board[player_id][index] = 0

    def next_index(self, row, col):
        if row == 1:
            col += 1
            if col > 6:
                row = 0
                col = 6
        elif row == 0:
            col -= 1
            if col < 0:
                row = 1
                col = 0
        return row, col

    def move_coins(self, player_id, row, col):
        current_coins = self.board[row][col]
        self.board[row][col] = 0

        while current_coins > 0:
            row, col = self.next_index(row, col)
            self.board[row][col] += 1
            current_coins -= 1
            self.check_for_pasu()

        row, col = self.next_index(row, col)
        if self.board[row][col] > 0:
            return self.move_coins(player_id, row, col)
        elif self.board[row][col] == 0:
            row, col = self.next_index(row, col)
            self.player_coins[player_id] += self.board[row][col]
            self.board[row][col] = 0
            return

def ai_move(game, player_id):
    """
    Simple AI that selects the pit with the maximum stones.
    If no valid moves are available, it returns None.
    """
    valid_moves = [i for i in range(7) if game.valid_move(player_id, i)]
    if not valid_moves:
        return None
    # Simple heuristic: choose the pit with the most stones
    best_move = max(valid_moves, key=lambda x: game.board[player_id][x])
    return best_move

def play_game():
    game = Palankuzhi()
    game.print_board()
    game.print_stats()
    human_player = int(input("Choose your side (1 or 2): ")) - 1
    ai_player = 1 - human_player
    current_player = 0  # Player 1 starts the game

    while True:
        print(f"Current Player: {'You' if current_player == human_player else 'AI'}")
        if current_player == human_player:
            try:
                index = int(input("Select a pit (1 - 7): ")) - 1
                if index < 0 or index > 6:
                    print("Invalid pit number. Please select a pit between 1 and 7.")
                    continue
                if not game.valid_move(current_player, index):
                    print("Selected pit is empty. Choose a different pit.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")
                continue
        else:
            # AI's turn
            index = ai_move(game, current_player)
            if index is None:
                print("AI has no valid moves. Passing turn.")
                current_player = human_player
                continue
            print(f"AI selects pit {index + 1}")

        game.move_coins(current_player, current_player, index)
        game.print_board()
        game.print_stats()

        game_over, winner = game.check_for_win()
        if game_over:
            break

        # Switch turns
        current_player = 1 - current_player

if __name__ == '__main__':
    play_game()
