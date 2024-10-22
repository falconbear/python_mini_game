import pygame

pygame.init()

W, H = 400, 300

win = pygame.display.set_mode((W, H))

#マリオの座標
mx = 50
my = 250

#マリオの上下の移動距離
vy = 0

#地面にいるかどうかのフラグ
on_ground = False

enemies = [
  {'rect' : pygame.Rect(250, 250, 20, 20), 'dir': -2},
  {'rect' : pygame.Rect(200, 250, 20, 20), 'dir': -1},
  {'rect' : pygame.Rect(300, 250, 20, 20), 'dir': -2}
]

clock = pygame.time.Clock()

while True:
  for e in pygame.event.get():
    if e.type == pygame.QUIT:
      exit()
  #キーの押下状態を取得
  keys = pygame.key.get_pressed()

  mx += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 5

  if keys[pygame.K_SPACE] and on_ground:
    vy -= 15

  #一つ下に下げる
  vy += 1
  #y軸方向移動距離を足す
  my += vy

  on_ground = False

  if my >= 250:
    my = 250
    vy = 0
    on_ground = True
  
  for enemy in enemies:
    #敵を左右に動かす
    enemy['rect'].x += enemy['dir']
    if enemy['rect'].left <= 0 or enemy['rect'].right > W:
      #端に来た時は向きを反転させる
      enemy['dir'] *= -1

    if enemy['rect'].colliderect(pygame.Rect(mx, my, 20, 20)) and vy > 0:
      #マリオとヒットし、下に移動している時
      enemies.remove(enemy)
      #踏んだ時にちょっとジャンプ
      vy = -10

  #背景を水色に塗りつぶし
  win.fill((135, 206, 235))
  #マリオを描画
  pygame.draw.rect(win, (255, 0, 0), (mx, my, 20, 20))

  #敵を描画
  for enemy in enemies:
    pygame.draw.rect(win, (0, 255, 0), enemy['rect'])

  #画面を更新
  pygame.display.flip()
  clock.tick(30)