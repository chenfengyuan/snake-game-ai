# coding=utf-8
import curses
import random
import logging

logger = logging.getLogger(__name__)


class Board(object):
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)
    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    CH_SNAKE_BODY_UP = '^'
    CH_SNAKE_BODY_DOWN = 'v'
    CH_SNAKE_DODY_LEFT = '<'
    CH_SNAKE_BODY_RIGHT = '>'

    class NotSafeSnake(Exception):
        pass

    class Win(Exception):
        pass

    def __init__(self, height, weight):
        self.height = height
        self.weight = weight
        self.arr = [' '] * (height * weight)
        self.snake = [(0, 2), (0, 1), (0, 0)]
        self.food = self._generate_food()
        self.score = 0
        self.moves = 0
        self._draw()

    def get(self, y, x):
        """
        :type y: int
        :type x: int
        :rtype: str
        """
        return self.arr[y * self.weight + x]

    @staticmethod
    def get_distance(p1, p2):
        """
        :type p1: tuple[int, int]
        :type p2: tuple[int, int]
        :rtype: int
        """
        return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

    def _generate_food(self):
        choices = set()
        for y in xrange(self.height):
            for x in xrange(self.weight):
                choices.add((y, x))
        for p in self.snake:
            choices.remove(p)
        if not choices:
            raise self.Win()
        return random.choice(list(choices))

    def _draw(self):
        self.arr = [' '] * (self.height * self.weight)
        self._set(self.snake[0], '*')
        for i in xrange(1, len(self.snake)):
            p1 = self.snake[i - 1]
            p2 = self.snake[i]
            last_direction = self._get_ch_snake_body(p1, p2)
            self._set(p2, last_direction)
        self._set(self.snake[-1], '%')
        self._set(self.food, '#')

    def _set(self, p, ch):
        y, x = p
        self.arr[y * self.weight + x] = ch

    def _get_ch_snake_body(self, p2, p1):
        """
        :type p1: tuple[int, int]
        :type p2: tuple[int, int]
        :rtype str
        """
        y1, x1 = p1
        y2, x2 = p2
        if y1 > y2:
            assert x1 == x2
            return self.CH_SNAKE_BODY_UP
        elif y1 < y2:
            assert x1 == x2
            return self.CH_SNAKE_BODY_DOWN
        elif x1 < x2:
            assert y1 == y2
            return self.CH_SNAKE_BODY_RIGHT
        elif x1 > x2:
            assert y1 == y2
            return self.CH_SNAKE_DODY_LEFT
        else:
            raise RuntimeError("wrong path {} -> {}".format(p1, p2))

    def is_safe(self, snake):
        """
        :type snake: list[tuple[int, int]]
        """
        p_set = set()
        for p in snake:
            if p in p_set:
                return False
            else:
                p_set.add(p)
            y, x = p
            if not (0 <= y < self.height):
                return False
            if not (0 <= x < self.weight):
                return False
        return True

    def move(self, actions):
        """
        :type actions: list[tuple(int, int)]
        """
        for action in actions:
            touch_food = False
            new_snake = []
            p = self.snake[0]
            new_p = (p[0] + action[0], p[1] + action[1])
            new_snake.append(new_p)
            if new_p == self.food:
                touch_food = True
                new_snake += self.snake
            else:
                for i in xrange(0, len(self.snake) - 1):
                    new_snake.append(self.snake[i])
            if not self.is_safe(new_snake):
                logger.debug(new_snake)
                raise self.NotSafeSnake()
            self.snake = new_snake
            self.moves += 1
            if touch_food:
                self.score += 1
                self.food = self._generate_food()
            self._draw()
            yield


class Console(object):

    def __enter__(self):
        curses.initscr()
        return self

    def draw(self, board):
        assert isinstance(board, Board)
        del self
        win = curses.newwin(board.height + 2, board.weight + 2, 0, 0)
        win.keypad(1)
        curses.noecho()
        curses.curs_set(0)
        win.border(0)
        win.nodelay(1)
        for height in xrange(0, board.height):
            for weight in xrange(0, board.weight):
                win.addch(height + 1, weight + 1, board.get(height, weight))
        return win.getch()

    def __exit__(self, exc_type, exc_val, exc_tb):
        del exc_tb, exc_type, exc_val
        curses.endwin()
