# coding-utf8
from .snake import Board
import logging
logger = logging.getLogger(__name__)


class Ai(object):
    def __init__(self, board):
        """
        :type board: Board
        """
        assert board.snake[0] == (0, 2), board.snake
        assert board.weight >= 2
        self.height = board.height
        self.weight = board.weight

    def get_actions(self, board):
        """
        :type board: Board
        :rtype: list[tuple[int, int]]
        """
        food = board.food
        head = board.snake[0]
        hy, hx = head
        fy, fx = food
        assert hx == 2
        block_height = (len(board.snake) + 2) / board.weight + 2
        if block_height % 2 == 1:
            block_height += 1
        while self.height % block_height > 0:
            block_height += 2
        h_block = hy / block_height
        f_block = fy / block_height
        return self._generate_move_actions(h_block, f_block, block_height)

    def _generate_move_actions(self, from_block_num, to_block_num, block_height):
        logger.debug((from_block_num, to_block_num, block_height))
        actions = []
        if to_block_num >= from_block_num:
            for _ in xrange(self.weight - 3):
                actions.append(Board.RIGHT)
            actions.append(Board.DOWN)
            for _ in xrange(self.weight - 2):
                actions.append(Board.LEFT)
            for _ in xrange(0, (to_block_num - from_block_num + 1) * block_height - 2, 2):
                actions.append(Board.DOWN)
                for _1 in xrange(self.weight - 2):
                    actions.append(Board.RIGHT)
                actions.append(Board.DOWN)
                for _1 in xrange(self.weight - 2):
                    actions.append(Board.LEFT)
            for i in xrange(to_block_num - from_block_num + 1):
                for j in xrange(block_height):
                    if i == 0 and j == 0:
                        actions.append(Board.LEFT)
                    else:
                        actions.append(Board.UP)
            for _ in xrange(2):
                actions.append(Board.RIGHT)
        else:
            for _ in xrange(self.weight - 3):
                actions.append(Board.RIGHT)
            actions.append(Board.DOWN)
            for _ in xrange(self.weight - 2):
                actions.append(Board.LEFT)
            for _ in xrange(0, block_height - 2, 2):
                actions.append(Board.DOWN)
                for _1 in xrange(self.weight - 2):
                    actions.append(Board.RIGHT)
                actions.append(Board.DOWN)
                for _1 in xrange(self.weight - 2):
                    actions.append(Board.LEFT)
            for i in xrange(from_block_num - to_block_num + 1):
                for j in xrange(block_height - 1):
                    if i == 0 and j == 0:
                        actions.append(Board.LEFT)
                    else:
                        actions.append(Board.UP)
            for _ in xrange(2):
                actions.append(Board.RIGHT)
        return actions
