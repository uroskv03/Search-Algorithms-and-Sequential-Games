from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Callable
from heapq import heappush, heappop

from core.grid import Grid
from core.path import Path


@dataclass(slots=True)
class Agent:
    name: str

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        raise NotImplementedError


class ExampleAgent(Agent):

    def __init__(self):
        super().__init__("Example")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        nodes = [start]
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4(r, c)
            min_dist = min(grid.manhattan(t.pos, goal) for t in neighbors)
            best_tiles = [
                tile for tile in neighbors
                if grid.manhattan(tile.pos, goal) == min_dist
            ]
            best_tile = best_tiles[random.randint(0, len(best_tiles) - 1)]

            nodes.append(best_tile.pos)

        return Path(nodes)


class DFSAgent(Agent):

    def __init__(self):
        super().__init__("DFS")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        nodes = [start]
        stack = []
        visited = set()
        while nodes[-1] != goal:
            r, c = nodes[-1]
            visited.add(nodes[-1])
            neighbors = grid.neighbors4Sorted(r, c)
            best_tiles = [
                tile for tile in neighbors
                if tile.pos not in visited
            ]
            best_tiles.reverse()

            if len(best_tiles) > 0:
                for x in best_tiles:
                    stack.append(x)
                nextNode = stack.pop()
            else:
                if not stack:
                    return Path([start])
                nextNode = stack.pop()
                while nodes and nextNode not in grid.neighbors4Sorted(nodes[-1][0], nodes[-1][1]):
                    nodes.pop()

            nodes.append(nextNode.pos)
        return Path(nodes)

    def find_path1(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        nodes = [start]
        stack = []
        while nodes[-1] != goal:
            r, c = nodes[-1]
            neighbors = grid.neighbors4Sorted(r, c)
            best_tiles = [
                tile for tile in neighbors
                if tile.pos not in nodes
            ]
            best_tiles.reverse()
            if len(best_tiles) > 0:
                for x in best_tiles:
                    stack.append(x)
                best_tile = stack.pop()
            else:
                best_tile = stack.pop()
                pom = nodes.copy()
                pom.pop()
                p, q = nodes[-1]
                while (best_tile not in grid.neighbors4Sorted(p, q)):
                    a = pom.pop()
                    nodes.append(a)
                    p, q = nodes[-1]

            nodes.append(best_tile.pos)
        return Path(nodes)


class BranchAndBoundAgent(Agent):

    def __init__(self):
        super().__init__("BranchAndBound")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        prio = []
        heappush(prio, (0, 1, [start]))
        bestCost = {start: 0}
        while prio:
            cost, len, path = heappop(prio)
            cur = path[-1]
            print("Putanja:", path, "Cena: ", cost)
            if cur == goal:
                return Path(path)

            r, c = cur
            for title in grid.neighbors4(r, c):
                if title.pos not in path and not (title.pos in bestCost and bestCost[title.pos] <= cost + title.cost):
                    bestCost[title.pos] = cost + title.cost
                    heappush(prio, (cost + title.cost, len + 1, path + [title.pos]))

        return Path([start])


class AStar(Agent):

    def __init__(self):
        super().__init__("AStar")

    def find_path(self, grid: Grid, start: tuple[int, int], goal: tuple[int, int]) -> Path:
        prio = []
        heappush(prio, (grid.manhattan(start, goal), 1, 0, [start]))
        bestCost = {start: 0}
        while (prio):
            hier, len, cost, path = heappop(prio)
            cur = path[-1]
            print("Putanja:", path, "Hier: ", hier, "Cost: ", cost)
            if cur == goal:
                return Path(path)

            r, c = cur
            for title in grid.neighbors4(r, c):
                if title.pos not in path and not (title.pos in bestCost and bestCost[title.pos] <= cost + title.cost):
                    bestCost[title.pos] = cost + title.cost
                    heappush(prio, (grid.manhattan(title.pos, goal) + cost + title.cost, len + 1, cost + title.cost,
                                    path + [title.pos]))

        return Path([start])


AGENTS: dict[str, Callable[[], Agent]] = {
    "Example": ExampleAgent,
    "DFS": DFSAgent,
    "BranchAndBound": BranchAndBoundAgent,
    "AStar": AStar
}


def create_agent(name: str) -> Agent:
    if name not in AGENTS:
        raise ValueError(f"Unknown agent '{name}'. Available: {', '.join(AGENTS.keys())}")
    return AGENTS[name]()
