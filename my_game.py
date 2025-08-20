import pygame

# 1. 初期化処理
pygame.init()

# 2. 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("動く！僕のRPG")

# ★★★ キャラクターの位置と速度を管理する変数を追加 ★★★
player_x = 350 # X座標
player_y = 250 # Y座標
player_speed = 5 # 移動速度

# 3. ゲームループ
running = True
while running:
    # 4. イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # ★★★ キーボードの状態をチェック ★★★
    keys = pygame.key.get_pressed() # 押されているキーのリストを取得
    if keys[pygame.K_LEFT]:
        player_x -= player_speed # 左キーが押されていたら、X座標を減らす
    if keys[pygame.K_RIGHT]:
        player_x += player_speed # 右キーが押されていたら、X座標を増やす
    if keys[pygame.K_UP]:
        player_y -= player_speed # 上キーが押されていたら、Y座標を減らす
    if keys[pygame.K_DOWN]:
        player_y += player_speed # 下キーが押されていたら、Y座標を増やす

    # 5. 画面の描画
    screen.fill((0, 0, 255))  # 背景を青で塗りつぶす

    # ★★★ キャラクター（四角形）を描画 ★★★
    # 固定の座標ではなく、player_x と player_y の位置に描画する
    pygame.draw.rect(screen, (255, 255, 255), (player_x, player_y, 100, 100))

    # 6. 画面の更新
    pygame.display.flip()

# 7. 終了処理
pygame.quit()