import pygame
import random
import psycopg2

db_config = {
    "host": "localhost",
    "dbname": "snakegame",
    "user": "postgres",
    "password": "Serik_100",
    "port": 5432
}

def connect():
    return psycopg2.connect(**db_config)

def create_tables():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            user_id INT PRIMARY KEY REFERENCES users(id),
            score INT DEFAULT 0,
            level INT DEFAULT 1
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_user(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
    else:
        cur.execute("INSERT INTO users(username) VALUES(%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]
        cur.execute("INSERT INTO user_score(user_id, score, level) VALUES(%s, 0, 1);", (user_id,))
    conn.commit()
    cur.close()
    conn.close()
    return user_id

def get_user_stats(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s;", (user_id,))
    stats = cur.fetchone()
    cur.close()
    conn.close()
    return stats

def save_progress(user_id, score, level):
    conn = connect()
    cur = conn.cursor()
    cur.execute("UPDATE user_score SET score = %s, level = %s WHERE user_id = %s;", (score, level, user_id))
    conn.commit()
    cur.close()
    conn.close()

def generate_walls(level):
    walls = []
    if level == 1:
        return walls
    if level == 2:
        for x in range(0, 600, 20):
            walls.append([x, 200])
    if level == 3:
        for y in range(0, 600, 20):
            walls.append([300, y])
    if level >= 4:
        for x in range(0, 600, 20):
            walls.append([x, 200])
            walls.append([x, 400])
    return walls

def snake_game(username):
    user_id = get_or_create_user(username)
    score, level = get_user_stats(user_id)
    pygame.init()
    width, height = 600, 600
    win = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    snake_pos = [100, 100]
    snake_body = [[100, 100], [80, 100], [60, 100]]
    direction = "right"
    walls = generate_walls(level)
    walls = [w for w in walls if w not in snake_body]
    food_pos = [random.randrange(1, 30) * 20, random.randrange(1, 30) * 20]
    while food_pos in snake_body or food_pos in walls:
        food_pos = [random.randrange(1, 30) * 20, random.randrange(1, 30) * 20]
    food_spawn = True
    speed = 10 + level
    paused = False
    running = True
    font = pygame.font.SysFont("Arial", 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(user_id, score, level)
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "down":
                    direction = "up"
                elif event.key == pygame.K_DOWN and direction != "up":
                    direction = "down"
                elif event.key == pygame.K_LEFT and direction != "right":
                    direction = "left"
                elif event.key == pygame.K_RIGHT and direction != "left":
                    direction = "right"
                elif event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        save_progress(user_id, score, level)

        if paused:
            win.fill((0, 0, 0))
            text = font.render(f"PAUSED  score: {score}  level: {level}", True, (255, 255, 255))
            win.blit(text, (180, 280))
            pygame.display.update()
            clock.tick(5)
            continue

        if direction == "up":
            snake_pos[1] -= 20
        elif direction == "down":
            snake_pos[1] += 20
        elif direction == "left":
            snake_pos[0] -= 20
        elif direction == "right":
            snake_pos[0] += 20

        snake_body.insert(0, list(snake_pos))

        if snake_pos == food_pos:
            score += 10
            level = score // 50 + 1
            speed = 10 + level
            walls = generate_walls(level)
            walls = [w for w in walls if w not in snake_body]
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, 30) * 20, random.randrange(1, 30) * 20]
            while food_pos in snake_body or food_pos in walls:
                food_pos = [random.randrange(1, 30) * 20, random.randrange(1, 30) * 20]
        food_spawn = True

        if snake_pos[0] < 0 or snake_pos[0] > 580 or snake_pos[1] < 0 or snake_pos[1] > 580:
            save_progress(user_id, score, level)
            running = False

        for block in snake_body[1:]:
            if snake_pos == block:
                save_progress(user_id, score, level)
                running = False

        for w in walls:
            if snake_pos == w:
                save_progress(user_id, score, level)
                running = False

        win.fill((0, 0, 0))
        for block in snake_body:
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(block[0], block[1], 20, 20))
        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 20, 20))
        for w in walls:
            pygame.draw.rect(win, (0, 0, 255), pygame.Rect(w[0], w[1], 20, 20))
        text = font.render(f"score: {score}  level: {level}", True, (255, 255, 255))
        win.blit(text, (10, 10))
        pygame.display.update()
        clock.tick(speed)

    pygame.quit()

if __name__ == "__main__":
    create_tables()
    username = input("enter username: ")
    snake_game(username)
    print("game over")


