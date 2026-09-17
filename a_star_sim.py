import heapq
import sys
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
GRAY = (160, 160, 160)
DARK_GRAY = (80, 80, 80)
GREEN = (46, 204, 113)
RED = (231, 76, 60)
BLUE = (52, 152, 219)
CYAN = (26, 188, 156)
YELLOW = (241, 196, 15)
PURPLE = (155, 89, 182)
BG_PANEL = (40, 44, 52)
BG_GRID = (20, 20, 20)
TEXT_COLOR = (220, 224, 232)

pygame.init()
pygame.font.init()
FONT_SM = pygame.font.SysFont('Consolas', 12)
FONT_MD = pygame.font.SysFont('Consolas', 15, bold=True)

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def draw(self, win):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(win, color, self.rect, border_radius=4)
        text_surf = FONT_MD.render(self.text, True, WHITE)
        win.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2, 
                             self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def compute_astar_states(grid, cols, rows, start, end):
    states = []
    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}
    
    open_set_hash = {start}
    closed_set = set()

    def record_state(current, done=False, path=None):
        sorted_queue = sorted([(f, n) for f, c, n in open_set])
        states.append({
            'current': current,
            'open_set': sorted_queue,
            'closed_set': set(closed_set),
            'came_from': dict(came_from),
            'done': done,
            'path': path if path else []
        })

    record_state(start)

    while open_set:
        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == end:
            path = []
            curr = current
            while curr in came_from:
                path.append(curr)
                curr = came_from[curr]
            path.append(start)
            path.reverse()
            record_state(current, done=True, path=path)
            return states

        closed_set.add(current)

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            if not (0 <= neighbor[0] < cols and 0 <= neighbor[1] < rows):
                continue
            if grid[neighbor[1]][neighbor[0]] == 1:
                continue
            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1

            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, end)
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        record_state(current)

    record_state(current, done=True)
    return states

def draw_grid_lines(win, offset_x, offset_y, cell_size, cols, rows):
    for i in range(rows + 1):
        pygame.draw.line(win, GRAY, (offset_x, offset_y + i * cell_size), 
                         (offset_x + cols * cell_size, offset_y + i * cell_size))
    for j in range(cols + 1):
        pygame.draw.line(win, GRAY, (offset_x + j * cell_size, offset_y), 
                         (offset_x + j * cell_size, offset_y + rows * cell_size))

