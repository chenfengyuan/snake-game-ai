# coding=utf-8
from .snake import Board


class Ai(object):

    def __init__(self, board):
        del board

    @staticmethod
    def get_actions(board):
        """
        :type board:  Board
        :return list[tuple[int, int]]
        """
        height = board.height
        weight = board.weight
        assert board.snake[0] == (0, 2), board.snake
        assert weight >= 2
        actions = []
        for _ in xrange(weight - 3):
            actions.append(Board.RIGHT)
        assert height % 2 == 0
        for i in xrange(height - 1):
            actions.append(Board.DOWN)
            for j in xrange(weight - 2):
                if i % 2 == 0:
                    actions.append(Board.LEFT)
                else:
                    actions.append(Board.RIGHT)
        actions.append(Board.LEFT)
        for _ in xrange(height - 1):
            actions.append(Board.UP)
        actions.append(Board.RIGHT)
        actions.append(Board.RIGHT)
        return actions


