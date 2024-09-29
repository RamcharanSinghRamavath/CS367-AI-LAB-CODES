import heapq

def is_goal(board):
    return sum(row.count(1) for row in board) == 1 and board[3][3] == 1

def generate_moves(board):
    moves = []
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  
    for r in range(7):
        for c in range(7):
            if board[r][c] == 1:
                for dr, dc in directions:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 7 and 0 <= nc < 7 and board[nr][nc] == 0:
                        mid_r, mid_c = r + dr // 2, c + dc // 2
                        if board[mid_r][mid_c] == 1:  
                            n_board = [row[:] for row in board]
                            n_board[r][c], n_board[mid_r][mid_c], n_board[nr][nc] = 0, 0, 1
                            moves.append(n_board)
    return moves

def heuristic_remaining_marbles(board):
    return sum(row.count(1) for row in board)

def a_star_search(initial_board, heuristic):
    pq = []
    heapq.heappush(pq, (heuristic(initial_board), 0, initial_board, []))  
    
    while pq:
        f, g, board, moves = heapq.heappop(pq)
        
        if is_goal(board):
            return moves 
        
        for n_board in generate_moves(board):
            new_moves = moves + [n_board]
            g_new = g + 1  
            f_new = g_new + heuristic(n_board)
            heapq.heappush(pq, (f_new, g_new, n_board, new_moves))

    return None 

initial_board = [
    [None, None, 1, 1, 1, None, None],
    [None, None, 1, 1, 1, None, None],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],  
    [1, 1, 1, 1, 1, 1, 1],
    [None, None, 1, 1, 1, None, None],
    [None, None, 1, 1, 1, None, None]
]

moves = a_star_search(initial_board, heuristic_remaining_marbles)
print(f"Moves to solve: {len(moves) if moves else 'No solution'}")