def main():
    win = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    screen_w, screen_h = win.get_size()
    
    panel_w = 440
    panel_x = screen_w - panel_w
    grid_area_w = panel_x

    cols = 25
    rows = 15
    start_node = (2, rows // 2)
    end_node = (cols - 3, rows // 2)

    grid = [[0 for _ in range(cols)] for _ in range(rows)]

    def calc_layout():
        cell_size = min(grid_area_w // cols, screen_h // rows)
        offset_x = (grid_area_w - (cols * cell_size)) // 2
        offset_y = (screen_h - (rows * cell_size)) // 2
        return cell_size, offset_x, offset_y

    cell_size, offset_x, offset_y = calc_layout()

    clock = pygame.time.Clock()
    states = compute_astar_states(grid, cols, rows, start_node, end_node)
    state_idx = 0
    auto_play = True
    last_update_time = pygame.time.get_ticks()
    update_delay = 100

    btn_play = Button(panel_x + 20, 230, 90, 28, "Pause", PURPLE, (175, 119, 200))
    btn_prev = Button(panel_x + 120, 230, 35, 28, "<", BLUE, (82, 172, 229))
    btn_next = Button(panel_x + 160, 230, 35, 28, ">", BLUE, (82, 172, 229))
    btn_reset = Button(panel_x + 205, 230, 90, 28, "Reset", RED, (241, 106, 90))

    btn_cols_dec = Button(panel_x + 100, 45, 25, 22, "-", DARK_GRAY, GRAY)
    btn_cols_inc = Button(panel_x + 165, 45, 25, 22, "+", DARK_GRAY, GRAY)
    btn_rows_dec = Button(panel_x + 280, 45, 25, 22, "-", DARK_GRAY, GRAY)
    btn_rows_inc = Button(panel_x + 345, 45, 25, 22, "+", DARK_GRAY, GRAY)

    btn_sx_dec = Button(panel_x + 100, 85, 25, 22, "-", DARK_GRAY, GRAY)
    btn_sx_inc = Button(panel_x + 165, 85, 25, 22, "+", DARK_GRAY, GRAY)
    btn_sy_dec = Button(panel_x + 280, 85, 25, 22, "-", DARK_GRAY, GRAY)
    btn_sy_inc = Button(panel_x + 345, 85, 25, 22, "+", DARK_GRAY, GRAY)

    btn_ex_dec = Button(panel_x + 100, 125, 25, 22, "-", DARK_GRAY, GRAY)
    btn_ex_inc = Button(panel_x + 165, 125, 25, 22, "+", DARK_GRAY, GRAY)
    btn_ey_dec = Button(panel_x + 280, 125, 25, 22, "-", DARK_GRAY, GRAY)
    btn_ey_inc = Button(panel_x + 345, 125, 25, 22, "+", DARK_GRAY, GRAY)

    def update_simulation(resize=False):
        nonlocal states, state_idx, grid, start_node, end_node, cell_size, offset_x, offset_y
        
        start_node = (max(0, min(start_node[0], cols - 1)), max(0, min(start_node[1], rows - 1)))
        end_node = (max(0, min(end_node[0], cols - 1)), max(0, min(end_node[1], rows - 1)))
        
        if resize:
            new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
            for r in range(min(len(grid), rows)):
                for c in range(min(len(grid[0]), cols)):
                    new_grid[r][c] = grid[r][c]
            grid = new_grid
            cell_size, offset_x, offset_y = calc_layout()

        grid[start_node[1]][start_node[0]] = 0
        grid[end_node[1]][end_node[0]] = 0

        states = compute_astar_states(grid, cols, rows, start_node, end_node)
        state_idx = 0

    running = True
    drawing_wall = False
    erasing_wall = False
    dragging_start = False
    dragging_end = False

    while running:
        win.fill(BG_GRID)
        pygame.draw.rect(win, BG_PANEL, (panel_x, 0, panel_w, screen_h))

        current_time = pygame.time.get_ticks()
        if auto_play and current_time - last_update_time > update_delay:
            if state_idx < len(states) - 1:
                state_idx += 1
            last_update_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if x < panel_x:
                    col = (x - offset_x) // cell_size
                    row = (y - offset_y) // cell_size
                    if 0 <= col < cols and 0 <= row < rows:
                        if event.button == 1:
                            if (col, row) == start_node:
                                dragging_start = True
                            elif (col, row) == end_node:
                                dragging_end = True
                            else:
                                grid[row][col] = 1
                                drawing_wall = True
                                update_simulation()
                        elif event.button == 3:
                            grid[row][col] = 0
                            erasing_wall = True
                            update_simulation()
                else:
                    if event.button == 1:
                        if btn_cols_dec.is_clicked((x, y)) and cols > 5:
                            cols -= 1
                            update_simulation(resize=True)
                        elif btn_cols_inc.is_clicked((x, y)) and cols < 60:
                            cols += 1
                            update_simulation(resize=True)
                        elif btn_rows_dec.is_clicked((x, y)) and rows > 5:
                            rows -= 1
                            update_simulation(resize=True)
                        elif btn_rows_inc.is_clicked((x, y)) and rows < 40:
                            rows += 1
                            update_simulation(resize=True)

                        elif btn_sx_dec.is_clicked((x, y)) and start_node[0] > 0:
                            start_node = (start_node[0] - 1, start_node[1])
                            update_simulation()
                        elif btn_sx_inc.is_clicked((x, y)) and start_node[0] < cols - 1:
                            start_node = (start_node[0] + 1, start_node[1])
                            update_simulation()
                        elif btn_sy_dec.is_clicked((x, y)) and start_node[1] > 0:
                            start_node = (start_node[0], start_node[1] - 1)
                            update_simulation()
                        elif btn_sy_inc.is_clicked((x, y)) and start_node[1] < rows - 1:
                            start_node = (start_node[0], start_node[1] + 1)
                            update_simulation()

                        elif btn_ex_dec.is_clicked((x, y)) and end_node[0] > 0:
                            end_node = (end_node[0] - 1, end_node[1])
                            update_simulation()
                        elif btn_ex_inc.is_clicked((x, y)) and end_node[0] < cols - 1:
                            end_node = (end_node[0] + 1, end_node[1])
                            update_simulation()
                        elif btn_ey_dec.is_clicked((x, y)) and end_node[1] > 0:
                            end_node = (end_node[0], end_node[1] - 1)
                            update_simulation()
                        elif btn_ey_inc.is_clicked((x, y)) and end_node[1] < rows - 1:
                            end_node = (end_node[0], end_node[1] + 1)
                            update_simulation()

                        elif btn_play.is_clicked((x, y)):
                            auto_play = not auto_play
                            btn_play.text = "Pause" if auto_play else "Play"
                        elif btn_prev.is_clicked((x, y)) and state_idx > 0:
                            auto_play = False
                            btn_play.text = "Play"
                            state_idx -= 1
                        elif btn_next.is_clicked((x, y)) and state_idx < len(states) - 1:
                            auto_play = False
                            btn_play.text = "Play"
                            state_idx += 1
                        elif btn_reset.is_clicked((x, y)):
                            grid = [[0 for _ in range(cols)] for _ in range(rows)]
                            update_simulation()

            if event.type == pygame.MOUSEBUTTONUP:
                drawing_wall = False
                erasing_wall = False
                dragging_start = False
                dragging_end = False

            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                if x < panel_x:
                    col = (x - offset_x) // cell_size
                    row = (y - offset_y) // cell_size
                    if 0 <= col < cols and 0 <= row < rows:
                        if dragging_start and (col, row) != end_node:
                            start_node = (col, row)
                            update_simulation()
                        elif dragging_end and (col, row) != start_node:
                            end_node = (col, row)
                            update_simulation()
                        elif drawing_wall and (col, row) != start_node and (col, row) != end_node:
                            grid[row][col] = 1
                            update_simulation()
                        elif erasing_wall:
                            grid[row][col] = 0
                            update_simulation()

        current_state = states[state_idx]

        for node in current_state['closed_set']:
            pygame.draw.rect(win, BLUE, (offset_x + node[0] * cell_size, offset_y + node[1] * cell_size, cell_size, cell_size))
        for f, node in current_state['open_set']:
            pygame.draw.rect(win, CYAN, (offset_x + node[0] * cell_size, offset_y + node[1] * cell_size, cell_size, cell_size))
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    pygame.draw.rect(win, BLACK, (offset_x + c * cell_size, offset_y + r * cell_size, cell_size, cell_size))

        pygame.draw.rect(win, GREEN, (offset_x + start_node[0] * cell_size, offset_y + start_node[1] * cell_size, cell_size, cell_size))
        pygame.draw.rect(win, RED, (offset_x + end_node[0] * cell_size, offset_y + end_node[1] * cell_size, cell_size, cell_size))

        if not current_state['done']:
            curr = current_state['current']
            pygame.draw.rect(win, PURPLE, (offset_x + curr[0] * cell_size, offset_y + curr[1] * cell_size, cell_size, cell_size))

        if current_state['path']:
            for node in current_state['path']:
                if node != start_node and node != end_node:
                    pygame.draw.rect(win, YELLOW, (offset_x + node[0] * cell_size, offset_y + node[1] * cell_size, cell_size, cell_size))

        draw_grid_lines(win, offset_x, offset_y, cell_size, cols, rows)

        title = FONT_MD.render(f"Control Panel (Step {state_idx}/{len(states)-1})", True, TEXT_COLOR)
        win.blit(title, (panel_x + 20, 15))

        win.blit(FONT_SM.render("Cols:", True, TEXT_COLOR), (panel_x + 20, 50))
        win.blit(FONT_SM.render(f"{cols}", True, YELLOW), (panel_x + 135, 50))
        btn_cols_dec.draw(win)
        btn_cols_inc.draw(win)

        win.blit(FONT_SM.render("Rows:", True, TEXT_COLOR), (panel_x + 210, 50))
        win.blit(FONT_SM.render(f"{rows}", True, YELLOW), (panel_x + 315, 50))
        btn_rows_dec.draw(win)
        btn_rows_inc.draw(win)

        win.blit(FONT_SM.render("Start X:", True, GREEN), (panel_x + 20, 90))
        win.blit(FONT_SM.render(f"{start_node[0]}", True, TEXT_COLOR), (panel_x + 135, 90))
        btn_sx_dec.draw(win)
        btn_sx_inc.draw(win)

        win.blit(FONT_SM.render("Start Y:", True, GREEN), (panel_x + 210, 90))
        win.blit(FONT_SM.render(f"{start_node[1]}", True, TEXT_COLOR), (panel_x + 315, 90))
        btn_sy_dec.draw(win)
        btn_sy_inc.draw(win)

        win.blit(FONT_SM.render("End X:", True, RED), (panel_x + 20, 130))
        win.blit(FONT_SM.render(f"{end_node[0]}", True, TEXT_COLOR), (panel_x + 135, 130))
        btn_ex_dec.draw(win)
        btn_ex_inc.draw(win)

        win.blit(FONT_SM.render("End Y:", True, RED), (panel_x + 210, 130))
        win.blit(FONT_SM.render(f"{end_node[1]}", True, TEXT_COLOR), (panel_x + 315, 130))
        btn_ey_dec.draw(win)
        btn_ey_inc.draw(win)

        win.blit(FONT_SM.render("Left Click: Draw Wall / Drag Green & Red", True, GRAY), (panel_x + 20, 170))
        win.blit(FONT_SM.render("Right Click: Erase Wall | ESC: Quit", True, GRAY), (panel_x + 20, 190))

        btn_play.draw(win)
        btn_prev.draw(win)
        btn_next.draw(win)
        btn_reset.draw(win)

        pygame.draw.line(win, DARK_GRAY, (panel_x + 20, 275), (screen_w - 20, 275), 2)

        win.blit(FONT_MD.render("Queue (Open Set) - Sorted by f_score", True, CYAN), (panel_x + 20, 290))
        win.blit(FONT_SM.render(f"Current node: {current_state['current']} (Purple)", True, PURPLE), (panel_x + 20, 315))

        y_offset = 340
        max_display = (screen_h - y_offset - 20) // 16
        for i, (f_score, node) in enumerate(current_state['open_set'][:max_display]):
            txt = f"[{i+1}] Node {node} | f = {f_score}"
            win.blit(FONT_SM.render(txt, True, TEXT_COLOR), (panel_x + 20, y_offset))
            y_offset += 16

        if len(current_state['open_set']) > max_display:
            win.blit(FONT_SM.render(f"... and {len(current_state['open_set']) - max_display} more", True, GRAY), (panel_x + 20, y_offset))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
