from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def check_winner(board):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],  # rows
        [0,3,6],[1,4,7],[2,5,8],  # cols
        [0,4,8],[2,4,6]           # diagonals
    ]
    for combo in wins:
        a, b, c = combo
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], combo
    return None, None

def minimax(board, is_maximizing):
    winner, _ = check_winner(board)
    if winner == 'O': return 10
    if winner == 'X': return -10
    if all(cell != '' for cell in board): return 0

    if is_maximizing:
        best = -1000
        for i in range(9):
            if board[i] == '':
                board[i] = 'O'
                best = max(best, minimax(board, False))
                board[i] = ''
        return best
    else:
        best = 1000
        for i in range(9):
            if board[i] == '':
                board[i] = 'X'
                best = min(best, minimax(board, True))
                board[i] = ''
        return best

def best_move(board):
    best_val = -1000
    move = -1
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            val = minimax(board, False)
            board[i] = ''
            if val > best_val:
                best_val = val
                move = i
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    mode = data.get('mode', 'pvp')

    winner, winning_combo = check_winner(board)
    if winner or all(cell != '' for cell in board):
        return jsonify({'board': board, 'winner': winner, 'winning_combo': winning_combo, 'draw': not winner})

    if mode == 'ai':
        ai_move = best_move(board)
        if ai_move != -1:
            board[ai_move] = 'O'

    winner, winning_combo = check_winner(board)
    draw = not winner and all(cell != '' for cell in board)

    return jsonify({
        'board': board,
        'winner': winner,
        'winning_combo': winning_combo,
        'draw': draw,
        'ai_move': ai_move if mode == 'ai' else None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
