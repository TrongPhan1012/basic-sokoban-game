from src.state import State
from src.state import DIRS

g_goals = set()

def get_next_states(state, walls):
    px, py = state.player
    for dx, dy in DIRS:
        nx, ny = px + dx, py + dy

        if (nx, ny) in walls:
            continue

        # Nếu di chuyển vào 1 thùng
        if (nx, ny) in state.boxes:
            bx, by = nx + dx, ny + dy
            if (bx, by) in walls or (bx, by) in state.boxes:
                continue
            if is_deadlock((bx, by), walls):
                continue
            new_boxes = set(state.boxes)
            new_boxes.remove((nx, ny))
            new_boxes.add((bx, by))
            yield State((nx, ny), new_boxes)
        else:
            yield State((nx, ny), state.boxes)

def is_goal(state):
    return all(box in g_goals for box in state.boxes)

def is_deadlock(box_pos, walls):
    bx, by = box_pos
    if box_pos in g_goals:
        return False
    # Box bị kẹt ở góc
    if (bx - 1, by) in walls and (bx, by - 1) in walls:
        return True
    if (bx - 1, by) in walls and (bx, by + 1) in walls:
        return True
    if (bx + 1, by) in walls and (bx, by - 1) in walls:
        return True
    if (bx + 1, by) in walls and (bx, by + 1) in walls:
        return True
    return False

def dfs_lazy(start_state, walls, goals):
    global g_goals
    g_goals = goals

    visited = set([start_state])
    stack = [(start_state, get_next_states(start_state, walls), [start_state])]

    while stack:
        state, children, path = stack[-1]  # Xem đỉnh stack

        # Nếu là goal, trả kết quả
        if is_goal(state):
            return path

        try:
            # Lazy expansion: chỉ lấy 1 state con khi cần
            next_state = next(children)
            if next_state not in visited:
                visited.add(next_state)
                stack.append((next_state, get_next_states(next_state, walls), path + [next_state]))
        except StopIteration:
            # Hết con để duyệt → backtrack
            stack.pop()

    return None
