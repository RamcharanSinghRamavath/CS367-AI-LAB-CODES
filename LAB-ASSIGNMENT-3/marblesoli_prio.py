import heapq

def is_goal(board):
    return sum(row.count(1) for row in board) == 1 and board[3][3] == 1

def gen_moves(board):
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

def board_to_tuple(board):
    """Helper function to convert board to a tuple of tuples to make it hashable."""
    return tuple(tuple(row) for row in board)

def priority_queue_search(initial_board, max_depth=50):
    pq = []
    visited = set()
    
    heapq.heappush(pq, (0, initial_board, []))
    visited.add(board_to_tuple(initial_board))
    
    depth = 0
    while pq:
        path_cost, board, moves = heapq.heappop(pq)
        depth = len(moves)
        
        print(f"Current depth: {depth}, Queue size: {len(pq)}")
        
        if is_goal(board):
            return moves
        
        if depth >= max_depth:
            print("Reached max depth limit, stopping.")
            break
        
        for n_board in gen_moves(board):
            n_board_tuple = board_to_tuple(n_board)
            if n_board_tuple not in visited:
                visited.add(n_board_tuple)
                new_moves = moves + [n_board]
                heapq.heappush(pq, (path_cost + 1, n_board, new_moves))

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

moves = priority_queue_search(initial_board, max_depth=50)
print(f"Moves to solve: {len(moves) if moves else 'No solution'}")