class Jar:
    def __init__(self, capacity):
        self.capacity = capacity
        self.content = 0

    def fill(self):
        if self.content < self.capacity:
            self.content = self.capacity
            return True

    def fillWith(self, cant):
        self.content = min(self.capacity, self.content+cant)

    def empty(self):
        if self.capacity > 0:
            self.content = 0
            return True

    def ifEmpty(self):
        return self.capacity == 0

    def isFull(self):
        return self.content >= self.capacity

    def toJar(self, otherJar):
        if (not self.empty) and (not otherJar.isFull):
            aux = self.content
            self.content = min(self.content - otherJar.left, 0)
            otherJar.content = max(aux + otherJer.content, otherJar.capacity)
            return True


def jarSolver(jarA, jarB, solution):
    if jarA.capacity < solution and jarB.capacity < solution:
        return None

    return jarRecursion(jarA, jarB, solution, "")

def jarRecursion(jarA, jarB, solution, action):

    print("jarA="+str(jarA.content)+"\njarB="+str(jarB.content)+"\n\n")

    if jarA.content == solution or jarB.content == solution:
        print(action)
        return True

    # fill jar_a
    if jarA.fill():
        jarRecursion(jarA, jarB, solution, "Fill Jar A\n")

    # pass jar_a to jar_b
    if jarA.toJar(jarB):
        jarRecursion(jarA, jarB, solution, "Pass A to B\n")

    # fill jar_b
    if jarB.fill():
        jarRecursion(jarA, jarB, solution, "Fill Jar B\n")

    # pass jar_b to jar_a
    if jarB.toJar(jarA):
        jarRecursion(jarA, jarB, solution, "Pass B to A\n")

    # empty jar_a
    if jarA.empty():
        jarRecursion(jarA, jarB, solution, "Empty Jar A\n")

    # empty jar_b
    if jarB.empty():
        jarRecursion(jarA, jarB, solution, "Empty Jar B\n")


# MAIN PROGRAM
JAR_A = 4
JAR_B = 3
SOLUTION = 2

jarA = Jar(JAR_A)
jarB = Jar(JAR_B)

sol = jarSolver(jarA, jarB, SOLUTION)

if not sol:
    print("There are no posible solution.\n")
