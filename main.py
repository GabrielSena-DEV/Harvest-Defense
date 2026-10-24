import math
import json
import os
import random
import sys
from datetime import datetime
import pygame

# HARVEST DEFENSE — jogo de defesa em Pygame (fazenda + Halloween)
# Controles: clique em uma torre no painel inferior e depois no mapa para posicioná-la.
# Clique em uma torre já colocada para selecioná-la. Espaço: iniciar/próxima onda.
# 1-6: selecionar torre. U: melhorar torre selecionada. F: pulso lunar.
# T: árvore de habilidades. ESC: voltar ao menu. F11: tela cheia.

pygame.init()
pygame.display.set_caption("HARVEST DEFENSE — Proteja a fazenda. Defenda a colheita.")
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED)
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("trebuchetms,verdana,dejavusans", 17)
SMALL = pygame.font.SysFont("trebuchetms,verdana,dejavusans", 14)
BIG = pygame.font.SysFont("georgia,dejavuserif", 26, bold=True)
HUGE = pygame.font.SysFont("georgia,dejavuserif", 32, bold=True)

BG = (16, 9, 26)
GRASS_A = (31, 36, 44)
GRASS_B = (35, 41, 49)
WHITE = (240, 232, 245)
MINT = (140, 232, 110)      # "bom / disponível" (verde gosma)
CYAN = (96, 208, 255)
PURPLE = (192, 130, 255)
ORANGE = (255, 150, 50)     # abóbora
RED = (255, 84, 84)
MUTED = (160, 140, 178)
PANEL = (28, 17, 44)
BORDER = (96, 58, 128)
DIRT = (104, 72, 48)
DIRT_EDGE = (70, 46, 34)

MAP_RECT = pygame.Rect(24, 80, 1052, 470)
PATH = [(30, 315), (165, 315), (165, 170), (360, 170), (360, 430),
        (560, 430), (560, 245), (760, 245), (760, 360), (1000, 360)]
CORE = (1015, 360)   # o celeiro
TOWER_TYPES = [
    {"name": "Espantalho", "cost": 100, "range": 150, "damage": 20, "rate": 0.72, "color": CYAN, "desc": "Dano equilibrado"},
    {"name": "Gárgula", "cost": 170, "range": 170, "damage": 36, "rate": 1.3, "color": MINT, "desc": "Golpes pesados"},
    {"name": "Lápide", "cost": 140, "range": 130, "damage": 10, "rate": 2.5, "color": (176, 178, 198), "desc": "Invoca bloqueadores", "behavior": "summon"},
    {"name": "Milho", "cost": 120, "range": 130, "damage": 5, "rate": 0.24, "color": (255, 220, 80), "desc": "Rajada veloz"},
    {"name": "Corvo", "cost": 190, "range": 220, "damage": 55, "rate": 1.85, "color": (174, 130, 220), "desc": "Precisão e alcance", "bullet_speed": 680},
    {"name": "Abóbora", "cost": 175, "range": 145, "damage": 22, "rate": 1.2, "color": ORANGE, "desc": "Explosão em área", "area": 48},
]
WAVES = [
    {"count": 9, "hp": 38, "speed": 62, "reward": 24, "name": "Fantasminhas"},
    {"count": 13, "hp": 54, "speed": 72, "reward": 30, "name": "Gosmas famintas"},
    {"count": 15, "hp": 72, "speed": 80, "reward": 37, "name": "Zumbis do milharal"},
    {"count": 17, "hp": 94, "speed": 88, "reward": 45, "name": "Abóboras malditas"},
    {"count": 21, "hp": 125, "speed": 98, "reward": 58, "name": "Colheita sombria"},
    {"count": 24, "hp": 145, "speed": 100, "reward": 64, "name": "Rei Abóbora"},
    {"count": 27, "hp": 162, "speed": 103, "reward": 70, "name": "Horda do milharal"},
    {"count": 30, "hp": 181, "speed": 106, "reward": 76, "name": "Praga do pântano"},
    {"count": 33, "hp": 202, "speed": 109, "reward": 82, "name": "Guardiões da colheita"},
    {"count": 36, "hp": 224, "speed": 112, "reward": 88, "name": "Marcha amaldiçoada"},
    {"count": 39, "hp": 248, "speed": 115, "reward": 94, "name": "Tempestade de monstros"},
    {"count": 43, "hp": 275, "speed": 118, "reward": 105, "name": "Rei Abóbora: batalha final"},
]
DIFFICULTIES = {
    "facil": {"name": "FÁCIL", "wave_count": 6, "enemy_hp": 0.8, "enemy_speed": 0.9, "core_damage": 0.8, "score_multiplier": 0.8},
    "normal": {"name": "MÉDIO", "wave_count": 9, "enemy_hp": 1.0, "enemy_speed": 1.0, "core_damage": 1.0, "score_multiplier": 1.0},
    "dificil": {"name": "DIFÍCIL", "wave_count": 12, "enemy_hp": 1.25, "enemy_speed": 1.12, "core_damage": 1.25, "score_multiplier": 1.25},
}
# cor das partículas ao derrotar cada tipo de monstro
KIND_COLORS = {"ghost": (235, 235, 255), "slime": PURPLE, "zombie": MINT, "pumpkin": ORANGE}

def fmt_money(n):
    return str(int(max(0, n)))

def draw_text(text, x, y, color=WHITE, font=FONT, surface=screen):
    surface.blit(font.render(str(text), True, color), (x, y))

