import tkinter as tk
import random

class CatchTheBallGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Catch the Ball Game")

        self.canvas = tk.Canvas(root, width=600, height=400, bg="lightblue")
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(250, 360, 350, 380, fill="darkblue")
        self.ball = self.canvas.create_oval(290, 40, 310, 60, fill="red")

        self.ball_dx = random.choice([-4, 4])  # Ball's horizontal speed
        self.ball_dy = 3  # Ball's vertical speed

        self.score = 0
        self.lives = 3
        self.score_text = self.canvas.create_text(50, 20, text=f"Score: {self.score}", font=("Arial", 14), fill="black")
        self.lives_text = self.canvas.create_text(550, 20, text=f"Lives: {self.lives}", font=("Arial", 14), fill="black")

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.game_running = True
        self.update_game()

    def update_game(self):
        if not self.game_running:
            return

        # Move the ball
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        ball_coords = self.canvas.coords(self.ball)

        # Bounce off walls
        if ball_coords[0] <= 0 or ball_coords[2] >= 600:
            self.ball_dx *= -1

        # Check for collision with paddle
        if self.check_collision(ball_coords):
            self.ball_dy *= -1
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        # Ball falls out of bounds
        if ball_coords[3] >= 400:
            self.lives -= 1
            self.canvas.itemconfig(self.lives_text, text=f"Lives: {self.lives}")
            self.reset_ball()
            if self.lives == 0:
                self.game_over()

        self.canvas.after(20, self.update_game)

    def check_collision(self, ball_coords):
        paddle_coords = self.canvas.coords(self.paddle)
        if paddle_coords[0] < ball_coords[2] and paddle_coords[2] > ball_coords[0]:
            if paddle_coords[1] <= ball_coords[3] <= paddle_coords[3]:
                return True
        return False

    def move_left(self, event):
        if self.game_running:
            self.canvas.move(self.paddle, -20, 0)
            if self.canvas.coords(self.paddle)[0] < 0:
                self.canvas.move(self.paddle, -self.canvas.coords(self.paddle)[0], 0)

    def move_right(self, event):
        if self.game_running:
            self.canvas.move(self.paddle, 20, 0)
            if self.canvas.coords(self.paddle)[2] > 600:
                self.canvas.move(self.paddle, 600 - self.canvas.coords(self.paddle)[2], 0)

    def reset_ball(self):
        self.canvas.coords(self.ball, 290, 40, 310, 60)
        self.ball_dx = random.choice([-4, 4])

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(300, 200, text="Game Over", font=("Arial", 30), fill="red")

if __name__ == "__main__":
    root = tk.Tk()
    game = CatchTheBallGame(root)
    root.mainloop()
