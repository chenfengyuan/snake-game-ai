# coding=utf-8
from snake import snake, naive, a_star, plain
import random
import logging
import time
import sys

logger = logging.getLogger(__name__)


def main():
    random.seed(42)
    board = snake.Board(10, 10)
    ai = naive.Ai(board)
    if len(sys.argv) > 1:
        if sys.argv[1] == 'plain':
            ai = plain.Ai(board)
        elif sys.argv[1] == 'a_star':
            ai = a_star.Ai(board)
    try:
        with snake.Console() as console:
            while True:
                actions = ai.get_actions(board)
                if not isinstance(actions, list):
                    logger.debug('no moves')
                if not actions:
                    logger.debug('no moves')
                    raise board.NotSafeSnake()
                logger.debug((board.snake, actions))
                try:
                    for _ in board.move(actions):
                        console.draw(board)
                        # time.sleep(0.01)
                except board.NotSafeSnake:
                    raise
    except board.Win:
        print 'You Win!!! score:{}, moves:{}'.format(board.score, board.moves)
    except board.NotSafeSnake:
        print 'Game Over!!! score:{}, moves:{}'.format(board.score, board.moves)

if __name__ == '__main__':
    main()
