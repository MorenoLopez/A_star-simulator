import pygame
import sys

# --- Colors ---
COLOR_BG = (20, 20, 20)          # #141414
COLOR_PANEL = (40, 44, 52)       # #282c34
COLOR_TEXT = (220, 224, 232)     # #dce0e8
COLOR_GRID_LINE = (160, 160, 160)# #a0a0a0
COLOR_WALL = (30, 30, 30)        # #1e1e1e
COLOR_START = (46, 204, 113)     # #2ecc71 (Green)
COLOR_END = (231, 76, 60)        # #e74c3c (Red)
COLOR_CURRENT = (155, 89, 182)   # #9b59b6 (Purple)
COLOR_CLOSED = (52, 152, 219)    # #3498db (Blue)
COLOR_OPEN = (26, 188, 156)      # #1abc9c (Teal)
COLOR_PATH = (241, 196, 15)      # #f1c40f (Yellow)
COLOR_BTN_BLUE = (52, 152, 219)
COLOR_BTN_PURPLE = (155, 89, 182)
COLOR_BTN_RED = (231, 76, 60)
COLOR_INPUT_BG = (20, 20, 20)
COLOR_INPUT_BORDER = (80, 80, 80)
COLOR_INPUT_ACTIVE = (241, 196, 15)

ALGORITHMS = [
    ("a_star", "A* Search"),
    ("dijkstra", "Dijkstra Algorithm"),
    ("greedy", "Greedy Best-First"),
    ("bfs", "Breadth-First Search (BFS)"),
    ("dfs", "Depth-First Search (DFS)")
]

def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def compute_algorithm_states(grid, cols, rows, start_node, end_node, algo_key):
    states_list = []
    count = 0

    start_key = f"{start_node[0]},{start_node[1]}"
    end_key = f"{end_node[0]},{end_node[1]}"

    g_score = {start_key: 0}
    came_from = {}

    h_start = heuristic(start_node, end_node)
    start_item = {'pos': start_node, 'g': 0, 'h': h_start, 'count': count}
    count += 1

    if algo_key == 'a_star':
        start_item['f'] = h_start
    elif algo_key == 'dijkstra':
        start_item['f'] = 0
    elif algo_key == 'greedy':
        start_item['f'] = h_start

    open_list = [start_item]
    visited = set()
    open_keys = {start_key}

    def record_state(current, done=False, path=None):
        if path is None:
            path = []
        if algo_key in ['a_star', 'dijkstra', 'greedy']:
            display_list = sorted(open_list, key=lambda x: (x.get('f', 0), x['count']))
        else:
            display_list = list(open_list)

        states_list.append({
            'current': current,
            'open_list': [{'pos': item['pos'], 'f': item.get('f')} for item in display_list],
            'closed_set': set(visited),
            'done': done,
            'path': path
        })

    record_state(start_node)

    while len(open_list) > 0:
        if algo_key in ['a_star', 'dijkstra', 'greedy']:
            open_list.sort(key=lambda x: (x.get('f', 0), x['count']))
            current_obj = open_list.pop(0)
        elif algo_key == 'bfs':
            current_obj = open_list.pop(0)
        elif algo_key == 'dfs':
            current_obj = open_list.pop()

        current = current_obj['pos']
        current_key = f"{current[0]},{current[1]}"
        open_keys.discard(current_key)

        if current_key in visited:
            continue
        visited.add(current_key)

        if current[0] == end_node[0] and current[1] == end_node[1]:
            path = []
            curr_k = current_key
            while curr_k in came_from:
                parts = list(map(int, curr_k.split(',')))
                path.append(parts)
                curr_k = came_from[curr_k]
            path.append(start_node)
            path.reverse()
            record_state(current, done=True, path=path)
            return states_list

        neighbors = [
            (current[0], current[1] + 1),
            (current[0] + 1, current[1]),
            (current[0], current[1] - 1),
            (current[0] - 1, current[1])
        ]

        for nx, ny in neighbors:
            if nx < 0 or nx >= cols or ny < 0 or ny >= rows:
                continue
            if grid[ny][nx] == 1:
                continue
            neighbor_key = f"{nx},{ny}"
            if neighbor_key in visited:
                continue

            if algo_key in ['a_star', 'dijkstra', 'greedy']:
                tentative_g = g_score.get(current_key, 0) + 1
                current_g = g_score.get(neighbor_key, float('inf'))

                if tentative_g < current_g:
                    came_from[neighbor_key] = current_key
                    g_score[neighbor_key] = tentative_g
                    h_val = heuristic((nx, ny), end_node)
                    
                    if algo_key == 'a_star':
                        f_val = tentative_g + h_val
                    elif algo_key == 'dijkstra':
                        f_val = tentative_g
                    elif algo_key == 'greedy':
                        f_val = h_val

                    existing = next((item for item in open_list if item['pos'] == [nx, ny]), None)
                    if existing:
                        existing['f'] = f_val
                        existing['g'] = tentative_g
                    else:
                        open_list.append({'pos': [nx, ny], 'f': f_val, 'g': tentative_g, 'h': h_val, 'count': count})
                        count += 1
                        open_keys.add(neighbor_key)
            else:
                if neighbor_key not in open_keys:
                    came_from[neighbor_key] = current_key
                    open_list.append({'pos': [nx, ny], 'count': count})
                    count += 1
                    open_keys.add(neighbor_key)

        record_state(current)

    record_state(start_node, done=True, path=[])
    return states_list

