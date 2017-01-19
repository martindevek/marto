class Jar:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.content = 0

    def fill(self):
        self.content = self.capacity

    def empty(self):
        self.content = 0

    def ifEmpty(self):
        return self.capacity == 0

    def isFull(self):
        return self.content >= self.capacity

    def toJar(self, otherJar):
        aux = self.content
        self.content = max(self.content - otherJar.left(), 0)
        otherJar.content = min(aux + otherJar.content, otherJar.capacity)

    def left(self):
        return self.capacity - self.content

    def state(self):
        return self.name + " capacity: " + str(self.capacity) + " - content: " + str(self.content)


def jarSolver(jarA, jarB, solution):
    if jarA.capacity < solution and jarB.capacity < solution:
        return None

    history = []
    jarRecursion(jarA, jarB, solution, history, "")
    return history

def jarRecursion(jarA, jarB, solution, history, state):

    if jarA.content == solution or jarB.content == solution:
        return True

    while state in history:
        state = doAction(jarA, jarB)
        jarA, jarB = jarB, jarA

    history.append(state)
    jarRecursion(jarB, jarA, solution, history, state)


def doAction(jarA, jarB):

    # pass jar_a to jar_b
    if jarA.content > 0 and jarB.content < jarB.capacity:
        jarA.toJar(jarB)

    # fill jar_a
    elif jarA.content < jarA.capacity:
        jarA.fill()

    # empty jar_a
    elif jarA.content > 0:
        jarA.empty()

    return jarA.state() + " // " + jarB.state()

# MAIN PROGRAM
JAR_A = 4
JAR_B = 3
SOLUTION = 2

jarA = Jar("Jar A", JAR_A)
jarB = Jar("Jar B", JAR_B)

sol = jarSolver(jarA, jarB, SOLUTION)

for line in sol:
    print(line)
