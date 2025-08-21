import pygame
import random

# 1. 初期化処理
pygame.init()

# 2. 画面と色の設定
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("僕のギルド")
DARK_GRAY = (45, 48, 51)
LIGHT_CYAN = (130, 210, 220)
BORDER_COLOR = (100, 100, 100)
HIGHLIGHT_COLOR = (200, 200, 100)
RED = (255, 100, 100)
GOLD = (255, 200, 80)

# フォントの準備
title_font = pygame.font.SysFont("meiryo", 60)
label_font = pygame.font.SysFont("meiryo", 40)
character_font = pygame.font.SysFont("meiryo", 32)
detail_font = pygame.font.SysFont("meiryo", 28)

# ★★★ 新しい関数：HPバーを描画する ★★★
def draw_hp_bar(surface, x, y, width, height, current_hp, max_hp):
    if current_hp < 0:
        current_hp = 0
    # HPの割合を計算 (0.0 ~ 1.0)
    ratio = current_hp / max_hp
    
    # HPバーの外枠（背景）と、内側のバーのRectを定義
    background_rect = pygame.Rect(x, y, width, height)
    hp_rect = pygame.Rect(x, y, width * ratio, height) # 現在のHPの割合だけ幅を狭める
    
    # 描画
    pygame.draw.rect(surface, (50, 50, 50), background_rect) # 背景を濃いグレーで
    pygame.draw.rect(surface, (0, 200, 0), hp_rect)       # HPを緑色で
    pygame.draw.rect(surface, BORDER_COLOR, background_rect, 2) # 枠線

# 冒険者のデータ
adventurers = [
    {"name": "アタリ", "level": 5, "class": "戦士", "hp": 150, "max_hp": 150, "attack": 30, "defense": 20, "skills": ["強打"]},
    {"name": "ベータ", "level": 3, "class": "魔法使い", "hp": 90, "max_hp": 90, "attack": 15, "defense": 10, "skills": ["ファイア", "ヒール"]},
    {"name": "シーラ", "level": 4, "class": "僧侶", "hp": 120, "max_hp": 120, "attack": 10, "defense": 15, "skills": ["ヒール", "防御"]}
]

# ゲームの状態を管理する変数
gold = 100
training_cost = 50
selected_adventurer = None
adventurer_rects = []
message = ""
message_timer = 0
game_state = "guild_home"
active_player = None # 戦闘に参加するプレイヤーを記憶する変数

# UIの骨格となるRectを、画面サイズを基準に定義
margin = screen_width * 0.05
list_x = margin
list_y = screen_height * 0.15
list_width = screen_width * 0.4
list_height = screen_height * 0.8
list_panel_rect = pygame.Rect(list_x, list_y, list_width, list_height)
right_panel_x = list_x + list_width + margin
report_width = screen_width - right_panel_x - margin
report_height = screen_height * 0.4
report_rect = pygame.Rect(right_panel_x, list_y, report_width, report_height)
facility_y = list_y + report_height + margin * 0.5
facility_height = screen_height - facility_y - (margin * 0.5)
facility_rect = pygame.Rect(right_panel_x, facility_y, report_width, facility_height)

