import pygame
import random
import psycopg2

DB_CONFIG = {
    "host": "localhost",
    "dbname": "snakegame",      # <-- измени на свою БД
    "user": "postgres",      # <-- имя пользователя
    "password": "Serik_100",      # <-- пароль PostgreSQL
    "port": 5432,
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)



def create_tables():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            user_id INT REFERENCES users(id),
            score INT DEFAULT 0,
            level INT DEFAULT 1,
            PRIMARY KEY(user_id)
        );
    """)

    conn.commit()
    conn.close()


def get_or_create_user(username):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
    result = cur.fetchone()

    if result:
        user_id = result[0]
        print(f"Пользователь найден: {username}")
    else:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id;", (username,))
        user_id = cur.fetchone()[0]

        cur.execute(
            "INSERT INTO user_score (user_id, score, level) VALUES (%s, 0, 1);",
            (user_id,)
        )
        print(f"Создан новый пользователь: {username}")

    conn.commit()
    conn.close()
    return user_id


def get_user_stats(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT score, level FROM user_score WHERE user_id = %s;", (user_id,))
    score, level = cur.fetchone()
    conn.close()
    return score, level


def save_progress(user_id, score, level):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_score SET score = %s, level = %s WHERE user_id = %s;
    """, (score, level, user_id))

    conn.commit()
    conn.close()


def snake_game(username):
    user_id = get_or_create_user(username)
    score, level = get_user_stats(user_id)

    pygame.init()
    WIDTH, HEIGHT = 600, 600
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake Game with PostgreSQL")

    clock = pygame.time.Clock()
    snake_pos = [100, 100]
    snake_body = [[100, 100], [90, 100], [80, 100]]
    direction = "RIGHT"

    food_pos = [random.randrange(1, 30) * 20,
                random.randrange(1, 30) * 20]
    food_spawn = True

    speed = 10 + level  # скорость растёт с уровнем

    running = True
    paused = False

    font = pygame.font.SysFont("Arial", 24)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_progress(user_id, score, level)
                running = False

            # управление
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                if event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                if event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

                # пауза (P)
                if event.key == pygame.K_p:
                    paused = not paused
                    if paused:
                        save_progress(user_id, score, level)
                        print("Игра на паузе. Прогресс сохранён.")

        if paused:
            continue

        # движение змейки
        if direction == "UP":
            snake_pos[1] -= 20
        if direction == "DOWN":
            snake_pos[1] += 20
        if direction == "LEFT":
            snake_pos[0] -= 20
        if direction == "RIGHT":
            snake_pos[0] += 20

        snake_body.insert(0, list(snake_pos))

        # поедание еды
        if snake_pos == food_pos:
            score += 10
            level = score // 50 + 1  # каждые 50 очков + уровень
            speed = 10 + level
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, 30) * 20,
                        random.randrange(1, 30) * 20]
        food_spawn = True

        # смерть от стены
        if snake_pos[0] < 0 or snake_pos[0] > 580 or snake_pos[1] < 0 or snake_pos[1] > 580:
            save_progress(user_id, score, level)
            running = False

        # смерть от самого себя
        for block in snake_body[1:]:
            if snake_pos == block:
                save_progress(user_id, score, level)
                running = False

        # отрисовка
        win.fill((0, 0, 0))

        for block in snake_body:
            pygame.draw.rect(win, (0, 255, 0), pygame.Rect(block[0], block[1], 20, 20))

        pygame.draw.rect(win, (255, 0, 0), pygame.Rect(food_pos[0], food_pos[1], 20, 20))

        text = font.render(f"Score: {score} | Level: {level}", True, (255, 255, 255))
        win.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(speed)

    pygame.quit()



if __name__ == "__main__":
    create_tables()

    username = input("Введите свой username: ").strip()
    snake_game(username)

    print("Игра завершена!")
