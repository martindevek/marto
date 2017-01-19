# declaro la clase a objeto de mantener mas legible el código
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

# se encarga de arrancar la recursión y comprobar que la solución sea posible dada las capacidades de cada jarra
def jarSolver(jarA, jarB, solution):
    if jarA.capacity < solution and jarB.capacity < solution:
        return None

    history = [] # lista que va a contener el historial de estados de las jarras
    jarRecursion(jarA, jarB, solution, history, "") # lanza la recursión
    return history

# función recursiva que
def jarRecursion(jarA, jarB, solution, history, state):

    print(jarA.state() + " // " + jarB.state() + "\n")
    if jarA.content == solution or jarB.content == solution:
        return True

    # este buble se repite hasta que las jarras queden en un estado en el cual no hayan estado antes
    while state in history:
        state = doAction(jarA, jarB)
        jarA, jarB = jarB, jarA # hace un swap en las variables

    history.append(state) # agrega el estado actaul al historial
    jarRecursion(jarB, jarA, solution, history, state)

# ejecuta una acción con las jarras
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
