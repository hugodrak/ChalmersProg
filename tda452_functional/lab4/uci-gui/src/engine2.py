#! /usr/bin/env python3
# This file is part of YoBot_Bronze UCI Chess Engine.
# Copyright (C) 2021- Yohaan Seth Nathan (TheYoBots)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the MIT License.
#
# You should have received a copy of the MIT License along with this
# UCI Chess Engine. If not, view this https://opensource.org/licenses/MIT

import logging
import chess
import sys

logger = logging.getLogger(__name__)


board = chess.Board()


def send_response(msg: str):
    logger.info(f"< {msg}")
    print(msg)


def command_received(msg: str):
    logger.info(f"> {msg}")

    if msg == "uci":

        send_response("id name YoBot Bronze")
        send_response("id author Yohaan Seth Nathan")
        send_response("option name Debug Log File type string default")
        send_response("option name Contempt type spin default 24 min -100 max 100")
        send_response("option name Analysis Contempt type combo default Both var Off var White var Black var Both")
        send_response("option name Threads type spin default 1 min 1 max 512")
        send_response("option name Hash type spin default 16 min 1 max 131072")
        send_response("option name Clear Hash type button")
        send_response("option name Ponder type check default false")
        send_response("option name MultiPV type spin default 1 min 1 max 500")
        send_response("option name Skill Level type spin default 20 min 0 max 20")
        send_response("option name Move Overhead type spin default 30 min 0 max 5000")
        send_response("option name Minimum Thinking Time type spin default 20 min 0 max 5000")
        send_response("option name Slow Mover type spin default 84 min 10 max 1000")
        send_response("option name nodestime type spin default 0 min 0 max 10000")
        send_response("option name UCI_Chess960 type check default false")
        send_response("option name UCI_AnalyseMode type check default false")
        send_response("option name SyzygyPath type string default <empty>")
        send_response("option name SyzygyProbeDepth type spin default 1 min 1 max 100")
        send_response("option name Syzygy50MoveRule type check default true")
        send_response("option name SyzygyProbeLimit type spin default 7 min 0 max 7")
        send_response("uciok")
        return

    elif msg == "isready":
        send_response("readyok")
        return

    elif msg == "ucinewgame":
        return


    elif msg == "isready":

        send_response("readyok")

        return


    elif msg == "ucinewgame":

        return


    elif "position startpos moves" in msg:

        moves = msg.split(" ")[3:]

        board.clear()

        board.set_fen(chess.STARTING_FEN)

        for move in moves:
            board.push(chess.Move.from_uci(move))

        return


    elif "position fen" in msg:

        fen = " ".join(msg.split(" ")[2:])

        board.set_fen(fen)

        return


    elif msg[0:2] == "go":

        _move = get_best_move(board)

        send_response(f"bestmove {_move}")

        return


    elif msg == "quit":

        sys.exit(0)


def main():
    logging.basicConfig(filename='logs.txt', level=logging.INFO,
                        format='%(asctime)s %(message)s')
    logging.info('YoBot Bronze started')

    try:
        while True:
            msg = input()
            command_received(msg)

    except Exception:
        logging.exception('Fatal error in main loop')


import logging
import chess
import random
import sys

logger = logging.getLogger(__name__)

def get_best_move(board: chess.Board) -> chess.Move:

    my_color = board.turn
    global_max_score = -sys.maxsize
    best_moves = []

    # attacked_pieces = get_attacked_pieces(board, my_color)
    # print(attacked_pieces)

    for my_candidate_move in list(board.legal_moves):

        board.push(my_candidate_move)

        bonus = 0

        if board.is_checkmate():
            return my_candidate_move

        if board.is_stalemate():
            bonus = +500

        if board.can_claim_threefold_repetition():
            current_score = __get_board_total_score(board, my_color)
            if current_score > 0:
                bonus = +1
            else:
                bonus = -1

        is_my_candidate_move_attacked = __is_attacked(board, my_candidate_move.to_square)

        candidate_min_score = sys.maxsize

        for opponent_candidate_move in list(board.legal_moves):

            board.push(opponent_candidate_move)

            if board.is_checkmate():
                current_score = -9999
            else:
                current_score = __get_board_total_score(board, my_color) + bonus
                if is_my_candidate_move_attacked:
                    current_score = current_score + 1

            candidate_min_score = min(current_score, candidate_min_score)

            board.pop()

        if candidate_min_score > global_max_score:
            global_max_score = candidate_min_score
            best_moves = [my_candidate_move]

        elif candidate_min_score == global_max_score:
            best_moves.append(my_candidate_move)

        board.pop()

    best_move = random.choice(best_moves)

    # Always promote to queen.
    if best_move.uci()[-1].isalpha():
        best_move.promotion = chess.QUEEN

    return best_move


def get_attacked_pieces(board: chess.Board, defending_color: chess.Color):

    attacked_pieces = { }

    for square, piece in board.piece_map().items():

        if board.color_at(square) != defending_color:
            continue

        attacking_pieces = get_attacking_pieces(board, not defending_color, square)
        if len(attacking_pieces) > 0:

            defending_pieces = get_defending_pieces(board, defending_color, square)
            attacked_pieces[square] = (piece.piece_type, attacking_pieces, defending_pieces)

    return attacked_pieces

def __is_attacked(board: chess.Board, square: chess.Square):

    return len(board.attacks(square)) > 1

def get_attacking_pieces(board: chess.Board, attacking_color: chess.Color, square: chess.Square) -> [chess.PieceType]:

    piece_types = []

    attacking_squares = board.attackers(attacking_color, square)

    for attacking_square in attacking_squares:

        if board.is_pinned(attacking_color, attacking_square) == False:
            piece_type = board.piece_type_at(attacking_square)
            piece_types.append(piece_type)

    return piece_types

def get_defending_pieces(board: chess.Board, defending_color: chess.Color, square: chess.Square) -> [chess.PieceType]:

    cloned_board = board.copy()

    defending_pieces = get_attacking_pieces(cloned_board, defending_color, square)

    del cloned_board

    return defending_pieces

def get_board_score(board: chess.Board, color: chess.Color) -> int:

    total = 0

    pawns = board.pieces(chess.PAWN, color)
    bishops = board.pieces(chess.BISHOP, color)
    knights = board.pieces(chess.KNIGHT, color)
    queens = board.pieces(chess.QUEEN, color)
    rooks = board.pieces(chess.ROOK, color)

    for _ in pawns:
        total += 10
    for _ in bishops:
        total += 30
    for _ in knights:
        total += 30
    for _ in queens:
        total += 90
    for _ in rooks:
        total += 50

    if (board.has_kingside_castling_rights(color)):
        total += 1

    if (board.has_queenside_castling_rights(color)):
        total += 1

    return total

def __get_board_total_score(board: chess.Board, color: chess.Color) -> int:

    color_score = get_board_score(board, color)
    opposite_color_score = get_board_score(board, not color)
    return color_score - opposite_color_score


if __name__ == '__main__':
    main()
