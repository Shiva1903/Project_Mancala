import math
import copy

class Palankuzhi:
    def __init__(self):
        self.board = [
            [5, 5, 5, 5, 5, 5, 5],  # Player 1 (Human) side
            [5, 5, 5, 5, 5, 5, 5]   # Player 2 (AI) side
        ]
        self.player_coins = [0, 0]  # [Human's coins, AI's coins]

    def check_for_win(self, simulate=False):
        coins_on_side = [sum(self.board[0]), sum(self.board[1])]

        if coins_on_side[0] == 0 or coins_on_side[1] == 0:
            if not simulate:
                # Collect remaining coins
                self.player_coins[0] += coins_on_side[0]
                self.player_coins[1] += coins_on_side[1]
                self.board = [[0]*7, [0]*7]  # Empty the board

                if self.player_coins[0] > self.player_coins[1]:
                    print("You win!")
                elif self.player_coins[0] < self.player_coins[1]:
                    print("AI wins!")
                else:
                    print("It's a draw!")
                print("Final Scores:")
                self.print_stats()
            return True
        return False

    def valid_moves(self, player_id):
        return [i for i in range(7) if self.board[player_id][i] > 0]

    def valid_move(self, player_id, pit_index):
        return self.board[player_id][pit_index] > 0

    def print_board(self):
        print("\nCurrent Board:")
        print("  AI Side:   ", self.board[1])
        print("  Your Side: ", self.board[0])
        print("Your Store:", self.player_coins[0], "| AI's Store:", self.player_coins[1])

    def print_stats(self):
        print("Your Total Coins:", self.player_coins[0])
        print("AI's Total Coins:", self.player_coins[1])

    def copy(self):
        new_game = Palankuzhi()
        new_game.board = [self.board[0][:], self.board[1][:]]
        new_game.player_coins = self.player_coins[:]
        return new_game

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

    def check_for_pasu(self):
        for player_id in [0, 1]:
            for i in range(7):
                if self.board[player_id][i] == 4:
                    self.player_coins[player_id] += 4
                    self.board[player_id][i] = 0

    def move_coins(self, player_id, row, col):
        stones = self.board[row][col]
        self.board[row][col] = 0
        while stones > 0:
            row, col = self.next_index(row, col)
            self.board[row][col] += 1
            stones -= 1
            self.check_for_pasu()
        next_row, next_col = self.next_index(row, col)
        if self.board[next_row][next_col] > 0:
            self.move_coins(player_id, next_row, next_col)
        else:
            next_row, next_col = self.next_index(next_row, next_col)
            if 0 <= next_col <= 6:
                captured_stones = self.board[next_row][next_col]
                self.player_coins[player_id] += captured_stones
                self.board[next_row][next_col] = 0

    def get_score(self, player_id):
        return self.player_coins[player_id] - self.player_coins[1 - player_id]

def iterative_minimax(game, max_depth, player_id):
    stack = []
    root_node = {
        'game': game.copy(),
        'depth': 0,
        'alpha': -math.inf,
        'beta': math.inf,
        'maximizing_player': True,
        'player_id': player_id,
        'value': None,
        'best_move': None,
        'move': None,
        'parent': None,
        'expanded': False
    }
    stack.append(root_node)

    while stack:
        node = stack.pop()

        if node['depth'] == max_depth or node['game'].check_for_win(simulate=True):
            # Leaf node
            node['value'] = node['game'].get_score(player_id)
            continue

        if node['expanded']:
            # Backtracking
            if node['maximizing_player']:
                node['value'] = -math.inf
                for child in node['children']:
                    if child['value'] > node['value']:
                        node['value'] = child['value']
                        node['best_move'] = child['move']
                if node['parent']:
                    node['parent']['alpha'] = max(node['parent']['alpha'], node['value'])
                    if node['parent']['alpha'] >= node['parent']['beta']:
                        continue
            else:
                node['value'] = math.inf
                for child in node['children']:
                    if child['value'] < node['value']:
                        node['value'] = child['value']
                        node['best_move'] = child['move']
                if node['parent']:
                    node['parent']['beta'] = min(node['parent']['beta'], node['value'])
                    if node['parent']['beta'] <= node['parent']['alpha']:
                        continue
        else:
            # Expand node
            node['expanded'] = True
            valid_moves = node['game'].valid_moves(node['player_id'] if node['maximizing_player'] else 1 - node['player_id'])

            if not valid_moves:
                node['value'] = node['game'].get_score(player_id)
                continue

            node['children'] = []
            # Add node back to stack to process after its children
            stack.append(node)

            for move in valid_moves:
                child_game = node['game'].copy()
                current_player_id = node['player_id'] if node['maximizing_player'] else 1 - node['player_id']
                child_game.move_coins(current_player_id, current_player_id, move)

                child_node = {
                    'game': child_game,
                    'depth': node['depth'] + 1,
                    'alpha': node['alpha'],
                    'beta': node['beta'],
                    'maximizing_player': not node['maximizing_player'],
                    'player_id': node['player_id'],
                    'value': None,
                    'move': move,
                    'parent': node,
                    'expanded': False
                }
                node['children'].append(child_node)
                stack.append(child_node)  # Add child to stack

    return root_node['best_move']

def ai_move(game, player_id):
    max_depth = 5  # Adjust for difficulty
    best_move = iterative_minimax(game, max_depth, player_id)
    return best_move

def main():
    game = Palankuzhi()
    current_player = 0  # 0 for Human, 1 for AI
    game.print_board()
    while True:
        if current_player == 0:
            # Human's turn
            valid = False
            while not valid:
                try:
                    move = int(input("\nYour turn! Select a pit (1-7): ")) - 1
                    if move in game.valid_moves(0):
                        valid = True
                    else:
                        print("Invalid move. Try again.")
                except ValueError:
                    print("Please enter a number between 1 and 7.")
            game.move_coins(0, 0, move)
            game.print_board()
            if game.check_for_win():
                break
        else:
            # AI's turn
            print("\nAI is thinking...")
            move = ai_move(game, 1)
            if move is not None:
                print(f"AI selects pit {move + 1}.")
                game.move_coins(1, 1, move)
                game.print_board()
                if game.check_for_win():
                    break
            else:
                print("AI has no valid moves.")
                if game.check_for_win():
                    break
        current_player = 1 - current_player  # Switch players

if __name__ == "__main__":
    main()