# 3. ゲームループ
running = True
while running:
    # 4. イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == "guild_home":
                if facility_rect.collidepoint(event.pos):
                    if selected_adventurer:
                        if gold >= training_cost:
                            gold -= training_cost
                            selected_adventurer['attack'] += 2
                            message = f"{selected_adventurer['name']}の攻撃力が上がった！"
                            message_timer = 120
                        else:
                            message = "ゴールドが足りません！"
                            message_timer = 120
                    else:
                        message = "先に冒険者を選択してください。"
                        message_timer = 120
                elif report_rect.collidepoint(event.pos):
                    if selected_adventurer:
                        active_player = selected_adventurer
                        game_state = "battle"
                    else:
                        message = "冒険に出るメンバーを選択してください。"
                        message_timer = 120
                else:
                    for i, rect in enumerate(adventurer_rects):
                        if rect.collidepoint(event.pos):
                            selected_adventurer = adventurers[i]
                            break
    
    # 5. 画面の描画
    screen.fill(DARK_GRAY)
    
    if game_state == "guild_home":
        # (A) タイトル
        title_text = title_font.render("ギルドホーム", True, LIGHT_CYAN)
        title_rect = title_text.get_rect(center=(screen_width // 2, screen_height * 0.08))
        screen.blit(title_text, title_rect)

        # (B) 冒険者リスト
        pygame.draw.rect(screen, BORDER_COLOR, list_panel_rect, 2)
        list_label = label_font.render("冒険者リスト", True, LIGHT_CYAN)
        screen.blit(list_label, (list_panel_rect.x + 10, list_panel_rect.y + 10))
        adventurer_rects.clear()
        mouse_pos = pygame.mouse.get_pos()
        start_y = list_panel_rect.y + 60
        for i, adventurer in enumerate(adventurers):
            display_text = f"{adventurer['name']} - LV:{adventurer['level']} ({adventurer['class']})"
            text_surface = character_font.render(display_text, True, LIGHT_CYAN)
            text_rect = text_surface.get_rect(topleft=(list_panel_rect.x + 10, start_y + (i * 40)))
            if text_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, text_rect, 2)
            screen.blit(text_surface, text_rect)
            adventurer_rects.append(text_rect)

        # (C) 冒険出発ボタン 兼 詳細ステータス
        pygame.draw.rect(screen, BORDER_COLOR, report_rect, 2)
        detail_label = label_font.render("冒険へ出発", True, LIGHT_CYAN)
        screen.blit(detail_label, (report_rect.x + 10, report_rect.y + 10))
        if selected_adventurer:
            details = [
                f"名前: {selected_adventurer['name']}", f"LV: {selected_adventurer['level']}", f"クラス: {selected_adventurer['class']}",
                "", f"HP: {selected_adventurer['hp']}", f"攻撃力: {selected_adventurer['attack']}", f"防御力: {selected_adventurer['defense']}",
                "", f"スキル: {', '.join(selected_adventurer['skills'])}"
            ]
            detail_start_y = report_rect.y + 60
            for i, detail_line in enumerate(details):
                line_surface = detail_font.render(detail_line, True, LIGHT_CYAN)
                screen.blit(line_surface, (report_rect.x + 10, detail_start_y + (i * 30)))

        # (D) 施設（訓練所）
        pygame.draw.rect(screen, BORDER_COLOR, facility_rect, 2)
        facility_label = label_font.render("施設：訓練所", True, LIGHT_CYAN)
        screen.blit(facility_label, (facility_rect.x + 10, facility_rect.y + 10))
        cost_text = detail_font.render(f"コスト: {training_cost} G", True, LIGHT_CYAN)
        screen.blit(cost_text, (facility_rect.x + 10, facility_rect.y + 60))
        effect_text = detail_font.render("効果: 攻撃力+2", True, LIGHT_CYAN)
        screen.blit(effect_text, (facility_rect.x + 10, facility_rect.y + 90))

        # (E) ゴールド表示
        gold_text = label_font.render(f"所持金: {gold} G", True, GOLD)
        gold_rect = gold_text.get_rect(topright=(screen_width - 30, 20))
        screen.blit(gold_text, gold_rect)

        # (F) メッセージ表示
        if message_timer > 0:
            message_text = label_font.render(message, True, RED)
            message_rect = message_text.get_rect(center=(screen_width // 2, screen_height - 50))
            screen.blit(message_text, message_rect)
            message_timer -= 1
            
    elif game_state == "battle":
        # 仮の敵データ（後で本物の敵データと連携します）
        temp_enemy = {"name": "スライム", "hp": 50, "max_hp": 50}

        # (A) プレイヤー情報の表示
        player_info_y = screen_height * 0.1
        player_name_text = label_font.render(f"{active_player['name']} LV:{active_player['level']}", True, LIGHT_CYAN)
        screen.blit(player_name_text, (margin, player_info_y))
        draw_hp_bar(screen, margin, player_info_y + 50, 400, 30, active_player['hp'], active_player['max_hp'])

        # (B) 敵情報の表示
        enemy_info_x = screen_width - margin - 400
        enemy_name_text = label_font.render(f"{temp_enemy['name']}", True, RED)
        screen.blit(enemy_name_text, (enemy_info_x, player_info_y))
        draw_hp_bar(screen, enemy_info_x, player_info_y + 50, 400, 30, temp_enemy['hp'], temp_enemy['max_hp'])

        # (C) バトルログのエリア
        log_height = screen_height * 0.3
        log_y = screen_height - log_height - (margin * 0.5)
        log_rect = pygame.Rect(margin, log_y, screen_width - (margin * 2), log_height)
        pygame.draw.rect(screen, BORDER_COLOR, log_rect, 2)
        log_label_text = label_font.render("バトルログ", True, LIGHT_CYAN)
        screen.blit(log_label_text, (log_rect.x + 10, log_rect.y + 10))

    # 6. 画面の更新
    pygame.display.flip()

# 7. 終了処理
pygame.quit()