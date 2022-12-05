#
# Web based GUI for BBC chess engine
#

# packages
from pathlib import Path

from flask import Flask
from flask import render_template
from flask import request
import chess
import chess.engine
import chess.pgn
import io
import random
from flask import jsonify
from flask import Response
import json
import subprocess

# create web app instance
app = Flask(__name__)


# root(index) route
@app.route('/')
def root():
    return render_template('bbc.html')


# make move API
@app.route('/make_move', methods=['POST'])
def make_move():
    # extract FEN string from HTTP POST request body
    pgn = request.form.get('pgn')

    # read game moves from PGN
    game = chess.pgn.read_game(io.StringIO(pgn))

    # init board
    board = game.board()

    # loop over moves in game
    for move in game.mainline_moves():
        # make move on chess board
        board.push(move)

    print(board.fen())

    completedProcess = subprocess.run(
        [Path(__file__).parent / "HaskellChessEngine", board.fen()], capture_output=True)

    move = completedProcess.stdout.decode("ascii").strip()

    # create chess engine instance
    engine = chess.engine.SimpleEngine.popen_uci('./engine2.py')

    # terminate engine process
    engine.quit()

    # extract best move from PV
    best_move = chess.Move.from_uci(move)

    # update internal python chess board state
    board.push(best_move)

    # get best score

    return {
        'fen': board.fen(),
        'best_move': str(best_move),
        'score': 100,
        'depth': 42,
        'pv': 'disabled',  # '.join([str(move) for move in info['pv']]),
        'nodes': "no nodes",  # info['nodes'],
        'time': 1337  # info['time']
    }


@app.route('/analytics')
def analytics():
    return render_template('stats.html')


@app.route('/analytics/api/post', methods=['POST'])
def post():
    response = Response('')
    response.headers['Access-Control-Allow-Origin'] = '*'

    stats = {
        'Date': request.form.get('date'),
        'Url': request.form.get('url'),
        'Agent': request.headers.get('User-Agent')
    }

    if request.headers.getlist("X-Forwarded-For"):
        stats['Ip'] = request.headers.getlist("X-Forwarded-For")[0]
    else:
        stats['Ip'] = request.remote_addr

    if request.headers.get('Origin'):
        stats['Origin'] = request.headers.get('Origin')
    else:
        stats['Origin'] = 'N/A'

    if request.headers.get('Referer'):
        stats['Referer'] = request.headers.get('Referer')
    else:
        stats['Referer'] = 'N/A'

    with open('stats.json', 'a') as f:
        f.write(json.dumps(stats, indent=2) + '\n\n')
    return response


@app.route('/analytics/api/get')
def get():
    stats = []

    with open('stats.json') as f:
        for entry in f.read().split('\n\n'):
            try:
                stats.append(json.loads(entry))
            except:
                pass

    return jsonify({'data': stats})


# main driver
if __name__ == '__main__':
    # start HTTP server
    app.run(debug=True, threaded=True)