# --- Composant Menu Déroulant (Dropdown) ---
class Dropdown:
    def __init__(self, x, y, w, h, options, selected_idx=0):
        self.rect = pygame.Rect(x, y, w, h)
        self.options = options  # Liste de tuples (key, label)
        self.selected_idx = selected_idx
        self.is_open = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_open:
                # Vérifier si clic sur une option de la liste déroulée
                for idx in range(len(self.options)):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (idx + 1) * self.rect.h, self.rect.w, self.rect.h)
                    if option_rect.collidepoint(event.pos):
                        self.selected_idx = idx
                        self.is_open = False
                        return True
                self.is_open = False
                return False
            else:
                if self.rect.collidepoint(event.pos):
                    self.is_open = True
                    return False
        return False

    def draw(self, surface, font):
        # Case principale
        pygame.draw.rect(surface, COLOR_INPUT_BG, self.rect, border_radius=4)
        border_col = COLOR_INPUT_ACTIVE if self.is_open else COLOR_BTN_BLUE
        pygame.draw.rect(surface, border_col, self.rect, width=1, border_radius=4)

        selected_label = self.options[self.selected_idx][1]
        txt_surf = font.render(selected_label, True, COLOR_INPUT_ACTIVE)
        surface.blit(txt_surf, (self.rect.x + 8, self.rect.y + (self.rect.h - txt_surf.get_height()) // 2))

        # Flèche du menu
        arrow = "▲" if self.is_open else "▼"
        arrow_surf = font.render(arrow, True, COLOR_TEXT)
        surface.blit(arrow_surf, (self.rect.x + self.rect.w - 18, self.rect.y + (self.rect.h - arrow_surf.get_height()) // 2))

        # Affichage des options si le menu est ouvert
        if self.is_open:
            for idx, (_, label) in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (idx + 1) * self.rect.h, self.rect.w, self.rect.h)
                mouse_pos = pygame.mouse.get_pos()
                is_hovered = opt_rect.collidepoint(mouse_pos)

                bg_color = (50, 55, 65) if is_hovered else COLOR_PANEL
                if idx == self.selected_idx:
                    bg_color = (30, 80, 130)

                pygame.draw.rect(surface, bg_color, opt_rect)
                pygame.draw.rect(surface, (80, 80, 80), opt_rect, width=1)

                opt_txt = font.render(label, True, COLOR_INPUT_ACTIVE if idx == self.selected_idx else COLOR_TEXT)
                surface.blit(opt_txt, (opt_rect.x + 8, opt_rect.y + (opt_rect.h - opt_txt.get_height()) // 2))

# --- Champs de Saisie / Boutons ---
class InputBox:
    def __init__(self, x, y, w, h, text='', min_val=0, max_val=100):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = str(text)
        self.active = False
        self.min_val = min_val
        self.max_val = max_val

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            return False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                return True
            elif event.unicode.isdigit():
                if len(self.text) < 3:
                    self.text += event.unicode
                    return True
        return False

    def get_value(self, default):
        try:
            val = int(self.text)
            return max(self.min_val, min(val, self.max_val))
        except ValueError:
            return default

    def set_value(self, val):
        self.text = str(val)

    def draw(self, surface, font):
        color = COLOR_INPUT_ACTIVE if self.active else COLOR_INPUT_BORDER
        pygame.draw.rect(surface, COLOR_INPUT_BG, self.rect)
        pygame.draw.rect(surface, color, self.rect, 1, border_radius=3)
        txt_surface = font.render(self.text, True, COLOR_INPUT_ACTIVE if self.active else COLOR_TEXT)
        surface.blit(txt_surface, (self.rect.x + (self.rect.w - txt_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.h - txt_surface.get_height()) // 2))

class Button:
    def __init__(self, x, y, w, h, text, color, hover_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        col = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=4)
        txt = font.render(self.text, True, (255, 255, 255))
        surface.blit(txt, (self.rect.x + (self.rect.w - txt.get_width()) // 2,
                           self.rect.y + (self.rect.h - txt.get_height()) // 2))

# --- Application Principale ---
class PathfindingVisualizer:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pathfinding Visualizer (Pygame)")

        self.window_width = 1280
        self.window_height = 720
        self.panel_width = 440

        self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 14)
        self.font_bold = pygame.font.SysFont("Consolas", 15, bold=True)
        self.font_title = pygame.font.SysFont("Consolas", 18, bold=True)

        self.cols = 25
        self.rows = 15
        self.start_node = [2, 7]
        self.end_node = [22, 7]
        self.algo_idx = 0

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.states = []
        self.state_idx = 0
        self.auto_play = False
        self.last_update = 0
        self.update_delay = 80

        self.drawing_wall = False
        self.erasing_wall = False
        self.dragging_start = False
        self.dragging_end = False

        self.setup_ui_elements()
        self.update_simulation(resize_grid=True)

    def setup_ui_elements(self):
        px = self.window_width - self.panel_width + 20

        # Menu déroulant pour le choix des algorithmes
        self.dropdown_algo = Dropdown(px + 100, 48, 300, 28, ALGORITHMS, self.algo_idx)

        self.input_cols = InputBox(px + 60, 90, 60, 24, self.cols, 5, 60)
        self.input_rows = InputBox(px + 230, 90, 60, 24, self.rows, 5, 40)

        self.input_sx = InputBox(px + 80, 125, 50, 24, self.start_node[0], 0, self.cols - 1)
        self.input_sy = InputBox(px + 250, 125, 50, 24, self.start_node[1], 0, self.rows - 1)

        self.input_ex = InputBox(px + 80, 160, 50, 24, self.end_node[0], 0, self.cols - 1)
        self.input_ey = InputBox(px + 250, 160, 50, 24, self.end_node[1], 0, self.rows - 1)

        self.btn_play = Button(px, 220, 140, 32, "Play", COLOR_BTN_PURPLE, (175, 122, 197))
        self.btn_prev = Button(px + 150, 220, 45, 32, "<", COLOR_BTN_BLUE, (93, 173, 226))
        self.btn_next = Button(px + 200, 220, 45, 32, ">", COLOR_BTN_BLUE, (93, 173, 226))
        self.btn_reset = Button(px + 255, 220, 140, 32, "Reset", COLOR_BTN_RED, (236, 112, 99))

        self.inputs = [self.input_cols, self.input_rows, self.input_sx, self.input_sy, self.input_ex, self.input_ey]

    def update_simulation(self, resize_grid=False):
        if resize_grid:
            new_grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
            for r in range(min(len(self.grid), self.rows)):
                for c in range(min(len(self.grid[0]), self.cols)):
                    new_grid[r][c] = self.grid[r][c]
            self.grid = new_grid

        self.start_node = [max(0, min(self.start_node[0], self.cols - 1)), max(0, min(self.start_node[1], self.rows - 1))]
        self.end_node = [max(0, min(self.end_node[0], self.cols - 1)), max(0, min(self.end_node[1], self.rows - 1))]

        self.grid[self.start_node[1]][self.start_node[0]] = 0
        self.grid[self.end_node[1]][self.end_node[0]] = 0

        self.states = compute_algorithm_states(
            self.grid, self.cols, self.rows, self.start_node, self.end_node, ALGORITHMS[self.algo_idx][0]
        )
        self.state_idx = 0
        self.auto_play = False
        self.btn_play.text = "Play"
        self.sync_input_fields()

    def sync_input_fields(self):
        self.input_cols.set_value(self.cols)
        self.input_rows.set_value(self.rows)
        self.input_sx.set_value(self.start_node[0])
        self.input_sy.set_value(self.start_node[1])
        self.input_ex.set_value(self.end_node[0])
        self.input_ey.set_value(self.end_node[1])

        self.input_sx.max_val = self.cols - 1
        self.input_ex.max_val = self.cols - 1
        self.input_sy.max_val = self.rows - 1
        self.input_ey.max_val = self.rows - 1

    def handle_inputs_change(self):
        c = self.input_cols.get_value(self.cols)
        r = self.input_rows.get_value(self.rows)
        sx = self.input_sx.get_value(self.start_node[0])
        sy = self.input_sy.get_value(self.start_node[1])
        ex = self.input_ex.get_value(self.end_node[0])
        ey = self.input_ey.get_value(self.end_node[1])

        resize = (c != self.cols or r != self.rows)
        self.cols, self.rows = c, r
        self.start_node = [sx, sy]
        self.end_node = [ex, ey]

        self.setup_ui_elements()
        self.update_simulation(resize_grid=resize)

    def run(self):
        while True:
            current_time = pygame.time.get_ticks()

            if self.auto_play and current_time - self.last_update > self.update_delay:
                if self.state_idx < len(self.states) - 1:
                    self.state_idx += 1
                else:
                    self.auto_play = False
                    self.btn_play.text = "Play"
                self.last_update = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.VIDEORESIZE:
                    self.window_width, self.window_height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.window_width, self.window_height), pygame.RESIZABLE)
                    self.setup_ui_elements()

                # Event du Menu Déroulant
                if self.dropdown_algo.handle_event(event):
                    self.algo_idx = self.dropdown_algo.selected_idx
                    self.update_simulation()
                    continue

                # Si le dropdown est ouvert, ignorer les autres clics
                if self.dropdown_algo.is_open:
                    continue

                # Event des champs de texte
                input_changed = False
                for inp in self.inputs:
                    if inp.handle_event(event):
                        input_changed = True
                if input_changed:
                    self.handle_inputs_change()

                # Event des Boutons Action
                if self.btn_play.is_clicked(event):
                    if self.state_idx >= len(self.states) - 1:
                        self.state_idx = 0
                    self.auto_play = not self.auto_play
                    self.btn_play.text = "Pause" if self.auto_play else "Play"

                if self.btn_prev.is_clicked(event):
                    if self.state_idx > 0:
                        self.auto_play = False
                        self.btn_play.text = "Play"
                        self.state_idx -= 1

                if self.btn_next.is_clicked(event):
                    if self.state_idx < len(self.states) - 1:
                        self.auto_play = False
                        self.btn_play.text = "Play"
                        self.state_idx += 1

                if self.btn_reset.is_clicked(event):
                    self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
                    self.update_simulation()

                # Raccourcis clavier
                if event.type == pygame.KEYDOWN and not any(inp.active for inp in self.inputs):
                    if event.key == pygame.K_SPACE:
                        if self.state_idx >= len(self.states) - 1:
                            self.state_idx = 0
                        self.auto_play = not self.auto_play
                        self.btn_play.text = "Pause" if self.auto_play else "Play"
                    elif event.key == pygame.K_LEFT and self.state_idx > 0:
                        self.auto_play = False
                        self.btn_play.text = "Play"
                        self.state_idx -= 1
                    elif event.key == pygame.K_RIGHT and self.state_idx < len(self.states) - 1:
                        self.auto_play = False
                        self.btn_play.text = "Play"
                        self.state_idx += 1
                    elif event.key == pygame.K_r:
                        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
                        self.update_simulation()

                # Interaction Grille
                self.handle_grid_mouse(event)

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_grid_mouse(self, event):
        canvas_w = self.window_width - self.panel_width
        canvas_h = self.window_height

        cell_size = min(canvas_w // self.cols, canvas_h // self.rows)
        offset_x = (canvas_w - (self.cols * cell_size)) // 2
        offset_y = (canvas_h - (self.rows * cell_size)) // 2

        mx, my = pygame.mouse.get_pos()
        col = (mx - offset_x) // cell_size
        row = (my - offset_y) // cell_size

        if event.type == pygame.MOUSEBUTTONDOWN and mx < canvas_w:
            if 0 <= col < self.cols and 0 <= row < self.rows:
                if event.button == 1:
                    if col == self.start_node[0] and row == self.start_node[1]:
                        self.dragging_start = True
                    elif col == self.end_node[0] and row == self.end_node[1]:
                        self.dragging_end = True
                    else:
                        self.grid[row][col] = 1
                        self.drawing_wall = True
                        self.update_simulation()
                elif event.button == 3:
                    self.grid[row][col] = 0
                    self.erasing_wall = True
                    self.update_simulation()

        elif event.type == pygame.MOUSEMOTION:
            if 0 <= col < self.cols and 0 <= row < self.rows:
                if self.dragging_start and (col != self.end_node[0] or row != self.end_node[1]):
                    self.start_node = [col, row]
                    self.update_simulation()
                elif self.dragging_end and (col != self.start_node[0] or row != self.start_node[1]):
                    self.end_node = [col, row]
                    self.update_simulation()
                elif self.drawing_wall and (col != self.start_node[0] or row != self.start_node[1]) and (col != self.end_node[0] or row != self.end_node[1]):
                    self.grid[row][col] = 1
                    self.update_simulation()
                elif self.erasing_wall:
                    self.grid[row][col] = 0
                    self.update_simulation()

        elif event.type == pygame.MOUSEBUTTONUP:
            self.drawing_wall = False
            self.erasing_wall = False
            self.dragging_start = False
            self.dragging_end = False

    def draw(self):
        self.screen.fill(COLOR_BG)

        # 1. Dessiner la Grille
        canvas_w = self.window_width - self.panel_width
        canvas_h = self.window_height

        cell_size = min(canvas_w // self.cols, canvas_h // self.rows)
        offset_x = (canvas_w - (self.cols * cell_size)) // 2
        offset_y = (canvas_h - (self.rows * cell_size)) // 2

        if self.states:
            curr_state = self.states[self.state_idx]

            # Closed Set
            for key in curr_state['closed_set']:
                x, y = map(int, key.split(','))
                pygame.draw.rect(self.screen, COLOR_CLOSED, (offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size))

            # Open Set
            for item in curr_state['open_list']:
                x, y = item['pos']
                pygame.draw.rect(self.screen, COLOR_OPEN, (offset_x + x * cell_size, offset_y + y * cell_size, cell_size, cell_size))

            # Murs
            for r in range(self.rows):
                for c in range(self.cols):
                    if self.grid[r][c] == 1:
                        pygame.draw.rect(self.screen, COLOR_WALL, (offset_x + c * cell_size, offset_y + r * cell_size, cell_size, cell_size))

            # Start & End
            pygame.draw.rect(self.screen, COLOR_START, (offset_x + self.start_node[0] * cell_size, offset_y + self.start_node[1] * cell_size, cell_size, cell_size))
            pygame.draw.rect(self.screen, COLOR_END, (offset_x + self.end_node[0] * cell_size, offset_y + self.end_node[1] * cell_size, cell_size, cell_size))

            # Nœud courant
            if not curr_state['done']:
                cx, cy = curr_state['current']
                pygame.draw.rect(self.screen, COLOR_CURRENT, (offset_x + cx * cell_size, offset_y + cy * cell_size, cell_size, cell_size))

            # Chemin final
            if curr_state['path']:
                for node in curr_state['path']:
                    if node != self.start_node and node != self.end_node:
                        pygame.draw.rect(self.screen, COLOR_PATH, (offset_x + node[0] * cell_size, offset_y + node[1] * cell_size, cell_size, cell_size))

        # Lignes de grille
        for i in range(self.rows + 1):
            pygame.draw.line(self.screen, COLOR_GRID_LINE, (offset_x, offset_y + i * cell_size), (offset_x + self.cols * cell_size, offset_y + i * cell_size))
        for j in range(self.cols + 1):
            pygame.draw.line(self.screen, COLOR_GRID_LINE, (offset_x + j * cell_size, offset_y), (offset_x + j * cell_size, offset_y + self.rows * cell_size))

        # 2. Panneau latéral
        px = self.window_width - self.panel_width
        pygame.draw.rect(self.screen, COLOR_PANEL, (px, 0, self.panel_width, self.window_height))

        # Titre
        step_txt = f"Control Panel (Step {self.state_idx}/{len(self.states) - 1 if self.states else 0})"
        self.screen.blit(self.font_title.render(step_txt, True, COLOR_TEXT), (px + 20, 15))

        # Labels et inputs
        self.screen.blit(self.font.render("Algorithm:", True, COLOR_TEXT), (px + 20, 53))

        self.screen.blit(self.font.render("Cols:", True, COLOR_TEXT), (px + 20, 95))
        self.input_cols.draw(self.screen, self.font)
        self.screen.blit(self.font.render("Rows:", True, COLOR_TEXT), (px + 180, 95))
        self.input_rows.draw(self.screen, self.font)

        self.screen.blit(self.font.render("Start X:", True, COLOR_START), (px + 20, 130))
        self.input_sx.draw(self.screen, self.font)
        self.screen.blit(self.font.render("Start Y:", True, COLOR_START), (px + 180, 130))
        self.input_sy.draw(self.screen, self.font)

        self.screen.blit(self.font.render("End X:", True, COLOR_END), (px + 20, 165))
        self.input_ex.draw(self.screen, self.font)
        self.screen.blit(self.font.render("End Y:", True, COLOR_END), (px + 180, 165))
        self.input_ey.draw(self.screen, self.font)

        # Boutons
        self.btn_play.draw(self.screen, self.font_bold)
        self.btn_prev.draw(self.screen, self.font_bold)
        self.btn_next.draw(self.screen, self.font_bold)
        self.btn_reset.draw(self.screen, self.font_bold)

        # Instructions
        inst1 = self.font.render("Left Click: Draw Wall / Drag Start & End", True, (160, 160, 160))
        inst2 = self.font.render("Right Click: Erase Wall | Space: Play/Pause", True, (160, 160, 160))
        self.screen.blit(inst1, (px + 20, 265))
        self.screen.blit(inst2, (px + 20, 285))

        pygame.draw.line(self.screen, (80, 80, 80), (px + 20, 310), (px + self.panel_width - 20, 310), 2)

        # Inspecteur de Structure
        algo_key = ALGORITHMS[self.algo_idx][0]
        titles = {
            'a_star': 'Queue (Open Set) - Sorted by f_score',
            'dijkstra': 'Queue (Open Set) - Sorted by g_score',
            'greedy': 'Queue (Open Set) - Sorted by h_score',
            'bfs': 'Queue (FIFO)',
            'dfs': 'Stack (LIFO)'
        }
        self.screen.blit(self.font_bold.render(titles[algo_key], True, COLOR_OPEN), (px + 20, 325))

        if self.states:
            curr_st = self.states[self.state_idx]
            curr_node_txt = f"Current node: ({curr_st['current'][0]}, {curr_st['current'][1]}) (Purple)"
            self.screen.blit(self.font.render(curr_node_txt, True, COLOR_CURRENT), (px + 20, 350))

            start_y = 380
            for idx, item in enumerate(curr_st['open_list'][:18]):
                score_str = f" | f = {item['f']}" if item['f'] is not None else ""
                q_txt = f"[{idx + 1}] Node ({item['pos'][0]}, {item['pos'][1]}){score_str}"
                self.screen.blit(self.font.render(q_txt, True, COLOR_TEXT), (px + 20, start_y + idx * 18))

        # Rendre le Dropdown EN DERNIER pour qu'il apparaisse au-dessus des autres éléments s'il est ouvert
        self.dropdown_algo.draw(self.screen, self.font)

if __name__ == "__main__":
    app = PathfindingVisualizer()
    app.run()
