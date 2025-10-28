import pygame
import random
import math
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- 定数の設定 ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

# 色の定義 (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128) # ボスの色

# ゲームの状態
STATE_PLAYING = 0 # 通常プレイ中
STATE_CHOICE = 1  # 選択中
STATE_BOSS = 2    # ボス戦

# --- フォントの準備 (グローバルで定義) ---
pygame.init() # フォントの前に init が必要
jp_font_names = ["Yu Gothic", "MS Gothic", "Hiragino Sans", "sans-serif"]
font_small_jp = pygame.font.match_font(jp_font_names)
if not font_small_jp:
    font_small_jp = None 
font_debug = pygame.font.Font(font_small_jp, 20)


# --- プレイヤー クラス ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30
        self.speed_x = 8
        self.shoot_delay = 500
        self.last_shot_time = pygame.time.get_ticks()
        self.arrow_count = 1

    def update_movement(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed_x
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            
    def auto_shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time > self.shoot_delay:
            self.last_shot_time = now
            spacing = 20
            start_offset = - (self.arrow_count - 1) * spacing / 2
            for i in range(self.arrow_count):
                x_pos = self.rect.centerx + start_offset + (i * spacing)
                arrow = Arrow(x_pos, self.rect.top)
                all_sprites.add(arrow)
                arrows.add(arrow)
                
    def apply_powerup(self, powerup_type):
        if powerup_type == "fire_rate":  # 連射速度上昇
            self.shoot_delay = max(50, self.shoot_delay * 0.7)
        elif powerup_type == "multi_shot":
            self.arrow_count += 1  # 矢の数増加
        elif powerup_type == "reduce_rate":
            self.shoot_delay = max(50, self.shoot_delay * 1.3)  # 連射速度低下
        elif powerup_type == "reduce_shot":
            self.arrow_count -= 1  # 矢の数減少
        elif 

# --- 矢 クラス ---
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 20))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self, scroll_speed, target_y=0):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

# --- 敵 クラス ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.Surface((70, 70))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x_pos
        self.rect.y = y_pos
        self.speed_y = 2

    def update(self, scroll_speed, target_y=0):
        self.rect.y += self.speed_y + scroll_speed
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()

