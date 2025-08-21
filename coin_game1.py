import pygame
import random
import os # ファイルの存在を確認するために必要

# 1. 初期化処理
pygame.init()
pygame.mixer.init() # サウンド機能を有効にする

# 2. 画面サイズの設定
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("コイン収集ゲーム")

# 色の定義（ダークテーマ）
DARK_GRAY = (45, 48, 51)
LIGHT_CYAN = (130, 210, 220)
GOLD = (255, 200, 80)

# --- 効果音の読み込み（★★これが最終完成形です★★） ---

# このスクリプト(my_game.py)自身の絶対パスを取得
# これにより、どこから実行しても、このファイルの場所が基準になる
try:
    script_dir = os.path.dirname(__file__)
except NameError:
    script_dir = os.getcwd() # Colabなどの対話環境用のフォールバック

# 読み込むファイル名を指定
sound_file_name = 'coin_get.ogg' 
# スクリプトの場所とファイル名を結合して、完全なパスを作成
sound_file_path = os.path.join(script_dir, sound_file_name)

print(f"効果音ファイルのフルパスを探します: {sound_file_path}") # デバッグ用にフルパスを表示

if os.path.exists(sound_file_path):
    coin_sound = pygame.mixer.Sound(sound_file_path)
    coin_sound.set_volume(0.19)
    print("サウンドオブジェクトの作成と音量設定が完了しました。")
else:
    coin_sound = None
    print(f"警告: 効果音ファイル '{sound_file_path}' が見つかりません。")

# プレイヤーの設定
player_size = 50
player_x = (screen_width - player_size) // 2
player_y = (screen_height - player_size) // 2
player_speed = 0.7

# コインの設定
coin_size = 30
coin_x = random.randint(0, screen_width - coin_size)
coin_y = random.randint(0, screen_height - coin_size)

# スコアの設定
score = 0
font = pygame.font.Font(None, 50)

# 3. ゲームループ
running = True
while running:
    # 4. イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キーボードの状態をチェック
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_x += player_speed
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed

    # 5. 画面の描画
    screen.fill(DARK_GRAY)

    # 当たり判定のために四角形オブジェクトを作成
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    coin_rect = pygame.Rect(coin_x, coin_y, coin_size, coin_size)

    # 当たり判定
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_x = random.randint(0, screen_width - coin_size)
        coin_y = random.randint(0, screen_height - coin_size)
        
        # --- 効果音を再生 ---
        if coin_sound: # coin_soundがNoneでないことを確認
            coin_sound.play()

    # プレイヤーとコインを描画
    pygame.draw.rect(screen, LIGHT_CYAN, player_rect)
    pygame.draw.rect(screen, GOLD, coin_rect)

    # スコアを描画
    score_text = font.render(f"Score: {score}", True, LIGHT_CYAN)
    screen.blit(score_text, (10, 10))

    # 画面の更新
    pygame.display.flip()

# 7. 終了処理
pygame.quit()