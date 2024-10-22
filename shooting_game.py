import pygame
import random
import math

# 初期化
pygame.init()

# 画面サイズの設定
screen_width = 400
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# プレイヤーの設定
player_width = 100
player_height = 60
player_x = screen_width // 2 - player_width // 2
player_y = screen_height - player_height - 10
player_speed = 5

# 味方の初期HP
player_hp = 100

# 弾丸の設定
bullet_width = 10
bullet_height = 10
bullet_speed = -7
bullets = []

# 弾の攻撃力
bullet_damage = 10

# 弾の射出口の数
max_bullet = 1

# アイテム効果のリスト
item_effects = ['+5', '×2', '-5', '÷2']

# 敵の設定
enemy_width = 80
enemy_height = 60
enemy_speed = 3
enemies = []

# 敵の種類とその属性
enemy_types = {
    'enemy_A': {'hp': 30, 'points': 30},
    'enemy_B': {'hp': 50, 'points': 50},
    'enemy_C': {'hp': 100, 'points': 100}
}

# 接触中の敵を追跡するためのリスト
colliding_enemies = []

# アイテムゾーンの設定
item_width = 100
item_height = 20
item_speed = enemy_speed
items = []

# スコアの初期化
score = 0

# 敵を生成する関数
def create_enemy():
    enemy_type = random.choice(list(enemy_types.keys()))
    enemy_x = random.randint(0, screen_width - enemy_width)
    enemy_y = random.randint(-150, -50)
    return {'type': enemy_type, 'x': enemy_x, 'y': enemy_y, 'hp': enemy_types[enemy_type]['hp']}

# 敵の出現を管理するタイマー
pygame.time.set_timer(pygame.USEREVENT + 3, 5000)  # 5秒ごとに敵を追加

# 弾を発射する関数
def shootBullet():
    bullets.append([player_x + player_width // 2, player_y])

# 0.5秒間隔で弾を発射するタイマーを設定
pygame.time.set_timer(pygame.USEREVENT, 500)

# 1秒ごとにHPを減少させるタイマーを設定
pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

# アイテムゾーンを生成する関数
def create_item():
    item_x = random.randint(0, screen_width - item_width)
    item_y = random.randint(-150, -50)
    effect = random.choice(item_effects)
    return [item_x, item_y, effect]

# 定期的にアイテムゾーンを追加
pygame.time.set_timer(pygame.USEREVENT + 2, 5000)  # 5秒ごとにアイテムゾーンを追加

# 弾の発射タイマーを設定
def set_bullet_timers():
    global max_bullet
    left_columns = max_bullet % 5
    right_columns = 5 - left_columns
    high_freq_interval = int(1000 / (max_bullet / 5 + 1))
    low_freq_interval = int(1000 / (max_bullet / 5))
    
    if max_bullet > 5:
        pygame.time.set_timer(pygame.USEREVENT, low_freq_interval)  # 低頻度の弾
        pygame.time.set_timer(pygame.USEREVENT + 4, high_freq_interval)  # 高頻度の弾
    else:
        pygame.time.set_timer(pygame.USEREVENT, 1000)  # 1秒間隔で発射
        pygame.time.set_timer(pygame.USEREVENT + 4, 0)  # 無効化

set_bullet_timers()

# ゲームループの開始
running = True
clock = pygame.time.Clock()
elapsed_time = 0

while running:
    clock.tick(60)
    elapsed_time += 1 / 60  # 経過時間を秒で計算
    
    # イベントの取得
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.USEREVENT:
            # 低頻度の弾を発射
            for i in range(min(max_bullet, 5 - (max_bullet % 5))):
                offset = (i - 2) * (player_width // 5)
                bullets.append([player_x + player_width // 2 + offset, player_y])
        elif event.type == pygame.USEREVENT + 4:
            # 高頻度の弾を発射
            for i in range(max_bullet % 5):
                offset = (i - 2) * (player_width // 5)
                bullets.append([player_x + player_width // 2 + offset, player_y])
        elif event.type == pygame.USEREVENT + 1:
            player_hp -= 10 * len(colliding_enemies)
            print(f"味方のHP: {player_hp}")
            if player_hp <= 0:
                running = False
                print("ゲームオーバー")
        elif event.type == pygame.USEREVENT + 2:
            items.append(create_item())
        elif event.type == pygame.USEREVENT + 3:
            num_enemies_to_add = (int(elapsed_time) // 5) * 3
            for _ in range(num_enemies_to_add):
                enemies.append(create_enemy())
    
    # キー入力の取得
    keys = pygame.key.get_pressed()
    
    # プレイヤーの移動と弾の発射
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < screen_width - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE]:
        for i in range(max_bullet):
            # 弾の位置を均等に配置
            offset = (i - max_bullet // 2) * (player_width // max_bullet)
            bullets.append([player_x + player_width // 2 + offset, player_y])
    
    # 画面のクリア
    screen.fill(BLACK)
    
    # プレイヤーの描画
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
    pygame.draw.rect(screen, WHITE, player_rect)
    
    # 弾丸の移動と描画
    for bullet in bullets[:]:
        bullet[1] += bullet_speed
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], bullet_width, bullet_height))
    
    # 画面外の弾丸を削除
    bullets = [bullet for bullet in bullets if bullet[1] > 0]
    
    # 敵の移動と描画
    colliding_enemies.clear()
    for enemy in enemies[:]:
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_width, enemy_height)
        
        if player_rect.colliderect(enemy_rect):
            colliding_enemies.append(enemy)
        else:
            enemy['y'] += enemy_speed
        
        pygame.draw.rect(screen, WHITE, enemy_rect)

        # 敵が味方陣地の境界線に触れた場合、ゲームオーバー
        if enemy['y'] + enemy_height >= screen_height:
            running = False
            print("ゲームオーバー")

    # 弾丸と敵の衝突判定
    for bullet in bullets[:]:
        bullet_rect = pygame.Rect(bullet[0], bullet[1], bullet_width, bullet_height)
        for enemy in enemies[:]:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], enemy_width, enemy_height)
            if bullet_rect.colliderect(enemy_rect):
                enemy['hp'] -= bullet_damage
                bullets.remove(bullet)
                if enemy['hp'] <= 0:
                    score += enemy_types[enemy['type']]['points']
                    enemies.remove(enemy)
                break  # 1つの弾で複数の敵を倒さないようにする

    # スコアの表示
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (screen_width - 150, 10))

    # アイテムゾーンの移動と描画
    for item in items[:]:
        item_rect = pygame.Rect(item[0], item[1], item_width, item_height)
        item[1] += item_speed
        pygame.draw.rect(screen, RED, item_rect)
        
        # アイテム効果を表示
        font = pygame.font.Font(None, 36)
        text = font.render(item[2], True, WHITE)
        screen.blit(text, (item[0], item[1] - 20))
        
        # プレイヤーがアイテムゾーンに接触した場合
        if player_rect.colliderect(item_rect):
            effect = item[2]
            if effect == '+5':
                max_bullet += 5
            elif effect == '×2':
                max_bullet *= 2
            elif effect == '-5':
                max_bullet = max(1, max_bullet - 5)
            elif effect == '÷2':
                max_bullet = max(1, math.ceil(max_bullet / 2))
            items.remove(item)
            set_bullet_timers()  # タイマーを再設定
    
    # 画面の更新
    pygame.display.flip()

# ゲーム終了時にPygameを終了
pygame.quit()