# --- パワーアップ選択ゲート クラス ---
class PowerUpChoice(pygame.sprite.Sprite):
    def __init__(self, x, y, powerup_type, text):
        super().__init__()
        self.powerup_type = powerup_type
        self.image = pygame.Surface((SCREEN_WIDTH // 2 - 20, 100))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        
        font = pygame.font.Font(font_small_jp, 24)
        text_surf = font.render(text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.image.get_rect().center)
        self.image.blit(text_surf, text_rect)

    def update(self, scroll_speed, target_y):
        if self.rect.y < target_y:
            self.rect.y += scroll_speed
            if self.rect.y > target_y:
                self.rect.y = target_y

# --- ボス クラス ---
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 150
        self.height = 100
        self.image_orig = pygame.Surface((self.width, self.height))
        self.image_orig.fill(PURPLE)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = 50
        
        self.max_hp = 50 
        self.hp = self.max_hp
        self.speed_x = 5 
        
        self.font = pygame.font.Font(font_small_jp, 20)

    def update(self, scroll_speed, target_y=0):
        self.rect.x += self.speed_x
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x = -self.speed_x 

        self.image = self.image_orig.copy()
        
        hp_bar_rect = pygame.Rect(10, self.height - 20, self.width - 20, 10)
        pygame.draw.rect(self.image, RED, hp_bar_rect)
        
        # <--- 修正: 計算結果を int() で囲み、整数に変換 ---
        current_hp_width = int((self.width - 20) * (self.hp / self.max_hp))
        # <--- 修正ここまで ---
        
        if current_hp_width < 0:
            current_hp_width = 0
        current_hp_rect = pygame.Rect(10, self.height - 20, current_hp_width, 10)
        pygame.draw.rect(self.image, GREEN, current_hp_rect)
        
        hp_text = self.font.render(f"{self.hp} / {self.max_hp}", True, WHITE)
        text_rect = hp_text.get_rect(center=(self.width // 2, 20))
        self.image.blit(hp_text, text_rect)

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.kill()
            return True 
        return False
# --- ボス クラスここまで ---


# --- ゲームの初期化 ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("進め！こうかとん～選択のアロー～")
clock = pygame.time.Clock()

# --- フォント ---
font_large = pygame.font.Font(font_small_jp, 74)
game_over_text = font_large.render("GAME OVER", True, WHITE)
text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

# --- スプライトグループ ---
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
arrows = pygame.sprite.Group()
choice_gates = pygame.sprite.Group() 
bosses = pygame.sprite.Group()

# プレイヤーの作成
player = Player()
all_sprites.add(player)

# --- ゲームループ用 変数 ---
running = True
game_over = False
game_state = STATE_PLAYING

# 進行管理
world_scroll_y = 0  
scroll_speed = 3    
next_gate_trigger = 1000 
gate_y_position = 650    
enemies_spawned_for_gate = False
gate_pass_count = 0 

# --- ゲームループ ---
while running:
    clock.tick(FPS)
    
    # --- イベント処理 (入力) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    if game_over:
        screen.fill(BLACK)
        screen.blit(game_over_text, text_rect)
        pygame.display.flip()
        continue 
        
    keys = pygame.key.get_pressed()
    
    # --- 更新処理 ---
    player.update_movement(keys)
    player.auto_shoot()

    current_scroll_speed = 0

    if game_state == STATE_PLAYING:
        current_scroll_speed = scroll_speed
        world_scroll_y += current_scroll_speed
        
        if world_scroll_y > (next_gate_trigger - 400) and not enemies_spawned_for_gate: 
            e1 = Enemy(SCREEN_WIDTH * 0.3, -50)
            e2 = Enemy(SCREEN_WIDTH * 0.7, -100)
            all_sprites.add(e1, e2)
            enemies.add(e1, e2)
            enemies_spawned_for_gate = True
            
        if random.random() < 0.015: 
            e = Enemy(random.randrange(50, SCREEN_WIDTH - 50), -50)
            all_sprites.add(e)
            enemies.add(e)

        if world_scroll_y > next_gate_trigger:
            gate1 = PowerUpChoice(SCREEN_WIDTH * 0.25, -100, "fire_rate", "連射速度UP")
            gate2 = PowerUpChoice(SCREEN_WIDTH * 0.75, -100, "multi_shot", "矢の数+1")
            all_sprites.add(gate1, gate2)
            choice_gates.add(gate1, gate2)
            game_state = STATE_CHOICE 

    elif game_state == STATE_CHOICE:
        if len(choice_gates) > 0:
            first_gate = choice_gates.sprites()[0]
            if first_gate.rect.y < gate_y_position:
                current_scroll_speed = scroll_speed
            else:
                current_scroll_speed = 0 
        else:
            game_state = STATE_PLAYING

    elif game_state == STATE_BOSS:
        current_scroll_speed = 0 
        if len(bosses) == 0:
            game_state = STATE_PLAYING
            next_gate_trigger = world_scroll_y + 1500
            enemies_spawned_for_gate = False

    # 全スプライトの更新
    for sprite in all_sprites:
        if isinstance(sprite, Player):
            pass 
        elif isinstance(sprite, PowerUpChoice):
            sprite.update(current_scroll_speed, gate_y_position)
        else:
            sprite.update(current_scroll_speed, 0)


    # --- 当たり判定 ---
    
    # 1. 矢 と 敵
    pygame.sprite.groupcollide(arrows, enemies, True, True)

    # 1b. 矢 と ボス
    hits_arrow_boss = pygame.sprite.groupcollide(bosses, arrows, False, True) 
    if hits_arrow_boss:
        for boss_hit in hits_arrow_boss.keys():
            for _ in hits_arrow_boss[boss_hit]: 
                boss_hit.hit() 

    # 2. プレイヤー と 敵
    hits_player_enemy = pygame.sprite.spritecollide(player, enemies, True)
    if hits_player_enemy:
        game_over = True
        
    # 2b. プレイヤー と ボス
    hits_player_boss = pygame.sprite.spritecollide(player, bosses, False)
    if hits_player_boss:
        game_over = True
        
    # 3. プレイヤー と 選択ゲート
    hits_player_gate = pygame.sprite.spritecollide(player, choice_gates, False)
    if hits_player_gate:
        chosen_gate = hits_player_gate[0]
        player.apply_powerup(chosen_gate.powerup_type)
        
        for gate in choice_gates:
            gate.kill()
            
        gate_pass_count += 1 

        if gate_pass_count % 2 == 0:  # 偶数回目にボス出現
            game_state = STATE_BOSS
            boss = Boss() 
            all_sprites.add(boss)
            bosses.add(boss)
            
            for enemy in enemies:
                enemy.kill()
        else:
            game_state = STATE_PLAYING
            next_gate_trigger = world_scroll_y + 1500
            enemies_spawned_for_gate = False 

    # --- 描画処理 ---
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    dist_text = font_debug.render(f"進行距離: {int(world_scroll_y)} | ゲート通過: {gate_pass_count}", True, WHITE)
    screen.blit(dist_text, (10, 10))

    pygame.display.flip()

# --- 終了処理 ---
pygame.quit()