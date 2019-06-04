from queue import PriorityQueue
from functools import total_ordering
from math import sqrt


class AStar:

    @total_ordering
    class Node:
        def __init__(self, state, landmark):
            self.state = state
            self.landmark = landmark
            self.h = 0.0
            self.g = 0.0
            self.came_from = None

        def __eq__(self, other):
            f = self.h + self.g
            of = other.h + other.g
            return f == of

        def __ne__(self, other):
            return not (self == other)

        def __lt__(self, other):
            f = self.h + self.g
            of = other.h + other.g
            return f < of

    def __init__(self):
        pass

    def find_path(self, start, goal):
        closed = {}
        openMap = {}
        openQueue = PriorityQueue()
        startNode = AStar.Node(start.get_particle_state(), start)
        openMap[startNode.landmark] = startNode
        openQueue.put(startNode)

        current = None

        while len(openMap) > 0:
            current = openQueue.get()
            if current.landmark == goal:
                return self.reconstruct_path(current)
            del openMap[current.landmark]
            closed[current.landmark] = current
            for neighbor in self.neighbors(current):
                if neighbor.landmark not in closed:
                    nextStepCost = current.g + Distance.euclidean(
                        current.state.get_x(), current.state.get_y(), neighbor.state.get_x(),
                        neighbor.state.get_y())
                    if neighbor.landmark not in openMap and nextStepCost < neighbor.g:
                        neighbor.came_from = current
                        neighbor.g = nextStepCost
                        neighbor.h = neighbor.g + self.heuristic_cost(
                            neighbor.state, goal.get_particle_state())
                        if neighbor.landmark not in openMap:
                            openMap[neighbor.landmark] = neighbor
                            openQueue.put(neighbor)

        return None

    def heuristic_cost(self, current_state, end_state):
        return Distance.euclidean(current_state.get_x(), current_state.get_y(), end_state.get_x(), end_state.get_y())

    def neighbors(self, node):
        neighbours = []
        bldg = node.landmark.get_building()
        landmarks = bldg.get_landmarks(node.state)

        for landmark in landmarks:
            neighbor = AStar.Node(ParticleState(landmark.get_x(), landmark.get_y()), landmark)
            neighbours.append(neighbor)

        return neighbours

    def reconstruct_path(self, goal):
        reversePath = []
        current = goal
        while current is not None:
            reversePath.append(current)
            current = current.came_from
        path = Path()
        while len(reversePath) > 0:
            current = reversePath.pop()
            path.add(Step(current.landmark, current.state))


class Distance:

    @staticmethod
    def euclidean(x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        return sqrt(dx * dx + dy * dy)


class Step:

    def __init__(self, landmark, state):
        self.landmark = landmark
        self.state = state


class Path:

    def __init__(self):
        self.steps = []

    def add(self, step):
        self.steps.append(step)


class Landmark:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_particle_state(self):
        pass


class ParticleState:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