def draw_outlined(text, font, color, center, outline=(20, 8, 30), alpha=255):
    base = font.render(text, True, color)
    edge = font.render(text, True, outline)
    w, h = base.get_size()
    surf = pygame.Surface((w + 6, h + 6), pygame.SRCALPHA)
    for dx in (0, 3, 6):
        for dy in (0, 3, 6):
            if (dx, dy) != (3, 3):
                surf.blit(edge, (dx, dy))
    surf.blit(base, (3, 3))
    surf.set_alpha(alpha)
    screen.blit(surf, (center[0] - surf.get_width()//2, center[1] - surf.get_height()//2))

def draw_pumpkin(surface, x, y, r, face=False):
    """Desenha uma abóbora simples (usada como ícone da moeda e nos inimigos)."""
    pygame.draw.ellipse(surface, (230, 112, 24), (x-r, y-int(r*.8), r*2, int(r*1.7)))
    pygame.draw.ellipse(surface, (255, 150, 50), (x-int(r*.55), y-int(r*.8), int(r*1.1), int(r*1.7)))
    pygame.draw.ellipse(surface, (200, 90, 18), (x-int(r*.2), y-int(r*.8), int(r*.4), int(r*1.7)))
    pygame.draw.rect(surface, (70, 120, 40), (x-2, y-int(r*.8)-int(r*.4), 4, max(3, int(r*.45))))
    if face:
        e = max(2, r//4)
        pygame.draw.polygon(surface, (255, 230, 120), [(x-r//2, y-1), (x-r//5, y-1), (x-r//3, y-e-2)])
        pygame.draw.polygon(surface, (255, 230, 120), [(x+r//2, y-1), (x+r//5, y-1), (x+r//3, y-e-2)])
        pygame.draw.arc(surface, (255, 230, 120), (x-r//2, y, r, r//2+2), math.pi, 2*math.pi, 2)


def dist(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def point_segment_distance(p, a, b):
    ax, ay = a; bx, by = b; px, py = p
    dx, dy = bx-ax, by-ay
    if dx == dy == 0:
        return dist(p, a)
    t = max(0, min(1, ((px-ax)*dx + (py-ay)*dy)/(dx*dx+dy*dy)))
    return dist(p, (ax+t*dx, ay+t*dy))

def on_path(pos):
    return any(point_segment_distance(pos, PATH[i], PATH[i+1]) < 28 for i in range(len(PATH)-1))

class Monster:
    def __init__(self, wave, difficulty):
        spec = WAVES[wave]
        difficulty_spec = DIFFICULTIES[difficulty]
        self.x, self.y = PATH[0]
        self.segment = 0
        self.progress = 0.0
        self.max_hp = spec["hp"] * difficulty_spec["enemy_hp"] * random.uniform(.82, 1.18)
        self.hp = self.max_hp
        self.speed = spec["speed"] * difficulty_spec["enemy_speed"] * random.uniform(.88, 1.12)
        self.reward = spec["reward"]
        self.radius = random.choice([10, 11, 12]) + wave // 3
        self.kind = random.choice(["ghost", "slime", "zombie"]) if wave < 3 else random.choice(["ghost", "zombie", "pumpkin"])
        self.slime_color = random.choice([(150, 78, 210), (255, 150, 40)])
        self.phase = random.uniform(0, 6.28)
        self.dead = False
        self.reached = False
        self.hit_flash = 0

    def update(self, dt):
        if self.segment >= len(PATH)-1:
            self.reached = True
            return
        target = PATH[self.segment+1]
        dx, dy = target[0]-self.x, target[1]-self.y
        length = math.hypot(dx, dy)
        step = self.speed * dt * getattr(self, "slow_factor", 1)
        if length <= step:
            self.x, self.y = target
            self.segment += 1
            if self.segment >= len(PATH)-1:
                self.reached = True
        elif length:
            self.x += dx/length*step
            self.y += dy/length*step
        self.hit_flash = max(0, self.hit_flash-dt)

    def draw(self, surface):
        r = self.radius
        bob = int(math.sin(pygame.time.get_ticks()/140 + self.phase) * 2)
        x, y = int(self.x), int(self.y) + bob
        dark = (28, 14, 36)
        if self.kind == "ghost":
            body = (226, 230, 255)
            pygame.draw.circle(surface, body, (x, y-2), r)
            pygame.draw.rect(surface, body, (x-r, y-2, r*2, r))
            for i in range(3):
                pygame.draw.circle(surface, body, (x-r+int(r*(i*2+1)/3), y+r-2), max(3, r//3))
            pygame.draw.circle(surface, dark, (x-r//3, y-4), max(2, r//5))
            pygame.draw.circle(surface, dark, (x+r//3, y-4), max(2, r//5))
            pygame.draw.circle(surface, dark, (x, y+1), max(2, r//5), 1)
        elif self.kind == "slime":
            pygame.draw.ellipse(surface, self.slime_color, (x-r-2, y-int(r*.6), r*2+4, int(r*1.5)))
            light = tuple(min(255, c+55) for c in self.slime_color)
            pygame.draw.ellipse(surface, light, (x-r//2, y-int(r*.45), r//2, r//3))
            pygame.draw.circle(surface, dark, (x-r//3, y+1), max(2, r//5))
            pygame.draw.circle(surface, dark, (x+r//3, y+1), max(2, r//5))
        elif self.kind == "zombie":
            pygame.draw.rect(surface, (74, 92, 128), (x-r//2-1, y+r//3, r+2, int(r*.9)), border_radius=3)
            pygame.draw.rect(surface, (118, 168, 96), (x-r-2, y+r//3, 4, r//2+2))   # braços
            pygame.draw.rect(surface, (118, 168, 96), (x+r-2, y+r//3, 4, r//2+2))
            pygame.draw.circle(surface, (122, 176, 100), (x, y-2), r-1)
            pygame.draw.circle(surface, (220, 60, 60), (x-r//3, y-4), max(2, r//5))
            pygame.draw.circle(surface, (220, 60, 60), (x+r//3, y-4), max(2, r//5))
            pygame.draw.line(surface, dark, (x-r//3, y+r//3), (x+r//3, y+r//3), 2)
        else:
            draw_pumpkin(surface, x, y, r, face=True)
            pygame.draw.rect(surface, (118, 168, 96), (x-r-3, y+2, 4, r//2))
            pygame.draw.rect(surface, (118, 168, 96), (x+r-1, y+2, 4, r//2))
        if self.hit_flash > 0:
            pygame.draw.circle(surface, WHITE, (x, y), r+2, 3)
        # barra de vida
        y0 = int(self.y)
        w = 30
        pygame.draw.rect(surface, (38, 24, 52), (x-w//2, y0-r-11, w, 4), border_radius=2)
        pygame.draw.rect(surface, MINT, (x-w//2, y0-r-11, int(w*max(0, self.hp/self.max_hp)), 4), border_radius=2)

class AlliedMinion:
    def __init__(self, pos, damage):
        self.x, self.y = pos
        self.hp = 30
        self.radius = 8
        self.speed = 112
        self.damage = damage
        self.attack_rate = 0.8
        self.attack_cooldown = 0
        self.lifetime = 8
        self.target = None
        self.dead = False

    def update(self, dt, enemies):
        self.lifetime -= dt
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        if self.hp <= 0 or self.lifetime <= 0:
            self.dead = True
            return
        candidates = [e for e in enemies if not e.dead and not e.reached]
        if not candidates:
            return
        self.target = min(candidates, key=lambda e: dist((self.x, self.y), (e.x, e.y)))
        dx, dy = self.target.x - self.x, self.target.y - self.y
        length = math.hypot(dx, dy)
        if length > self.radius + self.target.radius + 3:
            step = min(length - self.radius - self.target.radius - 3, self.speed * dt)
            self.x += dx / length * step
            self.y += dy / length * step
        elif self.attack_cooldown <= 0:
            self.target.hp -= self.damage
            self.target.hit_flash = .1
            if self.target.hp <= 0:
                self.target.dead = True
            self.hp -= 10
            self.attack_cooldown = self.attack_rate
        if self.hp <= 0 or self.lifetime <= 0:
            self.dead = True

    def draw(self, surface):
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(surface, (28, 20, 40), (x, y), self.radius + 2)
        pygame.draw.circle(surface, (176, 230, 170), (x, y), self.radius)
        pygame.draw.circle(surface, (35, 45, 48), (x - 3, y - 1), 1)
        pygame.draw.circle(surface, (35, 45, 48), (x + 3, y - 1), 1)


class Tower:
    def __init__(self, pos, kind, rate_multiplier=1.0):
        spec = TOWER_TYPES[kind]
        self.x, self.y = pos
        self.kind = kind
        self.level = 1
        self.range = spec["range"]
        self.damage = spec["damage"]
        self.rate = spec["rate"] * rate_multiplier
        self.cooldown = random.random() * .2
        self.color = spec["color"]
        self.cost = spec["cost"]
        self.target = None
        self.angle = 0

    def upgrade(self):
        self.level += 1
        self.damage *= 1.42
        self.range += 13
        self.rate *= .88

    def update(self, dt, enemies, bullets, minions):
        self.cooldown = max(0, self.cooldown-dt)
        candidates = [e for e in enemies if not e.dead and not e.reached and dist((self.x,self.y),(e.x,e.y)) <= self.range]
        if candidates:
            self.target = max(candidates, key=lambda e: e.segment + e.progress)
            self.angle = math.atan2(self.target.y-self.y, self.target.x-self.x)
            if self.cooldown <= 0:
                behavior = TOWER_TYPES[self.kind].get("behavior")
                if behavior == "summon":
                    minions.append(AlliedMinion((self.x, self.y), self.damage))
                else:
                    bullets.append(Bullet((self.x,self.y), self.target, self.damage, self.color,
                                          TOWER_TYPES[self.kind].get("area", 0),
                                          TOWER_TYPES[self.kind].get("bullet_speed", 420)))
                self.cooldown = self.rate
        else:
            self.target = None

    def draw(self, surface, selected=False):
        x, y = int(self.x), int(self.y)
        if selected:
            pygame.draw.circle(surface, self.color, (x, y), int(self.range), 1)
        pygame.draw.circle(surface, (42, 26, 54), (x, y), 20)
        pygame.draw.circle(surface, self.color, (x, y), 20, 3)
        tip = (x+int(math.cos(self.angle)*20), y+int(math.sin(self.angle)*20))
        pygame.draw.line(surface, self.color, (x, y), tip, 4)
        pygame.draw.circle(surface, WHITE, tip, 3)
        if self.kind == 0:      # Espantalho
            pygame.draw.circle(surface, (228, 198, 120), (x, y+2), 7)
            pygame.draw.rect(surface, (120, 80, 44), (x-10, y-5, 20, 3))
            pygame.draw.rect(surface, (140, 94, 52), (x-6, y-13, 12, 9), border_radius=2)
            pygame.draw.circle(surface, (40, 24, 30), (x-3, y+1), 1)
            pygame.draw.circle(surface, (40, 24, 30), (x+3, y+1), 1)
        elif self.kind == 1:    # Gárgula
            pygame.draw.polygon(surface, (70, 92, 78), [(x-14, y-8), (x-6, y-2), (x-6, y+6), (x-15, y+2)])
            pygame.draw.polygon(surface, (70, 92, 78), [(x+14, y-8), (x+6, y-2), (x+6, y+6), (x+15, y+2)])
            pygame.draw.ellipse(surface, (112, 140, 118), (x-7, y-8, 14, 17))
            pygame.draw.polygon(surface, (80, 104, 88), [(x-6, y-7), (x-4, y-13), (x-1, y-7)])
            pygame.draw.polygon(surface, (80, 104, 88), [(x+6, y-7), (x+4, y-13), (x+1, y-7)])
            pygame.draw.circle(surface, MINT, (x-3, y-2), 2)
            pygame.draw.circle(surface, MINT, (x+3, y-2), 2)
        elif self.kind == 2:    # Lápide
            pygame.draw.rect(surface, (118, 120, 140), (x-10, y-9, 20, 19), border_top_left_radius=8, border_top_right_radius=8)
            pygame.draw.line(surface, (64, 66, 84), (x, y-5), (x, y+4), 2)
            pygame.draw.line(surface, (64, 66, 84), (x-4, y-2), (x+4, y-2), 2)
        elif self.kind == 3:    # Milho
            pygame.draw.ellipse(surface, (255, 218, 76), (x-7, y-12, 14, 24))
            pygame.draw.line(surface, (104, 160, 68), (x-10, y+8), (x-5, y-4), 3)
            pygame.draw.line(surface, (104, 160, 68), (x+10, y+8), (x+5, y-4), 3)
            for dy in (-6, 0, 6):
                pygame.draw.circle(surface, (255, 246, 164), (x, y+dy), 2)
        elif self.kind == 4:    # Corvo
            pygame.draw.ellipse(surface, (45, 38, 62), (x-9, y-5, 18, 13))
            pygame.draw.circle(surface, (58, 50, 78), (x+4, y-7), 6)
            pygame.draw.polygon(surface, (220, 170, 80), [(x+8, y-8), (x+15, y-5), (x+8, y-3)])
            pygame.draw.circle(surface, (255, 238, 160), (x+5, y-8), 1)
            pygame.draw.polygon(surface, (78, 64, 102), [(x-7, y), (x-15, y-7), (x-11, y+4)])
        else:                   # Abóbora
            draw_pumpkin(surface, x, y, 12, face=True)
        pygame.draw.circle(surface, (22, 12, 32), (x+15, y+15), 9)
        draw_text(str(self.level), x+11, y+7, WHITE, SMALL)

class Bullet:
    def __init__(self, start, target, damage, color, area_radius=0, speed=420):
        self.x, self.y = start
        self.target = target
        self.damage = damage
        self.color = color
        self.area_radius = area_radius
        self.speed = speed
        self.dead = False

    def update(self, dt, enemies):
        if self.target.dead or self.target.reached:
            self.dead = True
            return
        dx, dy = self.target.x-self.x, self.target.y-self.y
        length = math.hypot(dx,dy)
        if length < self.speed*dt + 5:
            for enemy in enemies:
                if (not enemy.dead and not enemy.reached
                        and (enemy is self.target or
                             (self.area_radius and dist((self.target.x, self.target.y), (enemy.x, enemy.y)) <= self.area_radius))):
                    enemy.hp -= self.damage
                    enemy.hit_flash = .12
                    if enemy.hp <= 0:
                        enemy.dead = True
            self.dead = True
        elif length:
            self.x += dx/length*self.speed*dt
            self.y += dy/length*self.speed*dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x),int(self.y)), 5)
        pygame.draw.circle(surface, WHITE, (int(self.x),int(self.y)), 2)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def format_duration(seconds):
    total = max(0, int(seconds))
    return f"{total // 60:02}:{total % 60:02}"

class Leaderboard:
    """Ranking local, preservado entre execuções do jogo."""
    LIMIT = 10

    def __init__(self):
        self.path = os.path.join(os.path.expanduser("~"), ".harvest-defense", "leaderboard.json")
        self.rankings = self.load()

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as ranking_file:
                data = json.load(ranking_file)
        except FileNotFoundError:
            return {key: [] for key in DIFFICULTIES}
        except (OSError, json.JSONDecodeError) as error:
            print(f"Não foi possível carregar o ranking: {error}", file=sys.stderr)
            return {key: [] for key in DIFFICULTIES}

        rankings = data.get("rankings") if isinstance(data, dict) else None
        if not isinstance(rankings, dict):
            print("Arquivo de ranking inválido; será iniciado um ranking vazio.", file=sys.stderr)
            return {key: [] for key in DIFFICULTIES}

        clean_rankings = {key: [] for key in DIFFICULTIES}
        for difficulty in DIFFICULTIES:
            entries = rankings.get(difficulty, [])
            if not isinstance(entries, list):
                continue
            valid_entries = [
                entry for entry in entries
                if isinstance(entry, dict)
                and isinstance(entry.get("score"), int)
                and isinstance(entry.get("date"), str)
                and isinstance(entry.get("time"), (int, float))
            ]
            valid_entries.sort(key=lambda entry: entry["score"], reverse=True)
            clean_rankings[difficulty] = valid_entries[:self.LIMIT]
        return clean_rankings

    def records_for(self, difficulty):
        return self.rankings[difficulty]

    def add_result(self, result):
        difficulty = result["difficulty"]
        self.rankings[difficulty].append(result)
        self.rankings[difficulty].sort(key=lambda entry: entry["score"], reverse=True)
        self.rankings[difficulty] = self.rankings[difficulty][:self.LIMIT]
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            temporary_path = self.path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as ranking_file:
                json.dump({"rankings": self.rankings}, ranking_file, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self.path)
        except OSError as error:
            print(f"Não foi possível salvar o ranking: {error}", file=sys.stderr)
            return str(error)
        return None

class DifficultyScreen:
    OPTIONS = [
        ("facil", MINT),
        ("normal", CYAN),
        ("dificil", RED),
    ]
    RECTS = [pygame.Rect(120 + index * 292, 310, 268, 170) for index in range(3)]

    def __init__(self):
        self.selected = 1

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected = (self.selected - 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected = (self.selected + 1) % len(self.OPTIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self.OPTIONS[self.selected][0]
            elif event.key == pygame.K_ESCAPE:
                return "back"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, rect in enumerate(self.RECTS):
                if rect.collidepoint(event.pos):
                    self.selected = index
                    return self.OPTIONS[index][0]
        return None

    def draw(self, background):
        background.draw()
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((8, 3, 16, 215))
        screen.blit(veil, (0, 0))
        title = BIG.render("ESCOLHA A DIFICULDADE", True, ORANGE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 205))
        for index, (key, color) in enumerate(self.OPTIONS):
            rect = self.RECTS[index]
            selected = index == self.selected
            pygame.draw.rect(screen, (44, 56, 40) if selected else PANEL, rect, border_radius=14)
            pygame.draw.rect(screen, color if selected else BORDER, rect, 3 if selected else 2, border_radius=14)
            label = DIFFICULTIES[key]["name"]
            label_surface = BIG.render(label, True, color)
            screen.blit(label_surface, (rect.centerx - label_surface.get_width() // 2, rect.y + 28))
            lines = {
                "facil": ["6 ondas", "Inimigos: mais fracos", "Multiplicador: 0,80x"],
                "normal": ["9 ondas", "Inimigos: força padrão", "Multiplicador: 1,00x"],
                "dificil": ["12 ondas", "Inimigos: reforçados", "Multiplicador: 1,25x"],
            }[key]
            for line_index, line in enumerate(lines):
                text = SMALL.render(line, True, WHITE if line_index == 0 else MUTED)
                screen.blit(text, (rect.centerx - text.get_width() // 2, rect.y + 78 + line_index * 24))
        subtitle = FONT.render("Setas / A-D e ENTER ou clique para confirmar", True, WHITE)
        screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, 520))

class TitleScreen:
    """Tela inicial: arte em 1100x720, texto piscando e brasas flutuando."""
    FADE_IN = 1.2

    def __init__(self):
        self.time = 0.0
        self.image = None
        path = os.path.join(BASE_DIR, "assets", "tela_inicial.png")
        try:
            img = pygame.image.load(path).convert()
            if img.get_size() != (WIDTH, HEIGHT):
                img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            self.image = img
        except (pygame.error, FileNotFoundError):
            self.image = None   # sem a imagem, usa o fundo de reserva
        rnd = random.Random(5)
        # brasas: [x, y, velocidade, fase, tamanho]
        self.embers = [[rnd.uniform(0, WIDTH), rnd.uniform(0, HEIGHT), rnd.uniform(14, 34),
                        rnd.uniform(0, 6.28), rnd.choice([1, 2, 2, 3])] for _ in range(36)]

    def update(self, dt):
        self.time += dt
        for e in self.embers:
            e[1] -= e[2] * dt
            e[0] += math.sin(self.time * 1.3 + e[3]) * 12 * dt
            if e[1] < -5:
                e[0], e[1] = random.uniform(0, WIDTH), HEIGHT + 5

    def draw(self):
        if self.image:
            screen.blit(self.image, (0, 0))
        else:
            screen.fill(BG)
            draw_outlined("HARVEST DEFENSE", HUGE, ORANGE, (WIDTH//2, HEIGHT//2 - 40))
            draw_outlined("Proteja a fazenda. Defenda a colheita.", FONT, WHITE, (WIDTH//2, HEIGHT//2 + 4))
        for x, y, _, ph, size in self.embers:
            glow = 0.5 + 0.5 * math.sin(self.time * 3 + ph)
            col = (255, int(120 + 90 * glow), 40)
            pygame.draw.circle(screen, col, (int(x), int(y)), size)
        if self.time > 0.8:
            pulse = 0.5 + 0.5 * math.sin((self.time - 0.8) * 4.2)
            draw_outlined("Aperte qualquer botão para iniciar", BIG, WHITE,
                          (WIDTH//2, 690), alpha=int(45 + 210 * pulse))
        if self.time < self.FADE_IN:
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.set_alpha(int(255 * (1 - self.time / self.FADE_IN)))
            screen.blit(fade, (0, 0))

# ---------- cenário (desenhado uma vez e reaproveitado) ----------
_MAP_CACHE = None

def build_map_surface():
    surf = pygame.Surface((WIDTH, HEIGHT))
    surf.fill(BG)
    pygame.draw.rect(surf, GRASS_A, MAP_RECT, border_radius=12)
    surf.set_clip(MAP_RECT)
    rnd = random.Random(11)
    for gx in range(MAP_RECT.left, MAP_RECT.right, 28):
        for gy in range(MAP_RECT.top, MAP_RECT.bottom, 28):
            if ((gx - MAP_RECT.left)//28 + (gy - MAP_RECT.top)//28) % 2:
                pygame.draw.rect(surf, GRASS_B, (gx, gy, 28, 28))
    for _ in range(220):   # tufos de grama
        gx, gy = rnd.randint(MAP_RECT.left, MAP_RECT.right), rnd.randint(MAP_RECT.top, MAP_RECT.bottom)
        pygame.draw.line(surf, (24, 52, 40), (gx, gy), (gx-2, gy-5), 1)
        pygame.draw.line(surf, (24, 52, 40), (gx, gy), (gx+2, gy-5), 1)
    # estrada de terra
    pygame.draw.lines(surf, DIRT_EDGE, False, PATH, 46)
    for px, py in PATH:
        pygame.draw.circle(surf, DIRT_EDGE, (px, py), 23)
    pygame.draw.lines(surf, DIRT, False, PATH, 38)
    for px, py in PATH:
        pygame.draw.circle(surf, DIRT, (px, py), 19)
    for _ in range(140):   # pedrinhas
        i = rnd.randrange(len(PATH)-1)
        a, b = PATH[i], PATH[i+1]
        t = rnd.random()
        px = a[0] + (b[0]-a[0])*t + rnd.uniform(-13, 13)
        py = a[1] + (b[1]-a[1])*t + rnd.uniform(-13, 13)
        pygame.draw.circle(surf, (132, 100, 72), (int(px), int(py)), rnd.choice([1, 2]))
    # decoração (fora da estrada)
    placed = 0
    tries = 0
    while placed < 34 and tries < 600:
        tries += 1
        x = rnd.randint(MAP_RECT.left + 16, MAP_RECT.right - 16)
        y = rnd.randint(MAP_RECT.top + 16, MAP_RECT.bottom - 16)
        if any(point_segment_distance((x, y), PATH[i], PATH[i+1]) < 52 for i in range(len(PATH)-1)):
            continue
        if dist((x, y), CORE) < 80:
            continue
        kind = rnd.choice(["pumpkin", "pumpkin", "hay", "tomb", "tree", "mush"])
        if kind == "pumpkin":
            draw_pumpkin(surf, x, y, rnd.choice([7, 8, 9]), face=rnd.random() < .5)
        elif kind == "hay":
            pygame.draw.rect(surf, (196, 160, 70), (x-11, y-8, 22, 16), border_radius=3)
            for k in (-5, 0, 5):
                pygame.draw.line(surf, (150, 118, 48), (x+k, y-8), (x+k, y+8), 1)
        elif kind == "tomb":
            pygame.draw.rect(surf, (110, 112, 128), (x-8, y-10, 16, 20), border_top_left_radius=8, border_top_right_radius=8)
            pygame.draw.line(surf, (70, 72, 88), (x, y-6), (x, y+2), 2)
            pygame.draw.line(surf, (70, 72, 88), (x-3, y-3), (x+3, y-3), 2)
        elif kind == "tree":
            pygame.draw.line(surf, (60, 40, 40), (x, y+14), (x, y-8), 5)
            for dx, dy in ((-12, -18), (10, -16), (-6, -22), (4, -24)):
                pygame.draw.line(surf, (60, 40, 40), (x, y-6), (x+dx, y+dy), 2)
        else:
            pygame.draw.rect(surf, (230, 220, 210), (x-1, y-2, 3, 6))
            pygame.draw.ellipse(surf, (170, 70, 200), (x-6, y-8, 12, 8))
        placed += 1
    surf.set_clip(None)
    pygame.draw.rect(surf, BORDER, MAP_RECT, 2, border_radius=12)
    return surf

class Game:
    def __init__(self, difficulty="normal"):
        self.difficulty = difficulty
        self.difficulty_spec = DIFFICULTIES[difficulty]
        self.money = 320
        self.core_hp = 100
        self.towers = []
        self.enemies = []
        self.minions = []
        self.bullets = []
        self.particles = []
        self.wave = 0
        self.spawned = 0
        self.spawn_timer = 0
        self.wave_active = False
        self.wave_wait = False
        self.selected_kind = 0
        self.selected_tower = None
        self.message = "ESPAÇO: iniciar fase 1"
        self.message_time = 5
        self.special_cooldown = 0
        self.special_flash = 0
        self.paused = False
        self.tree_open = False
        self.unlocked = [True, False, False]
        self.tree_costs = [220, 360, 520]
        self.bonus_damage = 1.0
        self.bonus_income = 1.0
        self.fast_fire = 1.0
        self.completed = False
        self.lost = False
        self.total_kills = 0
        self.total_upgrades = 0
        self.skills_purchased = 0
        self.elapsed_seconds = 0
        self.run_started = False
        self.score_details = None
        self.ranking_save_error = None

    def notify(self, text, seconds=3):
        self.message = text
        self.message_time = seconds

    def start_wave(self):
        if (not self.wave_active and self.wave < self.difficulty_spec["wave_count"]
                and not self.completed and not self.lost):
            self.run_started = True
            self.wave_active = True
            self.spawned = 0
            self.spawn_timer = .2
            self.wave_wait = False
            self.notify(f"FASE {self.wave+1}: {WAVES[self.wave]['name']}", 3)

    def use_special(self):
        if self.special_cooldown > 0:
            self.notify("O pulso lunar está recarregando.")
            return
        count = 0
        for e in self.enemies:
            if not e.dead and not e.reached:
                e.hp -= 42 + self.wave*8
                e.hit_flash = .15
                if e.hp <= 0:
                    e.dead = True
                    count += 1
        self.special_cooldown = 12
        self.special_flash = .4
        self.notify(f"Pulso lunar! {count} monstro(s) eliminado(s).", 2)

    def buy_tower(self, pos):
        if not MAP_RECT.collidepoint(pos) or on_path(pos):
            self.notify("Posicione a torre fora da estrada dos monstros.")
            return
        if any(dist(pos,(t.x,t.y)) < 40 for t in self.towers):
            self.notify("As torres precisam de espaço entre si.")
            return
        spec = TOWER_TYPES[self.selected_kind]
        if self.money < spec["cost"]:
            self.notify("Abóboras insuficientes para essa torre.")
            return
        self.money -= spec["cost"]
        self.towers.append(Tower(pos, self.selected_kind, self.fast_fire))
        self.selected_tower = self.towers[-1]
        self.notify(f"Torre posicionada: {spec['name']}!")

    def upgrade_selected(self):
        t = self.selected_tower
        if not t:
            self.notify("Selecione uma torre primeiro.")
            return
        cost = int(t.cost * (0.8 + .65*t.level))
        if self.money < cost:
            self.notify(f"Melhoria custa {fmt_money(cost)} abóboras.")
            return
        self.money -= cost
        t.upgrade()
        self.total_upgrades += 1
        self.notify(f"Torre melhorada para nível {t.level}.")

    def buy_skill(self, index):
        if self.unlocked[index]:
            self.notify("Esse caminho já está desbloqueado.")
            return
        cost = self.tree_costs[index]
        if self.money < cost:
            self.notify(f"Árvore de habilidades: precisa de {fmt_money(cost)} abóboras.")
            return
        self.money -= cost
        self.unlocked[index] = True
        self.skills_purchased += 1
        if index == 0:
            self.bonus_damage = 1.35
        elif index == 1:
            self.bonus_income = 1.3
        else:
            self.fast_fire = .78
            for t in self.towers:
                t.rate *= .78
        self.notify(["Amuleto sombrio: dano +35%.", "Colheita farta: recompensa +30%.", "Ritmo de batalha: torres atacam mais rápido."][index], 4)

    def calculate_score(self):
        health_points = round(5000 * max(0, min(self.core_hp, 100)) / 100)
        time_limit = 4 * 60 * self.difficulty_spec["wave_count"]
        upgrade_target = 2 * self.difficulty_spec["wave_count"]
        time_points = round(2000 * max(0, 1 - self.elapsed_seconds / time_limit))
        upgrade_points = round(1000 * min(self.total_upgrades / upgrade_target, 1))
        talent_points = round(500 * min(self.skills_purchased / 2, 1))
        savings_points = round(1500 * min(self.money / 1000, 1))
        base_score = health_points + time_points + upgrade_points + talent_points + savings_points
        score = round(base_score * self.difficulty_spec["score_multiplier"])
        return {
            "health": health_points,
            "time": time_points,
            "upgrades": upgrade_points,
            "talents": talent_points,
            "savings": savings_points,
            "multiplier": self.difficulty_spec["score_multiplier"],
            "score": score,
        }

    def save_completed_score(self):
        self.score_details = self.calculate_score()
        result = {
            "player": "Fazendeiro",
            "difficulty": self.difficulty,
            "score": self.score_details["score"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "time": round(self.elapsed_seconds),
            "core_hp": self.core_hp,
            "upgrades": self.total_upgrades,
            "talents": self.skills_purchased,
            "money": self.money,
        }
        self.ranking_save_error = leaderboard.add_result(result)

    def update(self, dt):
        self.message_time = max(0, self.message_time-dt)
        self.special_cooldown = max(0, self.special_cooldown-dt)
        self.special_flash = max(0, self.special_flash-dt)
        if self.paused or self.tree_open or self.completed or self.lost:
            return
        if self.run_started:
            self.elapsed_seconds += dt
        if self.wave_active:
            self.spawn_timer -= dt
            spec = WAVES[self.wave]
            if self.spawned < spec["count"] and self.spawn_timer <= 0:
                self.enemies.append(Monster(self.wave, self.difficulty))
                self.spawned += 1
                self.spawn_timer = max(.24, .86 - self.wave*.1)
        for m in self.minions:
            m.update(dt, self.enemies)
        self.minions = [m for m in self.minions if not m.dead]
        for e in self.enemies:
            if not e.dead and not e.reached:
                e.slow_factor = .3 if any(
                    dist((m.x, m.y), (e.x, e.y)) <= m.radius + e.radius + 3
                    for m in self.minions
                ) else 1
                e.update(dt)
            if e.reached and not e.dead:
                e.dead = True
                self.core_hp -= int((10 + self.wave*2) * self.difficulty_spec["core_damage"])
                self.notify("Um monstro invadiu o celeiro! Integridade reduzida.", 2)
                if self.core_hp <= 0:
                    self.lost = True
        for t in self.towers:
            t.damage = TOWER_TYPES[t.kind]["damage"] * (1 + .42*(t.level-1)) * self.bonus_damage
            t.update(dt, self.enemies, self.bullets, self.minions)
        for b in self.bullets:
            b.update(dt, self.enemies)
        self.bullets = [b for b in self.bullets if not b.dead]
        for e in self.enemies:
            if e.dead and not getattr(e, "rewarded", False):
                if not e.reached:
                    self.money += int(e.reward*self.bonus_income)
                    self.total_kills += 1
                e.rewarded = True
                for _ in range(5):
                    self.particles.append([e.x,e.y,random.uniform(-70,70),random.uniform(-70,70),.35,e.kind])
        self.enemies = [e for e in self.enemies if not e.dead]
        if (self.wave_active and not self.lost
                and self.spawned >= WAVES[self.wave]["count"] and not self.enemies):
            self.wave_active = False
            self.wave += 1
            bonus = 80 + self.wave*35
            self.money += bonus
            self.notify(f"Fase concluída! Bônus: {fmt_money(bonus)} abóboras. Pressione ESPAÇO.", 5)
            if self.wave >= self.difficulty_spec["wave_count"]:
                self.completed = True
                self.save_completed_score()
                self.notify("FAZENDA PROTEGIDA — Você venceu!", 10)
        for p in self.particles:
            p[0] += p[2]*dt; p[1] += p[3]*dt; p[4] -= dt
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw_barn(self):
        cx, cy = CORE
        pygame.draw.circle(screen, (46, 30, 62), CORE, 38)
        pygame.draw.rect(screen, (140, 42, 44), (cx-22, cy-12, 44, 34), border_radius=3)
        pygame.draw.polygon(screen, (92, 28, 32), [(cx-27, cy-10), (cx, cy-34), (cx+27, cy-10)])
        pygame.draw.polygon(screen, (60, 18, 22), [(cx-27, cy-10), (cx, cy-34), (cx+27, cy-10)], 2)
        pygame.draw.rect(screen, (70, 24, 28), (cx-8, cy+3, 16, 19))
        pygame.draw.line(screen, (230, 210, 190), (cx-8, cy+3), (cx+8, cy+22), 1)
        pygame.draw.line(screen, (230, 210, 190), (cx+8, cy+3), (cx-8, cy+22), 1)
        pygame.draw.circle(screen, (255, 220, 120), (cx, cy-14), 4)
        ok = self.core_hp > 35
        w = 50
        pygame.draw.rect(screen, (38, 24, 52), (cx-w//2, cy-48, w, 6), border_radius=3)
        pygame.draw.rect(screen, MINT if ok else RED, (cx-w//2, cy-48, int(w*max(0, self.core_hp)/100), 6), border_radius=3)

    def draw_map(self):
        global _MAP_CACHE
        if _MAP_CACHE is None:
            _MAP_CACHE = build_map_surface()
        screen.blit(_MAP_CACHE, (0, 0))
        self.draw_barn()
        if self.special_flash > 0:
            pygame.draw.circle(screen, (255, 240, 170), CORE, int(50+(0.4-self.special_flash)*220), 3)
        for t in self.towers:
            t.draw(screen, t is self.selected_tower)
        for m in self.minions:
            m.draw(screen)
        for e in self.enemies:
            e.draw(screen)
        for b in self.bullets:
            b.draw(screen)
        for p in self.particles:
            color = KIND_COLORS.get(p[5], MINT)
            pygame.draw.circle(screen, color, (int(p[0]),int(p[1])), max(1,int(4*p[4]/.35)))

    def draw_tree(self):
        overlay = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        overlay.fill((8,2,16,220))
        screen.blit(overlay,(0,0))
        pygame.draw.rect(screen, PANEL, (245,145,610,430), border_radius=16)
        pygame.draw.rect(screen, BORDER, (245,145,610,430), 2, border_radius=16)
        draw_text("ÁRVORE DE HABILIDADES", 295, 168, ORANGE, BIG)
        draw_text("Escolha caminhos diferentes para adaptar sua defesa.", 295, 207, MUTED, SMALL)
        nodes = [
            (280,265,"1  AMULETO SOMBRIO","Dano das torres +35%",self.unlocked[0],self.tree_costs[0]),
            (280,350,"2  COLHEITA FARTA","Recompensas +30%",self.unlocked[1],self.tree_costs[1]),
            (280,435,"3  RITMO DE BATALHA","Torres atacam mais rápido",self.unlocked[2],self.tree_costs[2]),
        ]
        for x,y,title,desc,owned,cost in nodes:
            pygame.draw.rect(screen,(44,56,40) if owned else (36,24,54),(x,y,535,65),border_radius=9)
            pygame.draw.rect(screen,MINT if owned else BORDER,(x,y,535,65),2,border_radius=9)
            draw_text(title,x+16,y+9,MINT if owned else WHITE,FONT)
            draw_text(desc,x+16,y+37,MUTED,SMALL)
            draw_text("DESBLOQUEADO" if owned else f"{fmt_money(cost)} abóboras",x+350,y+24,MINT if owned else ORANGE,SMALL)
        draw_text("Clique em um caminho para desbloquear. ESC para voltar.", 295, 530, MUTED, SMALL)

    def draw_ui(self):
        pygame.draw.rect(screen, PANEL, (0,0,WIDTH,68))
        pygame.draw.line(screen, BORDER, (0,68),(WIDTH,68),2)
        draw_pumpkin(screen, 38, 33, 12, face=True)
        draw_text("HARVEST DEFENSE", 58, 18, ORANGE, BIG)
        draw_pumpkin(screen, 346, 27, 8)
        draw_text(f"ABÓBORAS  {fmt_money(self.money)}", 362, 16, WHITE, FONT)
        draw_text(f"CELEIRO  {self.core_hp}%", 545, 16, MINT if self.core_hp>35 else RED, FONT)
        wave_count = self.difficulty_spec["wave_count"]
        draw_text(f"FASE  {min(self.wave+1,wave_count)}/{wave_count}", 705, 16, WHITE, FONT)
        draw_text(f"ELIMINADOS  {self.total_kills}", 845, 16, CYAN, FONT)
        # Painel inferior
        pygame.draw.rect(screen, PANEL, (0,565,WIDTH,155))
        pygame.draw.line(screen, BORDER, (0,565),(WIDTH,565),2)
        draw_text("TORRES | 1-6 selecionam | U: melhoria", 24, 577, MUTED, SMALL)
        pulse_status = "PRONTO" if self.special_cooldown <= 0 else f"{int(self.special_cooldown)}s"
        draw_text(f"ESPAÇO: onda | F: pulso ({pulse_status}) | T: árvore", 365, 577, WHITE, SMALL)
        if self.selected_tower:
            t = self.selected_tower
            cost = int(t.cost * (0.8 + .65*t.level))
            draw_text(f"{TOWER_TYPES[t.kind]['name']} Nv.{t.level} | melhoria {fmt_money(cost)}", 735, 577, t.color, SMALL)
        else:
            draw_text("Clique numa torre para selecioná-la", 735, 577, MUTED, SMALL)
        for i,spec in enumerate(TOWER_TYPES):
            x = 24+i*174
            selected = self.selected_kind == i
            pygame.draw.rect(screen,(52,34,72) if selected else (36,24,54),(x,602,164,70),border_radius=9)
            pygame.draw.rect(screen,spec["color"] if selected else BORDER,(x,602,164,70),2,border_radius=9)
            draw_text(f"{i+1}. {spec['name']}",x+8,607,spec["color"],FONT)
            draw_text(f"{fmt_money(spec['cost'])} abóboras",x+8,630,WHITE,SMALL)
            draw_text(spec["desc"],x+8,650,MUTED,SMALL)
        if self.message_time > 0:
            text = FONT.render(self.message, True, WHITE)
            box = pygame.Rect(WIDTH//2-text.get_width()//2-14, 82, text.get_width()+28, 32)
            pygame.draw.rect(screen,(40,26,60),box,border_radius=8)
            pygame.draw.rect(screen,BORDER,box,1,border_radius=8)
            screen.blit(text,(box.x+14,box.y+6))
        if self.completed or self.lost:
            veil=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); veil.fill((8,3,16,205)); screen.blit(veil,(0,0))
            title = "FAZENDA PROTEGIDA!" if self.completed else "A COLHEITA FOI PERDIDA"
            col = MINT if self.completed else RED
            txt = HUGE.render(title, True, col)
            screen.blit(txt, (WIDTH//2-txt.get_width()//2, 225 if self.completed else 260))
            if self.completed:
                details = self.score_details
                if details is None:
                    raise RuntimeError("Vitória sem score calculado.")
                score_text = BIG.render(f"SCORE GLOBAL: {details['score']:,}".replace(",", "."), True, ORANGE)
                screen.blit(score_text, (WIDTH//2-score_text.get_width()//2, 282))
                score_lines = [
                    f"Integridade {details['health']} / 5.000  |  Tempo {details['time']} / 2.000  |  Melhorias {details['upgrades']} / 1.000",
                    f"Talentos {details['talents']} / 500  |  Economia {details['savings']} / 1.500  |  Dificuldade {self.difficulty_spec['name']}",
                    f"Tempo de partida: {format_duration(self.elapsed_seconds)}  |  Multiplicador: {details['multiplier']:.2f}x",
                ]
                for index, line in enumerate(score_lines):
                    text = SMALL.render(line, True, WHITE)
                    screen.blit(text, (WIDTH//2-text.get_width()//2, 330 + index*26))
                if self.ranking_save_error:
                    warning = SMALL.render("Não foi possível salvar o ranking; veja o terminal.", True, RED)
                    screen.blit(warning, (WIDTH//2-warning.get_width()//2, 420))
                prompt = FONT.render("ENTER: jogar novamente  |  R: ranking  |  ESC: menu", True, WHITE)
            else:
                prompt = FONT.render("ENTER para jogar novamente  |  ESC para o menu", True, WHITE)
            screen.blit(prompt, (WIDTH//2-prompt.get_width()//2, 485 if self.completed else 315))

    def draw(self):
        screen.fill(BG)
        self.draw_map()
        self.draw_ui()
        if self.tree_open:
            self.draw_tree()

def toggle_fullscreen():
    try:
        pygame.display.toggle_fullscreen()
    except pygame.error:
        pass

def is_fullscreen():
    surf = pygame.display.get_surface()
    return bool(surf and surf.get_flags() & pygame.FULLSCREEN)


class MenuScreen:
    """Menu principal: arte com os botões; seleção por mouse ou teclado."""
    ITEMS = [("JOGAR", "play"), ("CONFIGURAÇÕES", "settings"), ("COMO JOGAR", "howto"), ("SAIR", "quit")]
    RECTS = [pygame.Rect(51, 325, 247, 45), pygame.Rect(51, 379, 247, 44),
             pygame.Rect(51, 431, 247, 44), pygame.Rect(51, 485, 247, 41)]
    FADE_IN = 0.5
    GREEN = (120, 255, 130)

    def __init__(self):
        self.time = 0.0
        self.sel = 0
        self.panel = None   # None | "settings" | "howto"
        self.image = None
        path = os.path.join(BASE_DIR, "assets", "menu_principal.png")
        try:
            img = pygame.image.load(path).convert()
            if img.get_size() != (WIDTH, HEIGHT):
                img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            self.image = img
        except (pygame.error, FileNotFoundError):
            self.image = None

    def enter(self):
        self.time = 0.0
        self.panel = None

    def update(self, dt):
        self.time += dt

    def activate(self, i):
        action = self.ITEMS[i][1]
        if action in ("play", "quit"):
            return action
        self.panel = action
        return None

    def handle_event(self, event):
        if self.panel:
            back = False
            if event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_BACKSPACE):
                back = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.panel == "settings" and self.toggle_rect().collidepoint(event.pos):
                    toggle_fullscreen()
                elif self.back_rect().collidepoint(event.pos) or not self.panel_rect().collidepoint(event.pos):
                    back = True
            if back:
                self.panel = None
            return None
        if event.type == pygame.MOUSEMOTION:
            for i, r in enumerate(self.RECTS):
                if r.collidepoint(event.pos):
                    self.sel = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, r in enumerate(self.RECTS):
                if r.collidepoint(event.pos):
                    self.sel = i
                    return self.activate(i)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.panel = "ranking"
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.sel = (self.sel - 1) % len(self.ITEMS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.sel = (self.sel + 1) % len(self.ITEMS)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return self.activate(self.sel)
            elif event.key == pygame.K_ESCAPE:
                return "title"
        return None

    # --- painéis ---
    def panel_rect(self):
        return pygame.Rect(190, 60, 720, 600) if self.panel in ("howto", "ranking") else pygame.Rect(320, 200, 460, 330)

    def back_rect(self):
        r = self.panel_rect()
        return pygame.Rect(r.centerx - 70, r.bottom - 58, 140, 38)

    def toggle_rect(self):
        r = self.panel_rect()
        return pygame.Rect(r.right - 190, r.top + 98, 150, 38)

    def draw_panel_frame(self, title):
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((8, 3, 16, 200))
        screen.blit(veil, (0, 0))
        r = self.panel_rect()
        pygame.draw.rect(screen, PANEL, r, border_radius=16)
        pygame.draw.rect(screen, BORDER, r, 2, border_radius=16)
        draw_text(title, r.x + 28, r.y + 22, ORANGE, BIG)
        b = self.back_rect()
        pygame.draw.rect(screen, (52, 34, 72), b, border_radius=9)
        pygame.draw.rect(screen, MINT, b, 2, border_radius=9)
        t = FONT.render("Voltar", True, WHITE)
        screen.blit(t, (b.centerx - t.get_width()//2, b.centery - t.get_height()//2))

    def draw_howto(self):
        self.draw_panel_frame("COMO JOGAR")
        x, y = 218, 134
        draw_text("OBJETIVO", x, y, MINT, FONT)
        draw_text("Proteja o celeiro até o fim da campanha. Se a integridade", x, y+26, WHITE, SMALL)
        draw_text("do celeiro chegar a 0%, a colheita é perdida.", x, y+46, WHITE, SMALL)
        draw_text("Fácil: 6 ondas | Médio: 9 ondas | Difícil: 12 ondas.", x, y+66, ORANGE, SMALL)
        draw_text("TORRES", x, y+96, MINT, FONT)
        for i, spec in enumerate(TOWER_TYPES):
            ty = y + 124 + i*20
            pygame.draw.circle(screen, spec["color"], (x+8, ty+8), 6)
            draw_text(f"{spec['name']} — {spec['desc']} (custo {spec['cost']})", x+24, ty, WHITE, SMALL)
        draw_text("CONTROLES", x, y+272, MINT, FONT)
        controls = [
            ("Clique no painel / 1-6", "escolher a torre"),
            ("Clique no mapa", "posicionar (fora da estrada)"),
            ("Clique em uma torre", "selecionar e ver o alcance"),
            ("U", "melhorar a torre selecionada"),
            ("ESPAÇO", "iniciar a próxima onda"),
            ("F", "pulso lunar (recarrega)"),
            ("T  e  1 / 2 / 3", "árvore de habilidades"),
            ("ESC", "voltar ao menu"),
        ]
        for i, (k, d) in enumerate(controls):
            cy = y + 302 + i*20
            draw_text(k, x, cy, ORANGE, SMALL)
            draw_text(d, x+250, cy, WHITE, SMALL)
        draw_text("Moedas: abóboras. Ganhe ao derrotar monstros e concluir ondas.", x, y+467, MUTED, SMALL)
        draw_text("R no menu: consultar o ranking local de cada dificuldade.", x, y+487, MUTED, SMALL)

    def draw_ranking(self):
        self.draw_panel_frame("RANKING LOCAL")
        draw_text("Vitórias ordenadas por score — as 3 melhores de cada dificuldade.", 218, 132, MUTED, SMALL)
        columns = [218, 274, 390, 500, 588, 710]
        headers = ["#", "JOGADOR", "SCORE", "TEMPO", "CELEIRO", "DATA"]
        for x, header in zip(columns, headers):
            draw_text(header, x, 174, ORANGE, SMALL)
        row = 0
        for difficulty, info in DIFFICULTIES.items():
            difficulty_color = RED if info["score_multiplier"] >= 1.25 else CYAN
            draw_text(info["name"], 218, 205 + row * 28, difficulty_color, SMALL)
            row += 1
            records = leaderboard.records_for(difficulty)
            if not records:
                draw_text("Sem vitórias registradas", 250, 205 + row * 28, MUTED, SMALL)
                row += 1
                continue
            for place, entry in enumerate(records[:3], 1):
                y = 205 + row * 28
                draw_text(str(place), columns[0], y, WHITE, SMALL)
                draw_text(entry.get("player", "Fazendeiro")[:14], columns[1], y, WHITE, SMALL)
                draw_text(f"{entry['score']:,}".replace(",", "."), columns[2], y, MINT, SMALL)
                draw_text(format_duration(entry["time"]), columns[3], y, WHITE, SMALL)
                draw_text(f"{entry.get('core_hp', 0)}%", columns[4], y, WHITE, SMALL)
                draw_text(entry.get("date", "")[:16], columns[5], y, MUTED, SMALL)
                row += 1
        draw_text("O ranking fica salvo neste computador; não é enviado a um servidor.", 218, 558, MUTED, SMALL)

    def draw_settings(self):
        self.draw_panel_frame("CONFIGURAÇÕES")
        r = self.panel_rect()
        draw_text("Tela cheia  (F11)", r.x + 28, r.y + 108, WHITE, FONT)
        tg = self.toggle_rect()
        on = is_fullscreen()
        pygame.draw.rect(screen, (44, 56, 40) if on else (36, 24, 54), tg, border_radius=9)
        pygame.draw.rect(screen, MINT if on else BORDER, tg, 2, border_radius=9)
        t = FONT.render("LIGADA" if on else "DESLIGADA", True, MINT if on else MUTED)
        screen.blit(t, (tg.centerx - t.get_width()//2, tg.centery - t.get_height()//2))
        draw_text("Som", r.x + 28, r.y + 168, WHITE, FONT)
        draw_text("indisponível nesta versão", r.right - 250, r.y + 171, MUTED, SMALL)

    def draw_selection(self):
        rect = self.RECTS[self.sel]
        pulse = 0.5 + 0.5 * math.sin(self.time * 5)
        layer = pygame.Surface((rect.w + 40, rect.h + 40), pygame.SRCALPHA)
        base = pygame.Rect(20, 20, rect.w, rect.h)
        for k in range(5, 0, -1):
            a = int((26 + 22 * pulse) * (6 - k) / 5)
            pygame.draw.rect(layer, (*self.GREEN, a), base.inflate(k*3, k*3), 2, border_radius=9 + k)
        pygame.draw.rect(layer, (*self.GREEN, int(34 + 22 * pulse)), base, border_radius=8)
        pygame.draw.rect(layer, (*self.GREEN, 255), base.inflate(2, 2), 2, border_radius=9)
        screen.blit(layer, (rect.x - 20, rect.y - 20))

    def draw(self):
        if self.image:
            screen.blit(self.image, (0, 0))
        else:
            screen.fill(BG)
            draw_outlined("HARVEST DEFENSE", HUGE, ORANGE, (WIDTH//2, 120))
            for (label, _), r in zip(self.ITEMS, self.RECTS):
                pygame.draw.rect(screen, (92, 62, 44), r, border_radius=8)
                draw_outlined(label, FONT, WHITE, r.center)
        self.draw_selection()
        if self.panel == "howto":
            self.draw_howto()
        elif self.panel == "ranking":
            self.draw_ranking()
        elif self.panel == "settings":
            self.draw_settings()
        if self.panel is None:
            draw_text("R: ranking local", 58, 548, WHITE, SMALL)
        if self.time < self.FADE_IN:
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.set_alpha(int(255 * (1 - self.time / self.FADE_IN)))
            screen.blit(fade, (0, 0))


leaderboard = Leaderboard()
difficulty_screen = DifficultyScreen()
game = Game()
title = TitleScreen()
menu = MenuScreen()
state = "title"   # "title" -> tela inicial | "menu" -> menu principal | "difficulty" -> escolha | "playing" -> jogo
running = True
while running:
    dt = min(clock.tick(60)/1000, .04)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            toggle_fullscreen()
            continue
        if state == "title":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    menu.enter()
                    state = "menu"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                menu.enter()
                state = "menu"
            continue
        if state == "menu":
            action = menu.handle_event(event)
            if action == "play":
                state = "difficulty"
            elif action == "quit":
                running = False
            elif action == "title":
                title = TitleScreen()
                state = "title"
            continue
        if state == "difficulty":
            difficulty = difficulty_screen.handle_event(event)
            if difficulty == "back":
                state = "menu"
            elif difficulty:
                game = Game(difficulty)
                state = "playing"
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.tree_open:
                    game.tree_open = False
                else:
                    menu.enter()
                    state = "menu"
            elif game.completed or game.lost:
                if event.key == pygame.K_RETURN:
                    game = Game(game.difficulty)
                elif event.key == pygame.K_r and game.completed:
                    menu.enter()
                    menu.panel = "ranking"
                    state = "menu"
            elif game.tree_open:
                if event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                    game.buy_skill(event.key-pygame.K_1)
                elif event.key == pygame.K_t:
                    game.tree_open=False
            else:
                if event.key == pygame.K_SPACE:
                    game.start_wave()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                    game.selected_kind = event.key - pygame.K_1
                elif event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
                    game.selected_kind = {pygame.K_q: 0, pygame.K_w: 1, pygame.K_e: 2}[event.key]
                elif event.key == pygame.K_u:
                    game.upgrade_selected()
                elif event.key == pygame.K_f:
                    game.use_special()
                elif event.key == pygame.K_t:
                    game.tree_open=True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if game.tree_open:
                for i,y in enumerate([265,350,435]):
                    if pygame.Rect(280,y,535,65).collidepoint(pos):
                        game.buy_skill(i)
                if not pygame.Rect(245,145,610,430).collidepoint(pos):
                    game.tree_open=False
            elif MAP_RECT.collidepoint(pos):
                found = next((t for t in reversed(game.towers) if dist(pos,(t.x,t.y)) < 22),None)
                if found:
                    game.selected_tower=found
                else:
                    game.buy_tower(pos)
            elif pos[1] >= 602 and pos[1] <= 672:
                for i in range(len(TOWER_TYPES)):
                    if pygame.Rect(24+i*174,602,164,70).collidepoint(pos):
                        game.selected_kind=i
    if state == "title":
        title.update(dt)
        title.draw()
    elif state == "menu":
        menu.update(dt)
        menu.draw()
    elif state == "difficulty":
        difficulty_screen.draw(menu)
    else:
        game.update(dt)
        game.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
