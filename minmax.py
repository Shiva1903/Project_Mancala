import copy

class Palankuzhi:
    def __init__(self):
        self.board = [
            [5, 5, 5, 5, 5, 5, 5],  # Player 1's pits (row 0)
            [5, 5, 5, 5, 5, 5, 5]   # Player 2's pits (row 1)
        ]
        self.player_coins = [0, 0]  # Stores for Player 1 and Player 2

    def check_for_win(self):
        coin_on_side1 = sum(self.board[0])
        coin_on_side2 = sum(self.board[1])

        if coin_on_side1 == 0 or coin_on_side2 == 0:
            self.player_coins[0] += coin_on_side1
            self.player_coins[1] += coin_on_side2
            winner = None
            if self.player_coins[0] > self.player_coins[1]:
                winner = 0  # Player 1 wins
            elif self.player_coins[0] < self.player_coins[1]:
                winner = 1  # Player 2 wins
            else:
                winner = -1  # Draw
            return True, winner
        return False, -1

    def valid_move(self, player_id, index):
        if 0 <= index <= 6 and self.board[player_id][index] > 0:
            return True
        return False

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
        else:
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
            self.move_coins(player_id, row, col)
        else:
            row, col = self.next_index(row, col)
            if self.board[row][col] > 0:
                self.player_coins[player_id] += self.board[row][col]
                self.board[row][col] = 0

    def get_valid_moves(self, player_id):
        return [i for i in range(7) if self.valid_move(player_id, i)]

    def clone(self):
        new_game = Palankuzhi()
        new_game.board = [self.board[0][:], self.board[1][:]]
        new_game.player_coins = self.player_coins[:]
        return new_game

def minimax(game, depth, player_id, maximizing_player):
    game_over, winner = game.check_for_win()
    if game_over or depth == 0:
        if winner == maximizing_player:
            return float('inf'), None
        elif winner == 1 - maximizing_player:
            return float('-inf'), None
        elif winner == -1:
            return 0, None  # Draw
        else:
            # Heuristic evaluation
            score = game.player_coins[maximizing_player] - game.player_coins[1 - maximizing_player]
            return score, None

    valid_moves = game.get_valid_moves(player_id)
    if not valid_moves:
        # No valid moves, pass the turn
        return minimax(game, depth - 1, 1 - player_id, maximizing_player)

    if player_id == maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in valid_moves:
            new_game = game.clone()
            new_game.move_coins(player_id, player_id, move)
            eval_score, _ = minimax(new_game, depth - 1, 1 - player_id, maximizing_player)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        for move in valid_moves:
            new_game = game.clone()
            new_game.move_coins(player_id, player_id, move)
            eval_score, _ = minimax(new_game, depth - 1, 1 - player_id, maximizing_player)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move
        return min_eval, best_move

def ai_move(game, ai_player_id, depth=4):
    _, best_move = minimax(game, depth, ai_player_id, ai_player_id)
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
                if not game.valid_move(current_player, index):
                    print("Invalid move. Try again.")
                    continue
            except ValueError:
                print("Please enter a number between 1 and 7.")
                continue
        else:
            index = ai_move(game, ai_player)
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
            if winner == human_player:
                print("You Win!!!")
            elif winner == ai_player:
                print("AI Wins!!!")
            else:
                print("It's a Draw!!!")
            game.print_stats()
            break

        current_player = 1 - current_player

if __name__ == '__main__':
    play_game()
