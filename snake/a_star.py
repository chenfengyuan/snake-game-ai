# coding=utf-8
from collections import (
    namedtuple,
)
import heapq
import logging
import random
from snake import Board


logger = logging.getLogger(__name__)


class Impl(object):

    SnakePath = namedtuple('SnakePath', ['total_distance', 'snake', 'before_eat_food_actions',
                                         'after_eat_food_actions',
                                         'food_ate'])

    def __init__(self, board):
        """
        :type board: Board
        """
        self.board = board
        self.snake_paths = [self.SnakePath(0, board.snake, [], [], False)]

    def _get_distance(self, snake, food_ate):
        """
        :type snake: list[tuple[int, int]]
        :type food_ate: bool
        """
        head = snake[0]
        last = snake[-1]
        if food_ate:
            return Board.get_distance(head, last)
        else:
            return Board.get_distance(head, self.board.food) + Board.get_distance(self.board.food, last)

    def _move_snake(self, snake, direction, food_ate):
        """
        :type snake: list[tuple[int, int]]
        :type direction: tuple[int, int]
        :type food_ate: bool
        :rtype: bool, list[tuple[int, int]]
        """
        h = snake[0]
        new_snake = [(h[0] + direction[0], h[1] + direction[1])]
        if food_ate:
            for i in xrange(len(snake)-1):
                new_snake.append(snake[i])
            return True, new_snake
        else:
            if new_snake[0] == self.board.food:
                new_snake += snake
                return True, new_snake
            else:
                for i in xrange(len(snake)-1):
                    new_snake.append(snake[i])
                return False, new_snake

    def is_safe(self, snake, food_ate):
        """
        :type snake: list[tuple[int, int]]
        :type food_ate: bool
        :rtype: bool
        """
        if not self.board.is_safe(snake):
            return False
        if food_ate:
            if len(snake) == self.board.height * self.board.weight:
                return True
            else:
                ps = set(snake)
                ps.remove(snake[-1])
                p = snake[0]
                for dir_ in Board.DIRECTIONS:
                    y, x = (p[0] + dir_[0], p[1] + dir_[1])
                    if not (0 <= y < self.board.height):
                        continue
                    if not (0 <= x < self.board.weight):
                        continue
                    if (y, x) in ps:
                        continue
                    else:
                        return True
                return False
        else:
            return True

    def is_space_between_head_and_tail(self, snake):
        """
        :type snake: list[tuple[int, int]]
        :rtype: bool
        """
        ps = set(snake)
        y1, x1 = snake[0]
        y2, x2 = snake[-1]
        ps -= {snake[0], snake[-1]}
        if y1 > y2:
            y1, y2 = y2, y1
        if x1 > x2:
            x1, x2 = x2, x1
        space_count = -2
        for y in xrange(y1, y2 + 1):
            for x in xrange(x1, x2 + 1):
                if (y, x) in ps:
                    return False
                else:
                    space_count += 1
        if space_count >= 1:
            return True
        if len(snake) == self.board.height * self.board.weight:
            return True
        return False

    def search(self):
        """
        :rtype list[int]|None
        """
        count = 0
        while self.snake_paths:
            # logger.debug((len(self.snake_paths[0].snake), len(self.snake_paths[0].before_eat_food_actions),
            #               len(self.snake_paths[0].after_eat_food_actions), self.snake_paths[0].food_ate,
            #               len(self.snake_paths), count))
            count += 1
            snake_path = heapq.heappop(self.snake_paths)
            assert isinstance(snake_path, self.SnakePath)
            snake = snake_path.snake
            """:type: list[tuple[int, int]]"""
            for dir_ in Board.DIRECTIONS:
                food_ate = snake_path.food_ate
                new_food_ate, new_snake = self._move_snake(snake, dir_, food_ate)
                if self.is_safe(new_snake, new_food_ate):
                    distance = self._get_distance(new_snake, new_food_ate)
                    if food_ate:
                        before_eat_food_actions = snake_path.before_eat_food_actions
                        after_eat_food_actions = snake_path.after_eat_food_actions[:]
                        after_eat_food_actions.append(dir_)
                    else:
                        before_eat_food_actions = snake_path.before_eat_food_actions[:]
                        before_eat_food_actions.append(dir_)
                        after_eat_food_actions = snake_path.after_eat_food_actions
                    distance = distance * 5 + len(before_eat_food_actions) + len(after_eat_food_actions)

                    if new_food_ate or food_ate:
                        if len(new_snake) <= 5:
                            return before_eat_food_actions
                        elif self.is_space_between_head_and_tail(new_snake):
                            return before_eat_food_actions
                    heapq.heappush(self.snake_paths, self.SnakePath(distance, new_snake, before_eat_food_actions,
                                                                    after_eat_food_actions, new_food_ate))
        logger.debug('following tail')
        self.snake_paths = [self.SnakePath(0, self.board.snake, [], [], False)]
        while self.snake_paths:
            logger.debug((len(self.snake_paths[0].snake), len(self.snake_paths[0].before_eat_food_actions),
                          len(self.snake_paths[0].after_eat_food_actions), self.snake_paths[0].food_ate,
                          len(self.snake_paths), count))
            snake_path = heapq.heappop(self.snake_paths)
            logger.debug(snake_path)
            assert isinstance(snake_path, self.SnakePath)
            snake = snake_path.snake
            """:type: list[tuple[int, int]]"""
            for dir_ in Board.DIRECTIONS:
                food_ate = snake_path.food_ate
                new_food_ate, new_snake = self._move_snake(snake, dir_, food_ate)
                if self.is_safe(new_snake, new_food_ate):
                    distance = self._get_distance(new_snake, True)
                    if food_ate:
                        before_eat_food_actions = snake_path.before_eat_food_actions
                        after_eat_food_actions = snake_path.after_eat_food_actions[:]
                        after_eat_food_actions.append(dir_)
                    else:
                        before_eat_food_actions = snake_path.before_eat_food_actions[:]
                        before_eat_food_actions.append(dir_)
                        after_eat_food_actions = snake_path.after_eat_food_actions
                    distance = distance * 5 + len(before_eat_food_actions) + len(after_eat_food_actions)
                    distance += random.randint(0, 1)

                    if self.is_space_between_head_and_tail(new_snake):
                        logger.debug('return')
                        return before_eat_food_actions + after_eat_food_actions
                    heapq.heappush(self.snake_paths, self.SnakePath(distance, new_snake, before_eat_food_actions,
                                                                    after_eat_food_actions, new_food_ate))


class Ai(object):
    def __init__(self, board):
        del board

    @staticmethod
    def get_actions(board):
        """
        :type board: Board
        :rtype list[tuple[int, int]]
        """
        impl = Impl(board)
        rv = impl.search()
        return rv
