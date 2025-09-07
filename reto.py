from typing import List, Tuple, Set

GOAL = (1,2,3,4,5,6,7,8,0)  # 0 es "_"

def manhattan(state: Tuple[int, ...]) -> int:
    d = 0
    for i,v in enumerate(state):
        if v == 0: 
            continue
        gi = v-1
        x1,y1 = divmod(i,3); x2,y2 = divmod(gi,3)
        d += abs(x1-x2) + abs(y1-y2)
    return d

def neighbors(state: Tuple[int, ...]):
    i = state.index(0)
    x,y = divmod(i,3)
    def swap(j,k):
        s = list(state); s[j],s[k] = s[k],s[j]; return tuple(s)
    moves = []
    if x>0: moves.append(("up",   swap(i, i-3)))
    if x<2: moves.append(("down", swap(i, i+3)))
    if y>0: moves.append(("left", swap(i, i-1)))
    if y<2: moves.append(("right",swap(i, i+1)))
    # solo para ordenar la exploración (sigue siendo DFS con límite)
    moves.sort(key=lambda t: manhattan(t[1]))
    return moves

def is_solvable(state: Tuple[int, ...]) -> bool:
    a = [x for x in state if x!=0]
    inv = sum(1 for i in range(len(a)) for j in range(i+1,len(a)) if a[i]>a[j])
    return inv % 2 == 0

def iddfs(start: Tuple[int, ...], max_depth=60):
    if not is_solvable(start): 
        return None, None

    if start == GOAL: 
        return [], [start]

    for limit in range(max_depth+1):
        visited: Set[Tuple[int,...]] = set()
        path: List[Tuple[str, Tuple[int,...]]] = []

        def backtracking(s: Tuple[int,...], depth: int) -> bool:
            if s == GOAL: 
                return True
            if depth == limit: 
                return False
            visited.add(s)

            for mv, nxt in neighbors(s):
                if nxt in visited: 
                    continue

                path.append((mv, nxt))   
                if backtracking(nxt, depth+1): 
                    return True
                path.pop()               
            
            visited.remove(s)            
            return False

        if backtracking(start, 0):
            moves = [mv for mv,_ in path]
            states = [start] + [st for _,st in path]
            return moves, states
    return None, None


def show(state):  # pretty print
    def ch(v): return "_" if v==0 else str(v)
    for r in range(0,9,3):
        print(" ".join(ch(x) for x in state[r:r+3]))
    print()


start1 = (1,8,3, 2,6,4, 7,0,5)
moves, states = iddfs(start1)
print("¿Soluble?", is_solvable(start1))

if moves is None:
    print("No se encontró solución.")
else:
    print(f"\nSolución encontrada en {len(moves)} pasos\n")

    # Estado inicial
    print("Estado inicial:")
    show(states[0])

    # Secuencia de pasos
    for i, (mv, st) in enumerate(zip(moves, states[1:]), 1):
        print(f"Paso {i}: mover {mv}")
        show(st)

    # Estado final
    print("Estado final:")
    show(states[-1])
