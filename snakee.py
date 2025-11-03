import random
import tkinter as tk


CELL_SIZE = 20
GRID_W, GRID_H = 20, 20
SPEED_START_MS = 120
SPEED_MIN_MS = 60
SPEED_UP_EVERY = 5
HUD_HEIGHT = 40

COLOR_BG = "#111"
COLOR_GRID = "#222"
COLOR_FOOD = "#e74c3c"
COLOR_BODY = "#2ecc71"
COLOR_HEAD = "#27ae60"
COLOR_OVERLAY = "#000"
COLOR_TEXT = "#fff"

class SnakeGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Snake — Python/tkinter demo")
        root.resizable(False, False)
        self.canvas = tk.Canvas(
            root,
            width=GRID_W * CELL_SIZE,
            height=GRID_H * CELL_SIZE,
            bg=COLOR_BG,
            highlightthickness=0,
        )
        self.canvas.pack()
        self.hud = tk.Label(
            root,
            text="Score: 0   Pause: [Space]   Restart: [R]",
            font=("Segoe UI", 12)
        )
        self.hud.pack(fill="x", ipady=5)
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.speed_ms = SPEED_START_MS
        self.score = 0
        self.paused = False
        self.game_over = False
        self.food = None
        self.snake = []
        root.bind("<Up>", lambda e: self.queue_dir(0, -1))
        root.bind("<Down>", lambda e: self.queue_dir(0, 1))
        root.bind("<Left>", lambda e: self.queue_dir(-1, 0))
        root.bind("<Right>", lambda e: self.queue_dir(1, 0))
        root.bind("<space>", self.toggle_pause)
        root.bind("<Key-r>", self.restart)
        self.reset_game()
        self.loop()

    def reset_game(self):
        self.canvas.delete("all")
        self._draw_grid()
        cx, cy = GRID_W // 2, GRID_H // 2
        self.snake = [(cx - 2, cy), (cx - 1, cy), (cx, cy)]
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.place_food()
        self.score = 0
        self.speed_ms = SPEED_START_MS
        self.paused = False
        self.game_over = False
        self._redraw()

    def queue_dir(self, dx: int, dy: int):
        if (dx, dy) == (-self.direction[0], -self.direction[1]):
            return
        self.pending_direction = (dx, dy)

    def toggle_pause(self, _=None):
        if self.game_over:
            return
        self.paused = not self.paused
        self._update_hud()

    def restart(self, _=None):
        self.reset_game()

    def place_food(self):
        occupied = set(self.snake)
        free = [(x, y) for x in range(GRID_W) for y in range(GRID_H)
                if (x, y) not in occupied]
        self.food = random.choice(free) if free else None

    def step(self):
        if self.game_over or self.paused:
            return

        self.direction = self.pending_direction
        dx, dy = self.direction

        head_x, head_y = self.snake[-1]
        new_head = (head_x + dx, head_y + dy)

        if not (0 <= new_head[0] < GRID_W and 0 <= new_head[1] < GRID_H):
            return self._end_game()

        if new_head in self.snake:
            return self._end_game()

        self.snake.append(new_head)

        if self.food and new_head == self.food:
            self.score += 1
            if self.score % SPEED_UP_EVERY == 0 and self.speed_ms > SPEED_MIN_MS:
                self.speed_ms = max(SPEED_MIN_MS, self.speed_ms - 10)
            self.place_food()
        else:
            self.snake.pop(0)

        self._redraw()

    def loop(self):
        self.step()
        self.root.after(self.speed_ms, self.loop)

    def _draw_grid(self):
        for x in range(GRID_W):
            self.canvas.create_line(
                x * CELL_SIZE, 0, x * CELL_SIZE, GRID_H * CELL_SIZE, fill=COLOR_GRID
            )
        for y in range(GRID_H):
            self.canvas.create_line(
                0, y * CELL_SIZE, GRID_W * CELL_SIZE, y * CELL_SIZE, fill=COLOR_GRID
            )

    def _update_hud(self):
        status = ""
        if self.paused:
            status = "Paused"
        if self.game_over:
            status = "Game Over — press [R] to restart"
        self.hud.config(text=f"Score: {self.score}   {status}")

    def _redraw(self):
        self.canvas.delete("snake")
        self.canvas.delete("food")


        if self.food:
            fx, fy = self.food
            self._rect(fx, fy, pad=2, fill=COLOR_FOOD, tags="food")

        for i, (x, y) in enumerate(self.snake):
            is_head = (i == len(self.snake) - 1)
            self._rect(x, y, pad=1, fill=(COLOR_HEAD if is_head else COLOR_BODY), tags="snake")

        self._update_hud()

    def _rect(self, gx: int, gy: int, pad: int, fill: str, tags: str):
        x1 = gx * CELL_SIZE + pad
        y1 = gy * CELL_SIZE + pad
        x2 = (gx + 1) * CELL_SIZE - pad
        y2 = (gy + 1) * CELL_SIZE - pad
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline="", tags=tags)

    def _end_game(self):
        self.game_over = True
        self._update_hud()

        self.canvas.create_rectangle(
            0, 0, GRID_W * CELL_SIZE, GRID_H * CELL_SIZE,
            fill=COLOR_OVERLAY, stipple="gray50", outline=""
        )
        self.canvas.create_text(
            GRID_W * CELL_SIZE // 2, GRID_H * CELL_SIZE // 2 - 10,
            text="GAME OVER", fill=COLOR_TEXT, font=("Segoe UI", 24, "bold")
        )
        self.canvas.create_text(
            GRID_W * CELL_SIZE // 2, GRID_H * CELL_SIZE // 2 + 20,
            text="Press R to start again",
            fill="#ddd", font=("Segoe UI", 12)

        )

def main():
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
