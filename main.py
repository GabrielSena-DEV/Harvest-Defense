import math
import json
import os
import random
import sys
import shutil
from datetime import datetime
import pygame

pygame.init()
pygame.display.set_caption("HARVEST DEFENSE — Proteja a fazenda. Defenda a colheita.")
WIDTH, HEIGHT = 1100, 720
pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
screen = pygame.Surface((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("trebuchetms,verdana,dejavusans", 17)
SMALL = pygame.font.SysFont("trebuchetms,verdana,dejavusans", 14)
BIG = pygame.font.SysFont("georgia,dejavuserif", 26, bold=True)
HUGE = pygame.font.SysFont("georgia,dejavuserif", 32, bold=True)
ARCADE_FONT = pygame.font.SysFont("couriernew,consolas,monospace", 20, bold=True)
ARCADE_SMALL = pygame.font.SysFont("couriernew,consolas,monospace", 15, bold=True)

BG = (16, 9, 26)
GRASS_A = (31, 36, 44)
GRASS_B = (35, 41, 49)
WHITE = (240, 232, 245)
MINT = (140, 232, 110)     
CYAN = (96, 208, 255)
PURPLE = (192, 130, 255)
ORANGE = (255, 150, 50)   
RED = (255, 84, 84)
MUTED = (160, 140, 178)
PANEL = (28, 17, 44)
BORDER = (96, 58, 128)
DIRT = (104, 72, 48)
DIRT_EDGE = (70, 46, 34)

MAP_RECT = pygame.Rect(24, 80, 1052, 470)
PATH = [(30, 315), (165, 315), (165, 170), (360, 170), (360, 430),
        (560, 430), (560, 245), (760, 245), (760, 360), (1000, 360)]
CORE = (1015, 360)  

MAP_SCENES = {
    "fase_1": {   # Fácil
        "name": "fase_1",
        "source_size": (8600, 4800),
        "path": [
            (4250, 4780), (4250, 4800), (4250, 3750), (4250, 3500),
            (4250, 3250), (4250, 3000), (4250, 2750), (4250, 2500),
            (4000, 2500), (3700, 2500),
            (3400, 2500), (3200, 2500),
            (3100, 2700), (3100, 3000), (3100, 3300), (3000, 3400),
            (2800, 3400),
            (2300, 3400), (1900, 3400), (1780, 3300), (1750, 3050),
            (1750, 2750), (1780, 2500), (1880, 2320), (2070, 2200),
            (2350, 2178), (2600, 2178), (2600, 1900), (2600, 1550),
            (2600, 1200), (2660, 1030), (2800, 930), (3200, 917),
            (4300, 917), (5400, 917), (6660, 917),
        ],
        "core": (6660, 917),
    },
    "fase_2": {   # Médio
        "name": "fase_2",
        "source_size": (8600, 4800),
        "path": [
            (0, 2392), (800, 2392), (1050, 2392), (1150, 2300),
            (1151, 2050), (1151, 1650), (1151, 1350), (1240, 1230),
            (1420, 1192), (1900, 1192), (2350, 1192), (2737, 1192),
            (2790, 1400), (2795, 1900), (2795, 2400), (2790, 2900),
            (2788, 3200), (2880, 3350), (3100, 3389), (3600, 3389),
            (4050, 3389), (4426, 3389), (4434, 3050), (4434, 2650),
            (4434, 2250), (4434, 2000), (4520, 1900), (4800, 1896),
            (5300, 1896), (5800, 1896), (6047, 1896), (6047, 2150),
            (6047, 2500), (6047, 2700), (6140, 2793), (6400, 2794),
            (7000, 2794), (7600, 2794), (8170, 2794),
        ],
        "core": (8170, 2794),
    },
    "fase_3": {   # Difícil
        "name": "fase_3",
        "source_size": (8600, 4800),
        "path": [
            (1900, 4780), (2200, 4700), (2500, 4600), (2750, 4480),
            (2860, 4340), (3000, 4270), (3400, 4190), (3800, 4160),
            (4100, 4120), (4280, 4020), (4280, 3800), (4280, 3500),
            (4280, 3200), (4280, 2900), (4260, 2700), (4150, 2550),
            (4000, 2470), (3700, 2470), (3400, 2470), (3200, 2470),
            (3000, 2530), (2800, 2500), (2700, 2500), (2700, 2700),
            (2700, 3000), (2670, 3250), (2550, 3370), (2350, 3400),
            (2000, 3400), (1600, 3400), (1200, 3400), (1000, 3300),
            (1000, 3000), (1000, 2700), (1000, 2400), (1100, 2300),
            (1350, 2300), (1600, 2200), (1800, 2100), (1800, 1850),
            (1800, 1600), (1800, 1400), (1850, 1200), (2000, 1050),
            (2300, 950), (2700, 917), (3200, 910),
            (4000, 910), (5000, 910), (6000, 910), (7000, 910),
            (7833, 910), (7800, 770), (7740, 540),
        ],
        "core": (7740, 540),
    },
}
_SCENE_BACKGROUND_CACHE = {}
TOWER_TYPES = [
    {"id": "scarecrow", "name": "Espantalho", "cost": 100, "range": 150, "damage": 20, "rate": 0.72, "color": CYAN, "desc": "Dano equilibrado"},
    {"id": "gargoyle", "name": "Gárgula", "cost": 170, "range": 170, "damage": 36, "rate": 1.3, "color": MINT, "desc": "Golpes pesados"},
    {"id": "tombstone", "name": "Lápide", "cost": 140, "range": 130, "damage": 10, "rate": 2.5, "color": (176, 178, 198), "desc": "Invoca bloqueadores", "behavior": "summon"},
    {"id": "corn", "name": "Milho", "cost": 120, "range": 130, "damage": 5, "rate": 0.24, "color": (255, 220, 80), "desc": "Rajada veloz"},
    {"id": "raven", "name": "Corvo", "cost": 190, "range": 220, "damage": 55, "rate": 1.85, "color": (174, 130, 220), "desc": "Precisão e alcance", "bullet_speed": 680},
    {"id": "pumpkin", "name": "Abóbora", "cost": 175, "range": 145, "damage": 22, "rate": 1.2, "color": ORANGE, "desc": "Explosão em área", "area": 48},
]
TOWER_MAX_LEVEL = 5
TOWER_DAMAGE_MULTIPLIERS = (1.0, 1.25, 1.55, 1.9, 3.2)
TOWER_RATE_MULTIPLIERS = (1.0, 0.95, 0.9, 0.85, 0.72)
TOWER_RANGE_MULTIPLIERS = (1.0, 1.04, 1.08, 1.12, 1.2)
TOWER_AREA_MULTIPLIERS = (1.0, 1.08, 1.16, 1.24, 1.5)
TOWER_UPGRADE_COST_MULTIPLIERS = (0.9, 1.35, 2.1, 4.25)

def tower_upgrade_cost(base_cost, level):
    if level >= TOWER_MAX_LEVEL:
        return None
    return round(base_cost * TOWER_UPGRADE_COST_MULTIPLIERS[level - 1])

TOWER_UNLOCKS = [
    {"kind": 1, "cost": 2, "requires": ()},
    {"kind": 2, "cost": 2, "requires": (1,)},
    {"kind": 3, "cost": 2, "requires": (1,)},
    {"kind": 4, "cost": 2, "requires": (2, 3)},
    {"kind": 5, "cost": 2, "requires": (4,)},
]
TOWER_UNLOCK_BY_KIND = {unlock["kind"]: unlock for unlock in TOWER_UNLOCKS}
WAVES = [
    {"count": 9, "hp": 38, "speed": 62, "reward": 24, "name": "Esqueletos e zumbis"},
    {"count": 13, "hp": 54, "speed": 72, "reward": 30, "name": "Horda de mortos-vivos"},
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
    "facil": {"name": "FÁCIL", "scene": "fase_1", "wave_count": 6, "enemy_hp": 0.8, "enemy_speed": 0.9, "core_damage": 0.8, "score_multiplier": 0.8},
    "normal": {"name": "MÉDIO", "scene": "fase_2", "wave_count": 9, "enemy_hp": 1.0, "enemy_speed": 1.0, "core_damage": 1.0, "score_multiplier": 1.0},
    "dificil": {"name": "DIFÍCIL", "scene": "fase_3", "wave_count": 12, "enemy_hp": 1.25, "enemy_speed": 1.12, "core_damage": 1.25, "score_multiplier": 1.25},
}
HEROES = [
    {"id": "coan", "name": "Devair", "ability": "Lentidão Temporária", "description": "Reduz em 60% a velocidade dos inimigos numa área por 5 s.", "cooldown": 22},
    {"id": "capitao_nascimento", "name": "Monica", "ability": "Fúria", "description": "Aumenta em 50% o dano das torres por 8 s.", "cooldown": 24},
    {"id": "devair", "name": "Coan", "ability": "Frenesi", "description": "Aumenta em 50% a cadência das torres por 8 s.", "cooldown": 24},
    {"id": "chico_bento", "name": "Chico Bento", "ability": "Colheita Farta", "description": "Gera abóboras imediatamente: 180 + 25 por onda.", "cooldown": 32},
    {"id": "inacio", "name": "Carlos", "ability": "Pesticida", "description": "Envenena inimigos numa área; causa 6% da vida máx. por segundo durante 5 s.", "cooldown": 26},
    {"id": "jair", "name": "Alessandre", "ability": "Impacto", "description": "Elimina inimigos comuns numa área; chefões recebem dano massivo.", "cooldown": 30},
]
HERO_BY_ID = {hero["id"]: hero for hero in HEROES}
HERO_WAVE_COLORS = {
    "coan": (255, 190, 74),
    "capitao_nascimento": (255, 91, 79),
    "devair": (85, 210, 255),
    "chico_bento": (142, 232, 91),
    "inacio": (190, 111, 255),
    "jair": (255, 245, 167),
}
SKILLS = [
    {"id": "sharpshooter", "name": "Mira de Precisão", "description": "Torres causam 10% mais dano.", "cost": 3},
    {"id": "rapid_fire", "name": "Rajada Rápida", "description": "Torres atacam 8% mais rápido.", "cost": 3},
    {"id": "prepared_defense", "name": "Defesa Preparada", "description": "Comece cada campanha com +100 abóboras.", "cost": 3},
    {"id": "reinforced_barn", "name": "Celeiro Reforçado", "description": "Reduz em 10% o dano sofrido pelo celeiro.", "cost": 4},
    {"id": "harvest_bounty", "name": "Recompensa da Colheita", "description": "Ganhe 15% mais abóboras por inimigo derrotado.", "cost": 4},
    {"id": "lunar_focus", "name": "Foco Lunar", "description": "Pulso lunar recarrega 20% mais rápido e causa +20% de dano.", "cost": 5},
    {"id": "frost_runes", "name": "Runas Gélidas", "description": "Todos os inimigos avançam 15% mais devagar.", "cost": 5},
]
ENEMY_ARCHETYPES = {
    "zombie": {"hp": 1.7, "speed": 0.65, "armor": 0, "regen": 0, "pack": False},
    "skeleton": {"hp": 0.72, "speed": 1.08, "armor": 0, "regen": 0, "pack": False},
    "ghost": {"hp": 0.9, "speed": 1.18, "armor": 0, "regen": 0, "pack": False, "ignores_summons": True},
    "bat": {"hp": 0.3, "speed": 1.85, "armor": 0, "regen": 0, "pack": True},
    "spider": {"hp": 0.42, "speed": 1.65, "armor": 0, "regen": 0, "pack": True},
    "moth": {"hp": 0.32, "speed": 1.75, "armor": 0, "regen": 0, "pack": True},
    "vampire": {"hp": 1.05, "speed": 1.12, "armor": 0, "regen": 5, "pack": False},
    "mummy": {"hp": 1.8, "speed": 1.0, "armor": 0.2, "regen": 0, "pack": False},
    "frankenstein": {"hp": 2.3, "speed": 1.0, "armor": 0.32, "regen": 0, "pack": False},
    "slime": {"hp": 1.0, "speed": 0.9, "armor": 0, "regen": 0, "pack": False},
    "pumpkin": {"hp": 1.15, "speed": 1.0, "armor": 0, "regen": 0, "pack": False},
}
ENEMY_POOLS = [
    ("skeleton", "zombie"),
    ("skeleton", "zombie"),
    ("skeleton", "zombie", "ghost", "slime"),
    ("skeleton", "zombie", "ghost", "bat", "slime"),
    ("zombie", "ghost", "bat", "spider", "moth", "pumpkin"),
    ("zombie", "ghost", "bat", "spider", "moth", "vampire", "pumpkin"),
    ("zombie", "ghost", "bat", "spider", "moth", "vampire", "mummy", "pumpkin"),
    ("zombie", "ghost", "bat", "spider", "moth", "vampire", "mummy", "frankenstein", "pumpkin"),
]
BOSS_SEQUENCE = ("skeleton_bomber", "vampire_lord", "king_ghost", "pop_king")
BOSS_NAMES = {
    "skeleton_bomber": "Esqueleto Cbum",
    "vampire_lord": "Lorde Vampiro",
    "king_ghost": "Rei Fantasma",
    "pop_king": "Rei do Pop",
}
BOSS_ARCHETYPES = {
    "skeleton_bomber": {"base_kind": "skeleton", "hp": 4.0, "speed": 0.78, "armor": 0.12, "reward": 5.0},
    "vampire_lord": {"base_kind": "vampire", "hp": 4.5, "speed": 0.95, "armor": 0.12, "reward": 5.5},
    "king_ghost": {"base_kind": "ghost", "hp": 4.0, "speed": 1.05, "armor": 0, "reward": 5.0},
    "pop_king": {"base_kind": "zombie", "hp": 5.0, "speed": 0.82, "armor": 0.18, "reward": 6.0},
}
PUMPKIN_REWARD_MULTIPLIER = 0.5
BOSS_BRAIN_REWARD = 3

def boss_for_wave(wave):
    if (wave + 1) % 3:
        return None
    chapter = (wave + 1) // 3 - 1
    return BOSS_SEQUENCE[chapter % len(BOSS_SEQUENCE)]

# cor das partículas ao derrotar cada tipo de monstro
KIND_COLORS = {
    "ghost": (235, 235, 255), "slime": PURPLE, "zombie": MINT, "pumpkin": ORANGE,
    "skeleton": (218, 211, 185), "bat": (112, 78, 142), "spider": (68, 55, 48),
    "moth": (221, 199, 136), "vampire": (170, 40, 68), "mummy": (191, 169, 119),
    "frankenstein": (95, 158, 112),
    "skeleton_bomber": (225, 112, 65), "vampire_lord": (174, 34, 64),
    "king_ghost": (120, 224, 245), "pop_king": (184, 188, 112),
}

def fmt_money(n):
    return str(int(max(0, n)))

def draw_text(text, x, y, color=WHITE, font=FONT, surface=screen):
    surface.blit(font.render(str(text), True, color), (x, y))

def draw_centered_text(text, center, color=WHITE, font=FONT, surface=screen):
    rendered = font.render(str(text), True, color)
    surface.blit(rendered, (center[0] - rendered.get_width()//2, center[1] - rendered.get_height()//2))

def wrap_text(text, font, max_width):
    lines = []
    line = ""
    for word in str(text).split():
        candidate = f"{line} {word}".strip()
        if line and font.size(candidate)[0] > max_width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines

def draw_wrapped_text(text, x, y, max_width, color=WHITE, font=FONT, line_spacing=3, max_lines=None):
    lines = wrap_text(text, font, max_width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        last_line = lines[-1]
        while last_line and font.size(last_line + "...")[0] > max_width:
            last_line = last_line.rsplit(" ", 1)[0] if " " in last_line else last_line[:-1]
        lines[-1] = last_line.rstrip() + "..."
    line_height = font.get_linesize() + line_spacing
    for index, line in enumerate(lines):
        draw_text(line, x, y + index * line_height, color, font)
    return y + len(lines) * line_height

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

def map_scene_for_difficulty(difficulty):
    """Mapa da dificuldade (None = cenário clássico desenhado pelo código)."""
    scene_name = DIFFICULTIES[difficulty].get("scene")
    return MAP_SCENES[scene_name] if scene_name else None

def map_play_rect_for_scene(scene):
    if scene is None:
        return MAP_RECT
    source_width, source_height = scene["source_size"]
    map_scale = 0.94
    play_height = round(MAP_RECT.height * map_scale)
    play_width = round(play_height * source_width / source_height)
    return pygame.Rect(
        MAP_RECT.centerx - play_width // 2,
        MAP_RECT.centery - play_height // 2,
        play_width,
        play_height,
    )

def scene_point_to_screen(scene, point):
    source_width, source_height = scene["source_size"]
    play_rect = map_play_rect_for_scene(scene)
    return (
        play_rect.left + round(point[0] * play_rect.width / source_width),
        play_rect.top + round(point[1] * play_rect.height / source_height),
    )

_SCENE_PATH_CACHE = {}

def path_for_scene(scene):
    if scene is None:
        return PATH
    if scene["name"] not in _SCENE_PATH_CACHE:
        _SCENE_PATH_CACHE[scene["name"]] = [scene_point_to_screen(scene, p) for p in scene["path"]]
    return _SCENE_PATH_CACHE[scene["name"]]

def core_for_scene(scene):
    if scene is None:
        return CORE
    return scene_point_to_screen(scene, scene["core"])

def path_for_difficulty(difficulty):
    return path_for_scene(map_scene_for_difficulty(difficulty))

def on_path(pos, path=PATH, radius=28):
    return any(point_segment_distance(pos, path[i], path[i+1]) < radius for i in range(len(path)-1))

class Monster:
    def __init__(self, wave, difficulty, kind=None):
        spec = WAVES[wave]
        difficulty_spec = DIFFICULTIES[difficulty]
        self.wave_index = wave
        self.difficulty = difficulty
        self.kind = kind or random.choice(ENEMY_POOLS[min(wave, len(ENEMY_POOLS) - 1)])
        boss_spec = BOSS_ARCHETYPES.get(self.kind)
        self.is_boss = boss_spec is not None
        if boss_spec is None:
            archetype = ENEMY_ARCHETYPES[self.kind]
            hp_multiplier = archetype["hp"]
            speed_multiplier = archetype["speed"]
            armor = archetype["armor"]
            reward_multiplier = archetype["hp"] ** 0.35
        else:
            archetype = ENEMY_ARCHETYPES[boss_spec["base_kind"]]
            hp_multiplier = boss_spec["hp"]
            speed_multiplier = boss_spec["speed"]
            armor = boss_spec["armor"]
            reward_multiplier = boss_spec["reward"]
        self.path = path_for_difficulty(difficulty)
        self.x, self.y = self.path[0]
        self.segment = 0
        self.progress = 0.0
        self.max_hp = spec["hp"] * hp_multiplier * difficulty_spec["enemy_hp"] * random.uniform(.96, 1.04)
        self.hp = self.max_hp
        self.speed = spec["speed"] * speed_multiplier * difficulty_spec["enemy_speed"] * random.uniform(.96, 1.04)
        self.armor = armor
        self.regen = archetype["regen"]
        self.ignores_summons = archetype.get("ignores_summons", False)
        if self.kind == "king_ghost":
            self.ignores_summons = False
        self.reward = max(1, round(spec["reward"] * reward_multiplier * PUMPKIN_REWARD_MULTIPLIER))
        self.radius = random.choice([10, 11, 12]) + wave // 3 + (8 if self.is_boss else 0)
        self.slime_color = random.choice([(150, 78, 210), (255, 150, 40)])
        self.phase = random.uniform(0, 6.28)
        self.dead = False
        self.reached = False
        self.hit_flash = 0
        self.intangible = False
        self.intangible_timer = 0
        self.phase_charge = 0
        self.phase_used = False
        self.heal_cooldown = 0
        self.vigor_multiplier = 1
        self.hero_slow_timer = 0
        self.poison_timer = 0
        self.poison_tick_timer = 0
        self.summoned_at_half_health = False
        self.summons_on_death_done = False

    def take_damage(self, amount):
        if self.intangible:
            return
        self.hp -= max(1, amount * (1 - self.armor))
        if self.hp <= 0:
            self.dead = True

    def create_minions(self, count, kind):
        minions = []
        for _ in range(count):
            minion = Monster(self.wave_index, self.difficulty, kind)
            minion.x, minion.y = self.x, self.y
            minion.segment = self.segment
            minions.append(minion)
        return minions

    def update(self, dt, allied_minions=()):
        spawned = []
        self.heal_cooldown = max(0, self.heal_cooldown - dt)
        self.hero_slow_timer = max(0, self.hero_slow_timer - dt)
        if self.intangible:
            self.intangible_timer -= dt
            if self.intangible_timer <= 0:
                self.intangible = False

        if self.kind == "vampire_lord" and self.heal_cooldown <= 0:
            if any(dist((self.x, self.y), (unit.x, unit.y)) < 48 for unit in allied_minions):
                self.hp = min(self.max_hp, self.hp + self.max_hp * 0.05)
                self.heal_cooldown = 2.5

        if self.kind == "king_ghost" and not self.phase_used and self.hp <= self.max_hp * 0.3:
            slow_applied = getattr(self, "slow_factor", 1) < 1 or self.hero_slow_timer > 0
            self.phase_charge += dt * (0.25 if slow_applied else 1)
            if self.phase_charge >= 2.5:
                self.intangible = True
                self.intangible_timer = 3
                self.phase_used = True

        if self.kind == "pop_king" and not self.summoned_at_half_health and self.hp <= self.max_hp * 0.5:
            self.summoned_at_half_health = True
            spawned.extend(self.create_minions(4, "zombie"))

        if self.kind == "pop_king":
            self.vigor_multiplier = 1.25
        else:
            self.vigor_multiplier = 1

        self.hp = min(self.max_hp, self.hp + self.regen * dt)
        if self.segment >= len(self.path)-1:
            self.reached = True
            return spawned
        target = self.path[self.segment+1]
        dx, dy = target[0]-self.x, target[1]-self.y
        length = math.hypot(dx, dy)
        slow_factor = min(getattr(self, "slow_factor", 1), .4 if self.hero_slow_timer > 0 else 1)
        step = self.speed * self.vigor_multiplier * dt * slow_factor
        if length <= step:
            self.x, self.y = target
            self.segment += 1
            if self.segment >= len(self.path)-1:
                self.reached = True
        elif length:
            self.x += dx/length*step
            self.y += dy/length*step
        self.hit_flash = max(0, self.hit_flash-dt)
        return spawned

    def on_death(self):
        if self.kind == "skeleton_bomber" and not self.summons_on_death_done:
            self.summons_on_death_done = True
            return self.create_minions(4, "skeleton")
        return []

    def draw(self, surface):
        r = self.radius
        bob = int(math.sin(pygame.time.get_ticks()/140 + self.phase) * 2)
        x, y = int(self.x), int(self.y) + bob
        dark = (28, 14, 36)
        if self.is_boss:
            if self.kind == "pop_king":
                pygame.draw.circle(surface, (214, 190, 90), (x, y), 125, 1)
            boss_sprite = BOSS_SPRITES.get(self.kind)
            if boss_sprite is not None:
                sprite_rect = boss_sprite.get_rect(midbottom=(x, y + r))
                surface.blit(boss_sprite, sprite_rect)
                if self.kind == "king_ghost" and self.intangible:
                    pygame.draw.ellipse(surface, CYAN, sprite_rect.inflate(10, 10), 2)
            else:
                boss_color = {
                    "skeleton_bomber": (225, 112, 65),
                    "vampire_lord": (174, 34, 64),
                    "king_ghost": (120, 224, 245),
                    "pop_king": (184, 188, 112),
                }[self.kind]
                pygame.draw.circle(surface, (32, 18, 38), (x, y), r + 4)
                pygame.draw.circle(surface, boss_color, (x, y), r)
                pygame.draw.circle(surface, ORANGE if self.kind == "skeleton_bomber" else WHITE, (x, y), r + 3, 2)
                if self.kind == "skeleton_bomber":
                    pygame.draw.circle(surface, (245, 230, 194), (x, y-2), r//2)
                    pygame.draw.circle(surface, dark, (x-r//5, y-3), max(2, r//8))
                    pygame.draw.circle(surface, dark, (x+r//5, y-3), max(2, r//8))
                    pygame.draw.circle(surface, RED, (x, y+r//4), max(2, r//6))
                elif self.kind == "vampire_lord":
                    pygame.draw.polygon(surface, (62, 16, 39), [(x-r, y), (x-r//2, y+r), (x, y+r//2), (x+r//2, y+r), (x+r, y)])
                    pygame.draw.circle(surface, RED, (x-r//4, y-2), max(2, r//8))
                    pygame.draw.circle(surface, RED, (x+r//4, y-2), max(2, r//8))
                elif self.kind == "king_ghost":
                    pygame.draw.polygon(surface, (220, 242, 255), [(x-r//2, y-r//2), (x-r//3, y-r), (x, y-r//2), (x+r//3, y-r), (x+r//2, y-r//2)])
                    pygame.draw.circle(surface, dark, (x-r//4, y), max(2, r//8))
                    pygame.draw.circle(surface, dark, (x+r//4, y), max(2, r//8))
                    if self.intangible:
                        pygame.draw.circle(surface, CYAN, (x, y), r + 8, 2)
                else:
                    pygame.draw.rect(surface, (45, 48, 44), (x-r//2, y-r//2, r, r+5), border_radius=4)
                    pygame.draw.circle(surface, (30, 24, 22), (x-r//4, y-r//4), max(2, r//9))
                    pygame.draw.circle(surface, (30, 24, 22), (x+r//4, y-r//4), max(2, r//9))
                    pygame.draw.polygon(surface, (38, 24, 30), [(x-r, y), (x-r//2, y+r), (x, y+r//2), (x+r//2, y+r), (x+r, y)])
                    pygame.draw.line(surface, WHITE, (x-r//2, y-r), (x+r//2, y-r), 2)
        elif self.kind == "ghost":
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
        elif self.kind == "skeleton":
            pygame.draw.line(surface, (224, 216, 190), (x, y-2), (x, y+r), 3)
            pygame.draw.circle(surface, (235, 229, 207), (x, y-r//2), r//2+2)
            pygame.draw.circle(surface, dark, (x-r//5, y-r//2), 2)
            pygame.draw.circle(surface, dark, (x+r//5, y-r//2), 2)
            for offset in (-1, 1):
                pygame.draw.line(surface, (210, 201, 177), (x, y+2), (x+offset*r, y+r//2), 2)
                pygame.draw.line(surface, (210, 201, 177), (x, y+r//2), (x+offset*r, y+r), 2)
            pygame.draw.line(surface, (210, 201, 177), (x-r//2, y+2), (x+r//2, y+2), 2)
        elif self.kind == "bat":
            flap = int(math.sin(pygame.time.get_ticks()/65 + self.phase) * 4)
            pygame.draw.polygon(surface, (91, 62, 125), [(x, y), (x-r-4, y-r+flap), (x-r//2, y+2), (x-r-2, y+r//2)])
            pygame.draw.polygon(surface, (91, 62, 125), [(x, y), (x+r+4, y-r+flap), (x+r//2, y+2), (x+r+2, y+r//2)])
            pygame.draw.circle(surface, (55, 39, 72), (x, y), max(3, r//2))
            pygame.draw.circle(surface, RED, (x-2, y), 1)
            pygame.draw.circle(surface, RED, (x+2, y), 1)
        elif self.kind == "spider":
            for offset in (-1, 1):
                for leg_y in (-r//2, 0, r//2):
                    pygame.draw.line(surface, (57, 45, 42), (x, y+leg_y//2), (x+offset*r, y+leg_y), 2)
            pygame.draw.circle(surface, (56, 44, 40), (x, y), r//2+2)
            pygame.draw.circle(surface, RED, (x-2, y-1), 1)
            pygame.draw.circle(surface, RED, (x+2, y-1), 1)
        elif self.kind == "moth":
            flutter = int(math.sin(pygame.time.get_ticks()/70 + self.phase) * 3)
            pygame.draw.ellipse(surface, (215, 192, 137), (x-r-3, y-r//2-flutter, r+4, r+3))
            pygame.draw.ellipse(surface, (238, 220, 170), (x+1, y-r//2+flutter, r+3, r+3))
            pygame.draw.ellipse(surface, (92, 67, 46), (x-2, y-r//2, 4, r+5))
            pygame.draw.line(surface, dark, (x-1, y-r//2), (x-4, y-r), 1)
            pygame.draw.line(surface, dark, (x+1, y-r//2), (x+4, y-r), 1)
        elif self.kind == "vampire":
            pygame.draw.polygon(surface, (84, 25, 49), [(x-r-2, y-r//2), (x-r, y+r), (x, y+r//2), (x+r, y+r), (x+r+2, y-r//2)])
            pygame.draw.circle(surface, (188, 188, 202), (x, y-r//3), r//2+2)
            pygame.draw.circle(surface, RED, (x-r//5, y-r//3), 2)
            pygame.draw.circle(surface, RED, (x+r//5, y-r//3), 2)
            pygame.draw.line(surface, WHITE, (x-2, y), (x-1, y+3), 1)
            pygame.draw.line(surface, WHITE, (x+2, y), (x+1, y+3), 1)
        elif self.kind == "mummy":
            pygame.draw.ellipse(surface, (181, 161, 113), (x-r, y-r, r*2, r*2))
            for band_y in (-r//2, 0, r//2):
                pygame.draw.line(surface, (225, 210, 160), (x-r+2, y+band_y), (x+r-2, y+band_y+2), 3)
            pygame.draw.circle(surface, (48, 32, 27), (x-r//4, y-2), 2)
            pygame.draw.circle(surface, (48, 32, 27), (x+r//4, y-2), 2)
            pygame.draw.arc(surface, (90, 63, 43), (x-r//2, y, r, r//2), 0, math.pi, 2)
        elif self.kind == "frankenstein":
            pygame.draw.rect(surface, (50, 71, 59), (x-r, y-r//2, r*2, r+2), border_radius=3)
            pygame.draw.rect(surface, (105, 164, 113), (x-r-2, y-r//2-4, r*2+4, r), border_radius=5)
            pygame.draw.rect(surface, (48, 50, 49), (x-r-4, y-r//4, 4, 5))
            pygame.draw.rect(surface, (48, 50, 49), (x+r, y-r//4, 4, 5))
            pygame.draw.circle(surface, dark, (x-r//3, y-r//4), 2)
            pygame.draw.circle(surface, dark, (x+r//3, y-r//4), 2)
            pygame.draw.line(surface, dark, (x-r//3, y+r//4), (x+r//3, y+r//4), 2)
        else:
            draw_pumpkin(surface, x, y, r, face=True)
            pygame.draw.rect(surface, (118, 168, 96), (x-r-3, y+2, 4, r//2))
            pygame.draw.rect(surface, (118, 168, 96), (x+r-1, y+2, 4, r//2))
        if self.hit_flash > 0:
            pygame.draw.circle(surface, WHITE, (x, y), r+2, 3)
        if self.poison_timer > 0:
            pygame.draw.circle(surface, (122, 236, 88), (x, y), r+5, 2)
        # barra de vida
        y0 = int(self.y)
        boss_sprite = BOSS_SPRITES.get(self.kind) if self.is_boss else None
        bar_width = 68 if boss_sprite else 46 if self.is_boss else 30
        bar_y = y0 - boss_sprite.get_height() - 8 if boss_sprite else y0-r-11
        pygame.draw.rect(surface, (38, 24, 52), (x-bar_width//2, bar_y, bar_width, 5 if self.is_boss else 4), border_radius=2)
        health_color = ORANGE if self.is_boss else MINT
        pygame.draw.rect(surface, health_color, (x-bar_width//2, bar_y, int(bar_width*max(0, self.hp/self.max_hp)), 5 if self.is_boss else 4), border_radius=2)
        if self.is_boss:
            name = SMALL.render(BOSS_NAMES[self.kind], True, ORANGE)
            name_y = bar_y - name.get_height() - 3 if boss_sprite else y0-r-30
            surface.blit(name, (x-name.get_width()//2, name_y))
            if self.kind == "king_ghost" and self.intangible:
                if not boss_sprite:
                    phase_label = SMALL.render("INTANGÍVEL", True, CYAN)
                    surface.blit(phase_label, (x-phase_label.get_width()//2, y0-r-45))

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
        candidates = [e for e in enemies if not e.dead and not e.reached and not e.ignores_summons and not e.intangible]
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
            self.target.take_damage(self.damage)
            self.target.hit_flash = .1
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
        self.rate_multiplier = rate_multiplier
        self.rate = spec["rate"] * rate_multiplier
        self.cooldown = random.random() * .2
        self.color = spec["color"]
        self.cost = spec["cost"]
        self.target = None
        self.angle = 0

    def upgrade(self):
        if self.level >= TOWER_MAX_LEVEL:
            return False
        self.level += 1
        return True

    def update(self, dt, enemies, bullets, minions):
        self.cooldown = max(0, self.cooldown-dt)
        candidates = [
            e for e in enemies
            if not e.dead and not e.reached and not e.intangible
            and dist((self.x,self.y),(e.x,e.y)) <= self.range
        ]
        if candidates:
            self.target = max(candidates, key=lambda e: e.segment + e.progress)
            self.angle = math.atan2(self.target.y-self.y, self.target.x-self.x)
            if self.cooldown <= 0:
                behavior = TOWER_TYPES[self.kind].get("behavior")
                if behavior == "summon":
                    minions.append(AlliedMinion((self.x, self.y), self.damage))
                else:
                    area_radius = TOWER_TYPES[self.kind].get("area", 0)
                    area_radius *= TOWER_AREA_MULTIPLIERS[self.level - 1]
                    bullets.append(Bullet((self.x,self.y), self.target, self.damage, self.color,
                                          area_radius,
                                          TOWER_TYPES[self.kind].get("bullet_speed", 420)))
                self.cooldown = self.rate
        else:
            self.target = None

    def draw(self, surface, selected=False):
        x, y = int(self.x), int(self.y)
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
        if self.target.dead or self.target.reached or self.target.intangible:
            self.dead = True
            return
        dx, dy = self.target.x-self.x, self.target.y-self.y
        length = math.hypot(dx,dy)
        if length < self.speed*dt + 5:
            for enemy in enemies:
                if (not enemy.dead and not enemy.reached and not enemy.intangible
                        and (enemy is self.target or
                             (self.area_radius and dist((self.target.x, self.target.y), (enemy.x, enemy.y)) <= self.area_radius))):
                    enemy.take_damage(self.damage)
                    enemy.hit_flash = .12
            self.dead = True
        elif length:
            self.x += dx/length*self.speed*dt
            self.y += dy/length*self.speed*dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x),int(self.y)), 5)
        pygame.draw.circle(surface, WHITE, (int(self.x),int(self.y)), 2)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BOSS_SPRITE_FILES = {
    "skeleton_bomber": "1.png",
    "vampire_lord": "2.png",
    "king_ghost": "3.png",
    "pop_king": "4.png",
}
BOSS_SPRITE_HEIGHT = 96

def load_boss_sprites():
    sprites = {}
    for boss_kind, filename in BOSS_SPRITE_FILES.items():
        path = os.path.join(BASE_DIR, "assets", "enemies", filename)
        try:
            source = pygame.image.load(path).convert_alpha()
            bounds = source.get_bounding_rect(min_alpha=1)
            if bounds.width == 0 or bounds.height == 0:
                raise pygame.error("A imagem não contém pixels visíveis.")
            cropped = source.subsurface(bounds).copy()
            width = round(cropped.get_width() * BOSS_SPRITE_HEIGHT / cropped.get_height())
            sprites[boss_kind] = pygame.transform.scale(cropped, (width, BOSS_SPRITE_HEIGHT))
        except (pygame.error, OSError) as error:
            print(f"Não foi possível carregar o sprite do chefe '{path}': {error}", file=sys.stderr)
    return sprites

BOSS_SPRITES = load_boss_sprites()

HERO_SPRITE_FILES = {
    "coan": "Devair.png",
    "capitao_nascimento": "Mônica.png",
    "devair": "Coan.png",
    "chico_bento": "Chico.png",
    "inacio": "Carlos.png",
    "jair": "Alessandre.png",
}
HERO_SPRITE_HEIGHT = 88

def load_hero_sprites():
    sprites = {}
    for hero_id, filename in HERO_SPRITE_FILES.items():
        path = os.path.join(BASE_DIR, "assets", "heros", filename)
        try:
            source = pygame.image.load(path).convert_alpha()
            bounds = source.get_bounding_rect(min_alpha=1)
            if bounds.width == 0 or bounds.height == 0:
                raise pygame.error("A imagem não contém pixels visíveis.")
            cropped = source.subsurface(bounds).copy()
            width = round(cropped.get_width() * HERO_SPRITE_HEIGHT / cropped.get_height())
            sprites[hero_id] = pygame.transform.smoothscale(
                cropped,
                (width, HERO_SPRITE_HEIGHT),
            )
        except (pygame.error, OSError) as error:
            print(f"Não foi possível carregar o sprite do herói '{path}': {error}", file=sys.stderr)
    return sprites

HERO_SPRITES = load_hero_sprites()
HERO_MAP_SPRITES = {
    hero_id: pygame.transform.smoothscale(
        sprite,
        (
            round(sprite.get_width() * 76 / sprite.get_height()),
            76,
        ),
    )
    for hero_id, sprite in HERO_SPRITES.items()
}

def local_data_file(filename, legacy_filenames=()):
    data_dir = os.path.join(BASE_DIR, "docs")
    destination = os.path.join(data_dir, filename)
    if os.path.exists(destination):
        return destination

    legacy_dirs = (
        os.path.join(BASE_DIR, "placar"),
        os.path.join(os.path.expanduser("~"), ".harvest-defense"),
    )
    for legacy_filename in legacy_filenames:
        for legacy_dir in legacy_dirs:
            source = os.path.join(legacy_dir, legacy_filename)
            if not os.path.isfile(source):
                continue
            try:
                os.makedirs(data_dir, exist_ok=True)
                temporary_path = destination + ".migrating"
                shutil.copy2(source, temporary_path)
                os.replace(temporary_path, destination)
            except OSError as error:
                print(
                    f"Não foi possível mover '{source}' para '{destination}': {error}",
                    file=sys.stderr,
                )
                return source
            try:
                os.remove(source)
            except OSError as error:
                print(
                    f"Os dados foram copiados, mas não foi possível remover '{source}': {error}",
                    file=sys.stderr,
                )
            return destination
    return destination

def format_duration(seconds):
    total = max(0, int(seconds))
    return f"{total // 60:02}:{total % 60:02}"

class Leaderboard:
    """Ranking local, preservado entre execuções do jogo."""
    LIMIT = 10

    def __init__(self):
        self.path = local_data_file("scores.json", ("scores.json", "leaderboard.json"))
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

    def all_records(self):
        records = [
            (entry, difficulty)
            for difficulty in DIFFICULTIES
            for entry in self.records_for(difficulty)
        ]
        records.sort(key=lambda record: record[0]["score"], reverse=True)
        return records[:self.LIMIT]

    def add_result(self, result):
        difficulty = result["difficulty"]
        updated_rankings = {
            key: list(entries) for key, entries in self.rankings.items()
        }
        updated_rankings[difficulty].append(result)
        updated_rankings[difficulty].sort(key=lambda entry: entry["score"], reverse=True)
        updated_rankings[difficulty] = updated_rankings[difficulty][:self.LIMIT]
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            temporary_path = self.path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as ranking_file:
                json.dump({"rankings": updated_rankings}, ranking_file, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self.path)
        except OSError as error:
            print(f"Não foi possível salvar o ranking: {error}", file=sys.stderr)
            return str(error)
        self.rankings = updated_rankings
        return None

class PlayerProfile:
    """Moedas, habilidades e desbloqueios permanentes do jogador."""
    MAX_EQUIPPED_SKILLS = 3

    def __init__(self):
        self.path = local_data_file("profile.json", ("profile.json",))
        self.users = {}
        self.active_user = None
        self.last_user = None
        self.brains = 0
        self.unlocked_skills = set()
        self.equipped_skills = []
        self.unlocked_towers = set()
        self.auto_waves = False
        self.last_error = None
        self.load()

    @staticmethod
    def valid_initials(initials):
        return (
            isinstance(initials, str)
            and len(initials) == 3
            and all("A" <= char <= "Z" for char in initials)
        )

    @staticmethod
    def default_user_data():
        return {
            "brains": 0,
            "unlocked_skills": [],
            "equipped_skills": [],
            "unlocked_towers": [],
            "auto_waves": False,
        }

    def apply_user_data(self, data):
        defaults = self.default_user_data()
        valid_skill_ids = {skill["id"] for skill in SKILLS}
        valid_tower_ids = {TOWER_TYPES[unlock["kind"]]["id"] for unlock in TOWER_UNLOCKS}
        brains = data.get("brains", defaults["brains"])
        unlocked = data.get("unlocked_skills", defaults["unlocked_skills"])
        equipped = data.get("equipped_skills", defaults["equipped_skills"])
        unlocked_towers = data.get("unlocked_towers", defaults["unlocked_towers"])
        auto_waves = data.get("auto_waves", defaults["auto_waves"])
        if isinstance(brains, int) and not isinstance(brains, bool) and brains >= 0:
            self.brains = brains
        else:
            self.brains = 0
            self.last_error = "Saldo de cérebros inválido; iniciado em zero."
        self.unlocked_skills = (
            {
                skill_id for skill_id in unlocked
                if isinstance(skill_id, str) and skill_id in valid_skill_ids
            }
            if isinstance(unlocked, list)
            else set()
        )
        self.unlocked_towers = (
            {
                tower_id for tower_id in unlocked_towers
                if isinstance(tower_id, str) and tower_id in valid_tower_ids
            }
            if isinstance(unlocked_towers, list)
            else set()
        )
        self.equipped_skills = []
        if isinstance(equipped, list):
            for skill_id in equipped:
                if (isinstance(skill_id, str) and skill_id in self.unlocked_skills
                        and skill_id not in self.equipped_skills):
                    self.equipped_skills.append(skill_id)
                    if len(self.equipped_skills) == self.MAX_EQUIPPED_SKILLS:
                        break
        self.auto_waves = auto_waves if isinstance(auto_waves, bool) else False

    def serialize_active_user(self):
        return {
            "brains": self.brains,
            "unlocked_skills": sorted(self.unlocked_skills),
            "equipped_skills": list(self.equipped_skills),
            "unlocked_towers": sorted(self.unlocked_towers),
            "auto_waves": self.auto_waves,
        }

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as profile_file:
                data = json.load(profile_file)
        except FileNotFoundError:
            return
        except (OSError, json.JSONDecodeError) as error:
            self.last_error = f"Não foi possível carregar o perfil: {error}"
            print(self.last_error, file=sys.stderr)
            return

        if not isinstance(data, dict):
            self.last_error = "Arquivo de perfis inválido; novos jogadores começam sem progresso."
            print(self.last_error, file=sys.stderr)
            return

        users = data.get("users", {})
        if not isinstance(users, dict):
            self.last_error = "Lista de perfis inválida; jogadores novos começam sem progresso."
            print(self.last_error, file=sys.stderr)
            return
        for initials, user_data in users.items():
            if self.valid_initials(initials) and isinstance(user_data, dict):
                self.users[initials] = user_data
        last_user = data.get("active_user")
        if self.valid_initials(last_user):
            self.last_user = last_user

    def save(self):
        if self.active_user is None:
            self.last_error = "Identifique o jogador antes de salvar o perfil."
            return self.last_error
        self.users[self.active_user] = self.serialize_active_user()
        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            temporary_path = self.path + ".tmp"
            with open(temporary_path, "w", encoding="utf-8") as profile_file:
                json.dump({
                    "version": 2,
                    "active_user": self.active_user,
                    "users": self.users,
                }, profile_file, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self.path)
        except OSError as error:
            self.last_error = f"Não foi possível salvar o perfil: {error}"
            print(self.last_error, file=sys.stderr)
            return self.last_error
        self.last_error = None
        return None

    def select_user(self, initials):
        initials = initials.upper() if isinstance(initials, str) else ""
        if not self.valid_initials(initials):
            return "Digite exatamente três letras de A a Z."
        previous_user = self.active_user
        previous_last_user = self.last_user
        previous_users = {key: dict(value) for key, value in self.users.items()}
        previous_brains = self.brains
        previous_skills = set(self.unlocked_skills)
        previous_equipped = list(self.equipped_skills)
        previous_towers = set(self.unlocked_towers)
        previous_auto_waves = self.auto_waves
        if self.active_user is not None:
            self.users[self.active_user] = self.serialize_active_user()
        self.active_user = initials
        self.last_user = initials
        self.apply_user_data(self.users.get(initials, self.default_user_data()))
        error = self.save()
        if error:
            self.active_user = previous_user
            self.last_user = previous_last_user
            self.users = previous_users
            self.brains = previous_brains
            self.unlocked_skills = previous_skills
            self.equipped_skills = previous_equipped
            self.unlocked_towers = previous_towers
            self.auto_waves = previous_auto_waves
        return error

    def confirm_user(self, initials):
        initials = initials.upper() if isinstance(initials, str) else ""
        if not self.valid_initials(initials):
            return "Digite exatamente três letras de A a Z."
        if initials != self.active_user:
            return f"Esta partida pertence ao perfil {self.active_user}. Digite essas iniciais para salvar."
        return self.save()

    def award_brains(self, amount):
        self.brains += amount
        error = self.save()
        if error:
            self.brains -= amount
            return 0, error
        return amount, None

    def tower_is_unlocked(self, kind):
        if kind == 0:
            return True
        return TOWER_TYPES[kind]["id"] in self.unlocked_towers

    def unlock_tower(self, kind):
        unlock = TOWER_UNLOCK_BY_KIND.get(kind)
        if unlock is None:
            return "Essa torre não pode ser desbloqueada."
        tower = TOWER_TYPES[kind]
        tower_id = tower["id"]
        if self.tower_is_unlocked(kind):
            return f"{tower['name']} já foi desbloqueada."
        missing = [
            TOWER_TYPES[required]["name"]
            for required in unlock["requires"]
            if not self.tower_is_unlocked(required)
        ]
        if missing:
            return "Desbloqueie primeiro: " + " e ".join(missing) + "."
        if self.brains < unlock["cost"]:
            return f"Cérebros insuficientes: são necessários {unlock['cost']}."

        self.brains -= unlock["cost"]
        self.unlocked_towers.add(tower_id)
        error = self.save()
        if error:
            self.brains += unlock["cost"]
            self.unlocked_towers.remove(tower_id)
            return error
        return f"Torre desbloqueada: {tower['name']}."

    def purchase_skill(self, skill):
        skill_id = skill["id"]
        if skill_id in self.unlocked_skills:
            return "Essa habilidade já foi desbloqueada."
        skill_index = next(
            (index for index, item in enumerate(SKILLS) if item["id"] == skill_id),
            None,
        )
        if skill_index is None:
            raise ValueError(f"Habilidade desconhecida: {skill_id}")
        if skill_index > 0:
            prerequisite = SKILLS[skill_index - 1]
            if prerequisite["id"] not in self.unlocked_skills:
                return f"Desbloqueie primeiro: {prerequisite['name']}."
        if self.brains < skill["cost"]:
            return "Cérebros insuficientes para essa habilidade."
        self.brains -= skill["cost"]
        self.unlocked_skills.add(skill_id)
        equipped = False
        if len(self.equipped_skills) < self.MAX_EQUIPPED_SKILLS:
            self.equipped_skills.append(skill_id)
            equipped = True
        error = self.save()
        if error:
            self.brains += skill["cost"]
            self.unlocked_skills.remove(skill_id)
            if equipped:
                self.equipped_skills.remove(skill_id)
            return error
        status = "desbloqueada e equipada" if equipped else "desbloqueada; equipe pelo menu"
        return f"Habilidade {status}: {skill['name']}."

    def toggle_skill(self, skill):
        skill_id = skill["id"]
        if skill_id not in self.unlocked_skills:
            return self.purchase_skill(skill)
        if skill_id in self.equipped_skills:
            self.equipped_skills.remove(skill_id)
            message = f"Habilidade removida: {skill['name']}."
        else:
            if len(self.equipped_skills) >= self.MAX_EQUIPPED_SKILLS:
                return f"Limite de {self.MAX_EQUIPPED_SKILLS} habilidades equipadas."
            self.equipped_skills.append(skill_id)
            message = f"Habilidade equipada: {skill['name']}."
        error = self.save()
        if error:
            if skill_id in self.equipped_skills:
                self.equipped_skills.remove(skill_id)
            else:
                self.equipped_skills.append(skill_id)
            return error
        return message

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
        pygame.draw.rect(screen, (14, 8, 24), (0, 500, WIDTH, 110))
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
        equipped_names = [skill["name"] for skill in SKILLS if skill["id"] in profile.equipped_skills]
        loadout = ", ".join(equipped_names) if equipped_names else "nenhuma"
        draw_centered_text(
            f"Jogador {profile.active_user}  |  Cérebros: {profile.brains}  |  Equipamento: {loadout}",
            (WIDTH // 2, 566),
            PURPLE,
            SMALL,
        )

class PlayerIdentificationScreen:
    def __init__(self):
        self.initials = [" ", " ", " "]
        self.selected_index = 0
        self.message = "Digite suas iniciais para carregar ou criar seu perfil."
        self.can_back = profile.active_user is not None
        self.title_rect = pygame.Rect(250, 500, 270, 58)
        self.confirm_rect = pygame.Rect(580, 500, 270, 58)
        self.letter_rects = [
            pygame.Rect(WIDTH // 2 - 130 + index * 90, 320, 70, 88)
            for index in range(3)
        ]

    def reset(self):
        self.initials = [" ", " ", " "]
        self.selected_index = 0
        self.message = "Digite suas iniciais para carregar ou criar seu perfil."
        self.can_back = profile.active_user is not None

    def submit(self):
        initials = "".join(self.initials)
        error = profile.select_user(initials)
        if error:
            self.message = error
            return None
        return "selected"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and self.can_back:
                return "back"
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % 3
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % 3
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                letter = self.initials[self.selected_index]
                if "A" <= letter <= "Z":
                    delta = 1 if event.key == pygame.K_UP else -1
                    value = (ord(letter) - ord("A") + delta) % 26
                else:
                    value = 0 if event.key == pygame.K_UP else 25
                self.initials[self.selected_index] = chr(value + ord("A"))
            elif event.key == pygame.K_BACKSPACE:
                self.initials[self.selected_index] = " "
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                return self.submit()
            elif len(event.unicode) == 1 and event.unicode.isascii() and event.unicode.isalpha():
                self.initials[self.selected_index] = event.unicode.upper()
                if self.selected_index < 2:
                    self.selected_index += 1
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.title_rect.collidepoint(event.pos):
                return "title"
            if self.confirm_rect.collidepoint(event.pos):
                return self.submit()
            for index, rect in enumerate(self.letter_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = index
                    break
        return None

    def draw(self):
        screen.fill((5, 7, 18))
        panel = pygame.Rect(170, 120, 760, 500)
        pygame.draw.rect(screen, (12, 17, 34), panel, border_radius=18)
        pygame.draw.rect(screen, CYAN, panel, 3, border_radius=18)
        draw_centered_text("IDENTIFIQUE SEU JOGADOR", (panel.centerx, 170), ORANGE, BIG)
        draw_centered_text(
            "Seu perfil guarda seus cérebros e desbloqueios neste computador.",
            (panel.centerx, 220),
            WHITE,
            SMALL,
        )
        draw_centered_text(
            "Perfis novos começam com zero cérebros.",
            (panel.centerx, 250),
            PURPLE,
            SMALL,
        )
        for index, rect in enumerate(self.letter_rects):
            selected = index == self.selected_index
            pygame.draw.rect(
                screen,
                (23, 44, 52) if selected else (24, 20, 38),
                rect,
                border_radius=8,
            )
            pygame.draw.rect(screen, MINT if selected else BORDER, rect, 2, border_radius=8)
            letter = self.initials[index] if self.initials[index] != " " else "_"
            draw_centered_text(letter, rect.center, ORANGE if selected else WHITE, HUGE)
        draw_centered_text(
            "Digite letras ou use as setas para escolher a posicao e mudar a letra.",
            (panel.centerx, 450),
            MUTED,
            SMALL,
        )
        pygame.draw.rect(screen, (48, 30, 32), self.title_rect, border_radius=9)
        pygame.draw.rect(screen, ORANGE, self.title_rect, 2, border_radius=9)
        draw_centered_text("VOLTAR À TELA INICIAL", self.title_rect.center, ORANGE, SMALL)
        pygame.draw.rect(screen, (36, 58, 42), self.confirm_rect, border_radius=9)
        pygame.draw.rect(screen, MINT, self.confirm_rect, 2, border_radius=9)
        draw_centered_text("CONTINUAR", self.confirm_rect.center, MINT, FONT)
        draw_centered_text(self.message, (panel.centerx, 585), WHITE, SMALL)
        if self.can_back:
            draw_centered_text(
                f"Perfil ativo: {profile.active_user}  |  ESC: voltar",
                (panel.centerx, 645),
                MUTED,
                SMALL,
            )

class HeroSelectionScreen:
    CARD_RECTS = [
        pygame.Rect(46 + (index % 3) * 338, 255 + (index // 3) * 145, 320, 130)
        for index in range(len(HEROES))
    ]

    def __init__(self):
        self.selected = 0
        self.portrait_sprites = {
            hero_id: pygame.transform.smoothscale(
                sprite,
                (
                    round(sprite.get_width() * 82 / sprite.get_height()),
                    82,
                ),
            )
            for hero_id, sprite in HERO_SPRITES.items()
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected = (self.selected - 1) % len(HEROES)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected = (self.selected + 1) % len(HEROES)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 3) % len(HEROES)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 3) % len(HEROES)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                return HEROES[self.selected]["id"]
            elif event.key == pygame.K_ESCAPE:
                return "back"
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, rect in enumerate(self.CARD_RECTS):
                if rect.collidepoint(event.pos):
                    self.selected = index
                    return HEROES[index]["id"]
        return None

    def draw(self, background, difficulty):
        background.draw()
        veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        veil.fill((8, 3, 16, 215))
        screen.blit(veil, (0, 0))
        pygame.draw.rect(screen, (14, 8, 24), (0, 548, WIDTH, 90))
        draw_centered_text(
            f"ESCOLHA SEU HERÓI — {DIFFICULTIES[difficulty]['name']}",
            (WIDTH // 2, 150),
            ORANGE,
            BIG,
        )
        for index, (hero, rect) in enumerate(zip(HEROES, self.CARD_RECTS)):
            selected = index == self.selected
            accent = HERO_WAVE_COLORS[hero["id"]]
            intensity = .18 if selected else .08
            card_color = tuple(
                min(255, PANEL[channel] + round(accent[channel] * intensity))
                for channel in range(3)
            )
            pygame.draw.rect(screen, card_color, rect, border_radius=12)
            if selected:
                pygame.draw.rect(
                    screen,
                    accent,
                    rect.inflate(8, 8),
                    2,
                    border_radius=15,
                )
            pygame.draw.rect(
                screen,
                accent,
                rect,
                3 if selected else 2,
                border_radius=12,
            )

            portrait = self.portrait_sprites.get(hero["id"])
            portrait_box = pygame.Rect(rect.x + 9, rect.y + 10, 78, rect.h - 20)
            if portrait is not None:
                scaled_width = portrait.get_width()
                scaled_height = portrait.get_height()
                portrait_frame = pygame.Rect(
                    portrait_box.centerx - scaled_width // 2 - 4,
                    portrait_box.centery - scaled_height // 2 - 4,
                    scaled_width + 8,
                    scaled_height + 8,
                )
                pygame.draw.rect(screen, (10, 8, 18), portrait_frame, border_radius=8)
                pygame.draw.rect(screen, accent, portrait_frame, 2, border_radius=8)
                screen.blit(
                    portrait,
                    (
                        portrait_box.centerx - scaled_width // 2,
                        portrait_box.centery - scaled_height // 2,
                    ),
                )

            text_x = rect.x + 96
            text_width = rect.right - text_x - 10
            draw_text(hero["name"], text_x, rect.y + 10, accent, FONT)
            draw_text(hero["ability"], text_x, rect.y + 33, ORANGE, SMALL)

            lines = wrap_text(hero["description"], SMALL, text_width)
            for line_index, line in enumerate(lines[:2]):
                draw_text(line, text_x, rect.y + 57 + line_index * 16, MUTED, SMALL)
            draw_text(
                f"Recarga: {hero['cooldown']} s",
                text_x,
                rect.bottom - 22,
                CYAN,
                SMALL,
            )

        draw_centered_text(
            "Setas / WASD e ENTER ou clique para escolher | ESC: voltar",
            (WIDTH // 2, 575),
            WHITE,
            FONT,
        )
        draw_centered_text(
            "Durante a partida, pressione G para usar o poder do herói.",
            (WIDTH // 2, 609),
            MUTED,
            SMALL,
        )

class TitleScreen:
    """Tela inicial: arte em 1100x720, texto piscando e brasas flutuando."""
    FADE_IN = 1.2

    def __init__(self):
        self.time = 0.0
        self.image = None
        path = os.path.join(BASE_DIR, "assets", "backgrounds", "tela_inicial.png")
        try:
            img = pygame.image.load(path).convert()
            if img.get_size() != (WIDTH, HEIGHT):
                img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            self.image = img
        except (pygame.error, OSError) as error:
            self.image = None   # sem a imagem, usa o fundo de reserva
            print(f"Não foi possível carregar a tela inicial '{path}': {error}", file=sys.stderr)
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
_MAP_CACHE = {}

def build_map_surface(path=PATH, scene=None):
    cache_key = scene["name"] if scene else "classic"
    if cache_key in _MAP_CACHE:
        return _MAP_CACHE[cache_key]

    surf = pygame.Surface((WIDTH, HEIGHT))
    background = None
    if scene:
        if scene["name"] not in _SCENE_BACKGROUND_CACHE:
            background_path = os.path.join(BASE_DIR, "assets", "backgrounds", f"{scene['name']}.png")
            try:
                image = pygame.image.load(background_path).convert()
                play_rect = map_play_rect_for_scene(scene)
                artwork = pygame.transform.smoothscale(image, play_rect.size)
                low_resolution = pygame.transform.smoothscale(image, (64, 48))
                backdrop = pygame.transform.smoothscale(low_resolution, MAP_RECT.size)
                _SCENE_BACKGROUND_CACHE[scene["name"]] = {
                    "artwork": artwork,
                    "backdrop": backdrop,
                }
            except (pygame.error, OSError) as error:
                _SCENE_BACKGROUND_CACHE[scene["name"]] = None
                print(f"Não foi possível carregar o cenário '{background_path}': {error}", file=sys.stderr)
        background = _SCENE_BACKGROUND_CACHE[scene["name"]]

    if background:
        surf.fill(BG)
        surf.blit(background["backdrop"], MAP_RECT.topleft)
        shade = pygame.Surface(MAP_RECT.size, pygame.SRCALPHA)
        shade.fill((12, 7, 20, 145))
        surf.blit(shade, MAP_RECT.topleft)
        play_rect = map_play_rect_for_scene(scene)
        surf.blit(background["artwork"], play_rect.topleft)
        pygame.draw.rect(surf, BORDER, play_rect, 2, border_radius=8)
        pygame.draw.rect(surf, BORDER, MAP_RECT, 2, border_radius=12)
        _MAP_CACHE[cache_key] = surf
        return surf

    surf.fill(BG)
    pygame.draw.rect(surf, GRASS_A, MAP_RECT, border_radius=12)
    play_rect = map_play_rect_for_scene(scene) if scene else MAP_RECT
    surf.set_clip(play_rect)
    rnd = random.Random(11)
    for gx in range(play_rect.left, play_rect.right, 28):
        for gy in range(play_rect.top, play_rect.bottom, 28):
            if ((gx - play_rect.left)//28 + (gy - play_rect.top)//28) % 2:
                pygame.draw.rect(surf, GRASS_B, (gx, gy, 28, 28))
    for _ in range(220):   # tufos de grama
        gx, gy = rnd.randint(play_rect.left, play_rect.right), rnd.randint(play_rect.top, play_rect.bottom)
        pygame.draw.line(surf, (24, 52, 40), (gx, gy), (gx-2, gy-5), 1)
        pygame.draw.line(surf, (24, 52, 40), (gx, gy), (gx+2, gy-5), 1)
    # estrada de terra
    pygame.draw.lines(surf, DIRT_EDGE, False, path, 46)
    for px, py in path:
        pygame.draw.circle(surf, DIRT_EDGE, (px, py), 23)
    pygame.draw.lines(surf, DIRT, False, path, 38)
    for px, py in path:
        pygame.draw.circle(surf, DIRT, (px, py), 19)
    for _ in range(140):   # pedrinhas
        i = rnd.randrange(len(path)-1)
        a, b = path[i], path[i+1]
        t = rnd.random()
        px = a[0] + (b[0]-a[0])*t + rnd.uniform(-13, 13)
        py = a[1] + (b[1]-a[1])*t + rnd.uniform(-13, 13)
        pygame.draw.circle(surf, (132, 100, 72), (int(px), int(py)), rnd.choice([1, 2]))
    # decoração (fora da estrada)
    placed = 0
    tries = 0
    scene_core = core_for_scene(scene) if scene else CORE
    while placed < 34 and tries < 600:
        tries += 1
        x = rnd.randint(play_rect.left + 16, play_rect.right - 16)
        y = rnd.randint(play_rect.top + 16, play_rect.bottom - 16)
        if any(point_segment_distance((x, y), path[i], path[i+1]) < 52 for i in range(len(path)-1)):
            continue
        if dist((x, y), scene_core) < 80:
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
    pygame.draw.rect(surf, BORDER, play_rect, 2, border_radius=8 if scene else 12)
    _MAP_CACHE[cache_key] = surf
    return surf

class Game:
    def __init__(self, difficulty="normal", hero_id="coan", equipped_skills=None):
        self.difficulty = difficulty
        self.difficulty_spec = DIFFICULTIES[difficulty]
        # o mapa é definido pela dificuldade e não muda entre as ondas
        self.scene = map_scene_for_difficulty(difficulty)
        self.path = path_for_scene(self.scene)
        self.core = core_for_scene(self.scene)
        self.play_rect = map_play_rect_for_scene(self.scene)
        if hero_id not in HERO_BY_ID:
            raise ValueError(f"Herói desconhecido: {hero_id}")
        self.hero_id = hero_id
        self.hero = HERO_BY_ID[hero_id]
        self.hero_map_sprite = HERO_MAP_SPRITES.get(hero_id)
        self.equipped_skills = set(profile.equipped_skills if equipped_skills is None else equipped_skills)
        self.money = 320 + (100 if "prepared_defense" in self.equipped_skills else 0)
        self.core_hp = 100
        self.towers = []
        self.enemies = []
        self.minions = []
        self.bullets = []
        self.particles = []
        self.wave = 0
        self.spawned = 0
        self.spawn_timer = 0
        self.spawn_batch_remaining = 0
        self.spawn_group_index = 0
        self.spawn_kind = None
        self.boss_spawned = False
        self.wave_brains_earned = 0
        self.wave_active = False
        self.wave_wait = False
        self.selected_kind = 0
        self.selected_tower = None
        self.message = "Clique em INICIAR ONDA para começar."
        self.message_time = 5
        self.auto_waves = profile.auto_waves
        self.auto_waves_button_rect = pygame.Rect(20, 572, 128, 30)
        self.start_wave_button_rect = pygame.Rect(158, 572, 132, 30)
        self.special_button_rect = pygame.Rect(300, 572, 128, 30)
        self.hero_button_rect = pygame.Rect(438, 572, 150, 30)
        self.upgrade_button_rect = pygame.Rect(598, 572, 198, 30)
        self.sell_button_rect = pygame.Rect(806, 572, 108, 30)
        self.skills_button_rect = pygame.Rect(924, 572, 156, 30)
        self.skill_close_button_rect = pygame.Rect(470, 520, 160, 38)
        self.tower_card_rects = [
            pygame.Rect(20 + index * 177, 610, 169, 96)
            for index in range(len(TOWER_TYPES))
        ]
        self.hero_targeting = False
        self.special_cooldown = 0
        self.special_wave_timer = 0
        self.hero_cooldown = 0
        self.hero_wave_timer = 0
        self.hero_wave_color = HERO_WAVE_COLORS[hero_id]
        self.hero_damage_timer = 0
        self.hero_fire_timer = 0
        self.paused = False
        self.pause_screen = "main"
        self.pause_selection = 0
        self.pause_button_rects = []
        self.confirm_button_rects = []
        self.skills_open = False
        self.bonus_damage = 1.1 if "sharpshooter" in self.equipped_skills else 1.0
        self.bonus_income = 1.15 if "harvest_bounty" in self.equipped_skills else 1.0
        self.fast_fire = .92 if "rapid_fire" in self.equipped_skills else 1.0
        self.barn_damage_multiplier = .9 if "reinforced_barn" in self.equipped_skills else 1.0
        self.special_cooldown_multiplier = .8 if "lunar_focus" in self.equipped_skills else 1.0
        self.special_damage_multiplier = 1.2 if "lunar_focus" in self.equipped_skills else 1.0
        self.completed = False
        self.lost = False
        self.score_saved = False
        self.result_saved = False
        self.result_save_attempted = False
        self.identity_save_error = None
        self.result_replay_rect = pygame.Rect(300, 595, 230, 50)
        self.result_menu_rect = pygame.Rect(570, 595, 230, 50)
        self.total_kills = 0
        self.total_upgrades = 0
        self.brains_earned = 0
        self.brain_save_error = None
        self.elapsed_seconds = 0
        self.run_started = False
        self.score_details = None
        self.ranking_save_error = None
        if self.auto_waves:
            self.start_wave()

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
            self.spawn_batch_remaining = 0
            self.spawn_group_index = 0
            self.boss_spawned = False
            self.wave_brains_earned = 0
            self.wave_wait = False
            boss_kind = boss_for_wave(self.wave)
            boss_notice = f" — CHEFÃO: {BOSS_NAMES[boss_kind]}" if boss_kind else ""
            self.notify(f"ONDA {self.wave+1}: {WAVES[self.wave]['name']}{boss_notice}", 4)

    def toggle_wave_mode(self):
        previous_mode = profile.auto_waves
        profile.auto_waves = not previous_mode
        error = profile.save()
        if error:
            profile.auto_waves = previous_mode
            self.auto_waves = previous_mode
            self.notify(f"Não foi possível salvar o modo das ondas: {error}")
            return

        self.auto_waves = profile.auto_waves
        mode_name = "AUTOMÁTICO" if self.auto_waves else "MANUAL"
        if self.auto_waves and not self.wave_active:
            self.start_wave()
        else:
            self.notify(f"Modo de ondas: {mode_name}.", 3)

    def use_special(self):
        if self.special_cooldown > 0:
            self.notify("O pulso lunar está recarregando.")
            return
        count = 0
        for e in self.enemies:
            if not e.dead and not e.reached:
                e.take_damage((42 + self.wave*8) * self.special_damage_multiplier)
                e.hit_flash = .15
                if e.dead:
                    count += 1
        self.special_cooldown = 12 * self.special_cooldown_multiplier
        self.special_wave_timer = .9
        self.notify(f"Pulso lunar! {count} monstro(s) eliminado(s).", 2)

    def use_hero_ability(self, target_pos):
        if not self.run_started:
            self.notify("Inicie a primeira onda antes de usar o poder do herói.")
            return False
        if self.hero_cooldown > 0:
            self.notify(f"{self.hero['ability']} recarregando: {math.ceil(self.hero_cooldown)} s.")
            return False

        enemies = [enemy for enemy in self.enemies if not enemy.dead and not enemy.reached]
        if self.hero_id in ("coan", "inacio", "jair") and not self.play_rect.collidepoint(target_pos):
            self.notify("Escolha uma área dentro do mapa.")
            return False

        affected = []
        if self.hero_id in ("coan", "inacio", "jair"):
            radius = 195 if self.hero_id == "coan" else 175
            affected = [
                enemy for enemy in enemies
                if dist(target_pos, (enemy.x, enemy.y)) <= radius
            ]
            if not affected:
                self.notify("Não há inimigos na área escolhida.")
                return False

        if self.hero_id == "coan":
            for enemy in affected:
                enemy.hero_slow_timer = max(enemy.hero_slow_timer, 5)
            self.notify(f"Devair: {len(affected)} inimigo(s) desacelerado(s) por 5 s.")
        elif self.hero_id == "capitao_nascimento":
            self.hero_damage_timer = 8
            self.notify("Monica: dano das torres +50% por 8 s.")
        elif self.hero_id == "devair":
            self.hero_fire_timer = 8
            self.notify("Coan: cadência das torres +50% por 8 s.")
        elif self.hero_id == "chico_bento":
            reward = 180 + self.wave * 25
            self.money += reward
            self.notify(f"Chico Bento: colheita farta! +{fmt_money(reward)} abóboras.")
        elif self.hero_id == "inacio":
            for enemy in affected:
                enemy.poison_timer = max(enemy.poison_timer, 5)
                enemy.poison_tick_timer = min(enemy.poison_tick_timer or .5, .5)
            self.notify(f"Carlos: {len(affected)} inimigo(s) envenenado(s) por 5 s.")
        elif self.hero_id == "jair":
            for enemy in affected:
                damage = enemy.max_hp * (0.35 if enemy.is_boss else 1)
                enemy.take_damage(damage)
                enemy.hit_flash = .2
            self.notify(f"Alessandre: Impacto atingiu {len(affected)} inimigo(s) na área.")

        self.hero_wave_color = HERO_WAVE_COLORS[self.hero_id]
        self.hero_wave_timer = .85
        self.hero_cooldown = self.hero["cooldown"]
        return True

    def begin_hero_ability(self):
        if self.hero_id in ("coan", "inacio", "jair"):
            if not self.run_started:
                self.notify("Inicie a primeira onda antes de usar o poder do herói.")
            elif self.hero_cooldown > 0:
                self.notify(f"{self.hero['ability']} recarregando: {math.ceil(self.hero_cooldown)} s.")
            else:
                self.hero_targeting = True
                self.notify("Clique na área do mapa onde deseja usar o poder.", 4)
            return
        self.use_hero_ability(self.play_rect.center)

    def buy_tower(self, pos):
        path_radius = 34 if self.scene else 28
        if (not self.play_rect.collidepoint(pos)
                or on_path(pos, self.path, path_radius)):
            self.notify("Posicione a torre fora da estrada dos monstros.")
            return
        if not profile.tower_is_unlocked(self.selected_kind):
            self.notify(f"{TOWER_TYPES[self.selected_kind]['name']} está bloqueada. Desbloqueie-a na árvore de habilidades do menu.")
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
        cost = tower_upgrade_cost(t.cost, t.level)
        if cost is None:
            self.notify(f"{TOWER_TYPES[t.kind]['name']} já está no nível máximo ({TOWER_MAX_LEVEL}).")
            return
        if self.money < cost:
            self.notify(f"Melhoria custa {fmt_money(cost)} abóboras.")
            return
        self.money -= cost
        if not t.upgrade():
            self.money += cost
            self.notify(f"{TOWER_TYPES[t.kind]['name']} já está no nível máximo ({TOWER_MAX_LEVEL}).")
            return
        self.total_upgrades += 1
        if t.level == TOWER_MAX_LEVEL:
            self.notify(f"{TOWER_TYPES[t.kind]['name']} chegou ao nível máximo! Dano massivamente aumentado.")
        else:
            self.notify(f"Torre melhorada para nível {t.level}.")

    def sell_selected(self):
        tower = self.selected_tower
        if tower is None:
            self.notify("Selecione uma torre para vender.")
            return
        refund = round(TOWER_TYPES[tower.kind]["cost"] * 0.7)
        tower_name = TOWER_TYPES[tower.kind]["name"]
        self.money += refund
        self.towers.remove(tower)
        self.selected_tower = None
        self.notify(f"{tower_name} vendida por {fmt_money(refund)} abóboras.")

    def calculate_score(self):
        health_points = round(5000 * max(0, min(self.core_hp, 100)) / 100)
        time_limit = 4 * 60 * self.difficulty_spec["wave_count"]
        upgrade_target = 2 * self.difficulty_spec["wave_count"]
        time_points = round(2000 * max(0, 1 - self.elapsed_seconds / time_limit))
        upgrade_points = round(1000 * min(self.total_upgrades / upgrade_target, 1))
        talent_points = round(500 * min(len(self.equipped_skills) / 3, 1))
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

    def save_completed_score(self, initials):
        if self.score_saved:
            return None
        if not profile.valid_initials(initials):
            raise ValueError("As iniciais do placar devem conter exatamente três letras.")
        if self.score_details is None:
            self.score_details = self.calculate_score()
        result = {
            "player": initials,
            "difficulty": self.difficulty,
            "score": self.score_details["score"],
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "time": round(self.elapsed_seconds),
            "core_hp": self.core_hp,
            "upgrades": self.total_upgrades,
            "talents": len(self.equipped_skills),
            "money": self.money,
        }
        self.ranking_save_error = leaderboard.add_result(result)
        if self.ranking_save_error is None:
            self.score_saved = True
        return self.ranking_save_error

    def save_player_result(self, initials):
        error = profile.confirm_user(initials)
        if error:
            self.identity_save_error = error
            return error
        if self.completed:
            error = self.save_completed_score(initials)
            if error:
                self.identity_save_error = error
                return error
        self.result_saved = True
        self.identity_save_error = None
        return None

    def update(self, dt):
        if self.paused:
            return
        self.message_time = max(0, self.message_time-dt)
        self.special_cooldown = max(0, self.special_cooldown-dt)
        self.special_wave_timer = max(0, self.special_wave_timer-dt)
        self.hero_cooldown = max(0, self.hero_cooldown-dt)
        self.hero_wave_timer = max(0, self.hero_wave_timer-dt)
        self.hero_damage_timer = max(0, self.hero_damage_timer-dt)
        self.hero_fire_timer = max(0, self.hero_fire_timer-dt)
        if self.skills_open or self.completed or self.lost:
            return
        if self.run_started:
            self.elapsed_seconds += dt
        if self.wave_active:
            self.spawn_timer -= dt
            spec = WAVES[self.wave]
            boss_kind = boss_for_wave(self.wave)
            if self.spawn_timer <= 0:
                if self.spawned < spec["count"] and self.spawn_batch_remaining == 0:
                    remaining = spec["count"] - self.spawned
                    batch_size = min(3, remaining)
                    pool = ENEMY_POOLS[min(self.wave, len(ENEMY_POOLS) - 1)]
                    eligible = [
                        kind for kind in pool
                        if not ENEMY_ARCHETYPES[kind]["pack"] or batch_size >= 3
                    ]
                    self.spawn_kind = eligible[self.spawn_group_index % len(eligible)]
                    self.spawn_group_index += 1
                    self.spawn_batch_remaining = batch_size
                if self.spawned < spec["count"]:
                    self.enemies.append(Monster(self.wave, self.difficulty, self.spawn_kind))
                    self.spawned += 1
                    self.spawn_batch_remaining -= 1
                    self.spawn_timer = .08 if self.spawn_batch_remaining else max(.35, .86 - self.wave*.035)
                elif boss_kind and not self.boss_spawned:
                    self.enemies.append(Monster(self.wave, self.difficulty, boss_kind))
                    self.boss_spawned = True
                    self.spawn_timer = 0
        for m in self.minions:
            m.update(dt, self.enemies)
        self.minions = [m for m in self.minions if not m.dead]
        for e in self.enemies:
            e.vigor_multiplier = 1
        pop_kings = [e for e in self.enemies if not e.dead and e.kind == "pop_king"]
        for boss in pop_kings:
            for enemy in self.enemies:
                if enemy is not boss and not enemy.dead and dist((boss.x, boss.y), (enemy.x, enemy.y)) <= 125:
                    enemy.vigor_multiplier = 1.25
        for enemy in self.enemies:
            if enemy.poison_timer > 0 and not enemy.dead and not enemy.reached:
                enemy.poison_timer = max(0, enemy.poison_timer - dt)
                enemy.poison_tick_timer -= dt
                if enemy.poison_tick_timer <= 0:
                    enemy.take_damage(enemy.max_hp * 0.06)
                    enemy.hit_flash = .1
                    enemy.poison_tick_timer = 1
        summoned_enemies = []
        for e in self.enemies:
            if not e.dead and not e.reached:
                near_summon = not e.ignores_summons and any(
                    dist((m.x, m.y), (e.x, e.y)) <= m.radius + e.radius + 3
                    for m in self.minions
                )
                e.slow_factor = .3 if near_summon else 1
                if "frost_runes" in self.equipped_skills:
                    e.slow_factor = min(e.slow_factor, .85)
                summoned_enemies.extend(e.update(dt, self.minions))
            if e.reached and not e.dead:
                e.dead = True
                self.core_hp -= int(
                    (10 + self.wave*2) * self.difficulty_spec["core_damage"]
                    * self.barn_damage_multiplier
                )
                self.notify("Um monstro invadiu o celeiro! Integridade reduzida.", 2)
                if self.core_hp <= 0:
                    self.lost = True
        for t in self.towers:
            level_index = t.level - 1
            spec = TOWER_TYPES[t.kind]
            t.damage = (
                spec["damage"] * TOWER_DAMAGE_MULTIPLIERS[level_index]
                * self.bonus_damage * (1.5 if self.hero_damage_timer > 0 else 1)
            )
            t.rate = (
                spec["rate"] * t.rate_multiplier * TOWER_RATE_MULTIPLIERS[level_index]
                / (1.5 if self.hero_fire_timer > 0 else 1)
            )
            t.range = spec["range"] * TOWER_RANGE_MULTIPLIERS[level_index]
            t.update(dt, self.enemies, self.bullets, self.minions)
        for b in self.bullets:
            b.update(dt, self.enemies)
        self.bullets = [b for b in self.bullets if not b.dead]
        for e in self.enemies:
            if e.dead and not getattr(e, "rewarded", False):
                if not e.reached:
                    summoned_enemies.extend(e.on_death())
                    if e.is_boss:
                        brains, brain_save_error = profile.award_brains(BOSS_BRAIN_REWARD)
                        if brain_save_error:
                            self.brain_save_error = brain_save_error
                            self.notify("Erro ao salvar os cérebros do chefão; consulte o menu.", 4)
                        else:
                            self.brain_save_error = None
                            self.brains_earned += brains
                            self.wave_brains_earned += brains
                if not e.reached:
                    self.money += int(e.reward*self.bonus_income)
                    self.total_kills += 1
                e.rewarded = True
                particle_count = 16 if e.kind == "skeleton_bomber" else 5
                for _ in range(particle_count):
                    self.particles.append([e.x,e.y,random.uniform(-70,70),random.uniform(-70,70),.35,e.kind])
        self.enemies.extend(summoned_enemies)
        self.enemies = [e for e in self.enemies if not e.dead]
        if (self.wave_active and not self.lost
                and self.spawned >= WAVES[self.wave]["count"]
                and (boss_for_wave(self.wave) is None or self.boss_spawned)
                and not self.enemies):
            self.wave_active = False
            self.wave += 1
            bonus = 40 + self.wave*15
            self.money += bonus
            if self.brain_save_error:
                brain_text = " Erro ao salvar cérebros; consulte o menu."
            elif self.wave_brains_earned:
                brain_text = f" +{self.wave_brains_earned} cérebros pelo chefão."
            else:
                brain_text = ""
            if self.wave >= self.difficulty_spec["wave_count"]:
                self.completed = True
                self.score_details = self.calculate_score()
                self.notify("FAZENDA PROTEGIDA — pressione ENTER para registrar suas iniciais!", 10)
            elif self.auto_waves:
                self.start_wave()
            else:
                self.notify(
                    f"Onda concluída! +{fmt_money(bonus)} abóboras.{brain_text} Clique em PRÓXIMA ONDA.",
                    5,
                )
        for p in self.particles:
            p[0] += p[2]*dt; p[1] += p[3]*dt; p[4] -= dt
        self.particles = [p for p in self.particles if p[4] > 0]
        if self.lost and self.score_details is None:
            self.score_details = self.calculate_score()

    def draw_barn(self, scene=None):
        if scene:
            cx, cy = self.core
            health = max(0, min(self.core_hp, 100))
            color = MINT if health > 60 else ORANGE if health > 30 else RED
            panel = pygame.Rect(cx - 8, cy - 49, 78, 24)
            pygame.draw.rect(screen, (18, 13, 27), panel, border_radius=7)
            pygame.draw.rect(screen, (107, 78, 124), panel, 1, border_radius=7)
            track = pygame.Rect(panel.x + 7, panel.y + 8, 64, 9)
            pygame.draw.rect(screen, (8, 7, 16), track, border_radius=4)
            if health:
                fill = track.copy()
                fill.width = round(track.width * health / 100)
                pygame.draw.rect(screen, color, fill, border_radius=4)
                shine = pygame.Rect(fill.x + 2, fill.y + 2, max(0, fill.width - 4), 2)
                if shine.width:
                    pygame.draw.rect(screen, (226, 255, 238), shine, border_radius=2)
            percent = SMALL.render(f"{health}%", True, color)
            screen.blit(percent, (panel.centerx - percent.get_width() // 2, panel.bottom - 1))
            return
        core = self.core
        cx, cy = core
        pygame.draw.rect(screen, (140, 42, 44), (cx-22, cy-12, 44, 34), border_radius=3)
        pygame.draw.polygon(screen, (92, 28, 32), [(cx-27, cy-10), (cx, cy-34), (cx+27, cy-10)])
        pygame.draw.polygon(screen, (60, 18, 22), [(cx-27, cy-10), (cx, cy-34), (cx+27, cy-10)], 2)
        pygame.draw.rect(screen, (70, 24, 28), (cx-8, cy+3, 16, 19))
        pygame.draw.line(screen, (230, 210, 190), (cx-8, cy+3), (cx+8, cy+22), 1)
        pygame.draw.line(screen, (230, 210, 190), (cx+8, cy+3), (cx-8, cy+22), 1)
        pygame.draw.circle(screen, (255, 220, 120), (cx, cy-14), 4)

    def draw_hero_at_base(self):
        if self.hero_map_sprite is None:
            return
        icon = self.hero_map_sprite
        frame = pygame.Rect(0, 0, icon.get_width() + 10, icon.get_height() + 10)
        core_x, core_y = self.core
        candidates = [
            frame.move(core_x + 14, core_y - frame.height // 2),
            frame.move(core_x - 14 - frame.width, core_y - frame.height // 2),
            frame.move(core_x - frame.width // 2, core_y + 14),
            frame.move(core_x - frame.width // 2, core_y - 14 - frame.height),
        ]
        valid_positions = [rect for rect in candidates if self.play_rect.contains(rect)]
        if not valid_positions:
            valid_positions = [rect for rect in candidates if MAP_RECT.contains(rect)]
        if not valid_positions:
            return
        if self.path:
            frame = max(
                valid_positions,
                key=lambda rect: min(
                    point_segment_distance(
                        rect.center,
                        self.path[index],
                        self.path[index + 1],
                    )
                    for index in range(len(self.path) - 1)
                ),
            )
        else:
            frame = valid_positions[0]

        screen.blit(
            icon,
            (frame.centerx - icon.get_width() // 2, frame.centery - icon.get_height() // 2),
        )

    def draw_map_wave(self, color, timer, duration, center, lunar=False):
        if timer <= 0:
            return
        progress = 1 - timer / duration
        max_radius = math.ceil(math.hypot(MAP_RECT.width, MAP_RECT.height))
        alpha = round(185 * (1 - progress))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.set_clip(MAP_RECT)
        overlay.fill((*color, round(15 * (1 - progress))), MAP_RECT)

        front_radius = max(1, round(max_radius * progress))
        for trail in range(3):
            radius = front_radius - trail * 72
            if radius <= 0:
                continue
            ring_alpha = max(25, alpha - trail * 42)
            pygame.draw.circle(
                overlay,
                (*color, ring_alpha),
                center,
                radius,
                5 if lunar and trail == 0 else 3,
            )

        if lunar:
            ray_inner = max(0, front_radius - 34)
            for angle_index in range(8):
                angle = math.tau * angle_index / 8
                start = (
                    round(center[0] + math.cos(angle) * ray_inner),
                    round(center[1] + math.sin(angle) * ray_inner),
                )
                end = (
                    round(center[0] + math.cos(angle) * front_radius),
                    round(center[1] + math.sin(angle) * front_radius),
                )
                pygame.draw.line(overlay, (*color, alpha), start, end, 2)
            pygame.draw.circle(
                overlay,
                (*color, alpha),
                center,
                max(5, round(18 * (1 - progress))),
                2,
            )
        screen.blit(overlay, (0, 0))

    def draw_map(self):
        _map_surface = build_map_surface(self.path, self.scene)
        screen.blit(_map_surface, (0, 0))
        self.draw_barn(self.scene)
        for t in self.towers:
            t.draw(screen, t is self.selected_tower)
        for m in self.minions:
            m.draw(screen)
        for e in self.enemies:
            if not e.is_boss:
                e.draw(screen)
        for b in self.bullets:
            b.draw(screen)
        for p in self.particles:
            color = KIND_COLORS.get(p[5], MINT)
            pygame.draw.circle(screen, color, (int(p[0]),int(p[1])), max(1,int(4*p[4]/.35)))
        for e in self.enemies:
            if e.is_boss:
                e.draw(screen)
        self.draw_map_wave(
            self.hero_wave_color,
            self.hero_wave_timer,
            .85,
            MAP_RECT.center,
        )
        self.draw_map_wave(
            (255, 226, 137),
            self.special_wave_timer,
            .9,
            self.core,
            lunar=True,
        )
        self.draw_hero_at_base()

    def draw_equipped_skills(self):
        overlay = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        overlay.fill((8,2,16,220))
        screen.blit(overlay,(0,0))
        pygame.draw.rect(screen, PANEL, (245,145,610,430), border_radius=16)
        pygame.draw.rect(screen, BORDER, (245,145,610,430), 2, border_radius=16)
        draw_text("HABILIDADES EQUIPADAS", 295, 168, ORANGE, BIG)
        draw_text("Este equipamento foi escolhido no menu com cérebros.", 295, 207, MUTED, SMALL)
        equipped = [skill for skill in SKILLS if skill["id"] in self.equipped_skills]
        if not equipped:
            draw_text("Nenhuma habilidade equipada. Escolha-as na árvore do menu.", 295, 265, WHITE, FONT)
        for index, skill in enumerate(equipped):
            y = 265 + index * 65
            pygame.draw.rect(screen, (44, 56, 40), (280, y, 535, 55), border_radius=9)
            pygame.draw.rect(screen, MINT, (280, y, 535, 55), 2, border_radius=9)
            draw_text(skill["name"], 296, y + 7, MINT, FONT)
            draw_text(skill["description"], 296, y + 31, WHITE, SMALL)
        draw_text(f"Cérebros disponíveis: {profile.brains}  |  Equipadas: {len(equipped)}/3", 295, 485, ORANGE, SMALL)
        pygame.draw.rect(screen, (42, 30, 58), self.skill_close_button_rect, border_radius=8)
        pygame.draw.rect(screen, MINT, self.skill_close_button_rect, 2, border_radius=8)
        draw_centered_text("FECHAR", self.skill_close_button_rect.center, MINT, SMALL)

    def draw_pause_overlay(self):
        if self.pause_screen == "settings":
            menu.draw_settings()
            return

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((8, 3, 16, 205))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(300, 190, 500, 370)
        pygame.draw.rect(screen, PANEL, panel, border_radius=16)
        pygame.draw.rect(screen, BORDER, panel, 2, border_radius=16)

        if self.pause_screen == "confirm":
            draw_text("VOLTAR AO MENU PRINCIPAL?", panel.x + 34, panel.y + 36, ORANGE, BIG)
            draw_text("O progresso desta campanha será perdido.", panel.x + 38, panel.y + 96, WHITE, FONT)
            draw_text("Tem certeza de que deseja sair?", panel.x + 38, panel.y + 126, MUTED, SMALL)
            buttons = [
                (pygame.Rect(panel.x + 32, panel.y + 225, 205, 52), "SAIR PARA O MENU"),
                (pygame.Rect(panel.x + 263, panel.y + 225, 205, 52), "CONTINUAR"),
            ]
            self.confirm_button_rects = [rect for rect, _ in buttons]
            for index, (rect, label) in enumerate(buttons):
                selected = index == self.pause_selection
                pygame.draw.rect(screen, (52, 56, 40) if selected else (36, 24, 54), rect, border_radius=9)
                pygame.draw.rect(screen, MINT if selected else BORDER, rect, 2, border_radius=9)
                draw_centered_text(label, rect.center, MINT if selected else WHITE, SMALL)
            draw_centered_text("← / → para escolher | ENTER confirma | ESC cancela", (panel.centerx, panel.y + 300), MUTED, SMALL)
            return

        draw_centered_text("JOGO PAUSADO", (panel.centerx, panel.y + 38), ORANGE, BIG)
        labels = ("CONTINUAR", "CONFIGURAÇÕES", "VOLTAR AO MENU PRINCIPAL")
        self.pause_button_rects = [
            pygame.Rect(panel.x + 50, panel.y + 105 + index * 70, panel.w - 100, 54)
            for index in range(len(labels))
        ]
        for index, (rect, label) in enumerate(zip(self.pause_button_rects, labels)):
            selected = index == self.pause_selection
            pygame.draw.rect(screen, (52, 56, 40) if selected else (36, 24, 54), rect, border_radius=9)
            pygame.draw.rect(screen, MINT if selected else BORDER, rect, 2, border_radius=9)
            draw_centered_text(label, rect.center, MINT if selected else WHITE, FONT)
        draw_centered_text("↑ / ↓ para escolher | ENTER seleciona | ESC continua", (panel.centerx, panel.bottom - 31), MUTED, SMALL)

    def draw_action_button(self, rect, label, color, enabled=True):
        fill = (42, 52, 40) if enabled else (31, 27, 38)
        border = color if enabled else (82, 76, 88)
        pygame.draw.rect(screen, fill, rect, border_radius=7)
        pygame.draw.rect(screen, border, rect, 2, border_radius=7)
        draw_centered_text(label, rect.center, color if enabled else MUTED, SMALL)

    def draw_result_overlay(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((4, 5, 16, 225))
        screen.blit(overlay, (0, 0))
        panel = pygame.Rect(48, 38, 1004, 644)
        pygame.draw.rect(screen, (11, 13, 27), panel, border_radius=18)
        pygame.draw.rect(screen, BORDER, panel, 2, border_radius=18)

        title_text = "FAZENDA PROTEGIDA!" if self.completed else "A COLHEITA FOI PERDIDA"
        title_color = MINT if self.completed else RED
        draw_centered_text(title_text, (panel.centerx, 75), title_color, BIG)
        draw_centered_text(
            f"JOGADOR {profile.active_user}  ·  {self.difficulty_spec['name']}",
            (panel.centerx, 112),
            CYAN,
            SMALL,
        )

        summary = pygame.Rect(72, 145, 438, 410)
        ranking = pygame.Rect(530, 145, 498, 410)
        for rect in (summary, ranking):
            pygame.draw.rect(screen, (17, 19, 35), rect, border_radius=12)
            pygame.draw.rect(screen, (81, 64, 100), rect, 1, border_radius=12)

        draw_text("RESUMO DA PARTIDA", 92, 162, ORANGE, FONT)
        if self.score_details is None:
            self.score_details = self.calculate_score()
        details = self.score_details
        score_text = BIG.render(f"{details['score']:,}".replace(",", "."), True, (255, 228, 92))
        screen.blit(score_text, (92, 195))
        draw_text("PONTUAÇÃO", 94, 232, MUTED, SMALL)

        if self.completed:
            outcome = "CAMPANHA CONCLUÍDA"
            outcome_color = MINT
        else:
            reached_wave = min(self.wave + 1, self.difficulty_spec["wave_count"])
            outcome = f"DERROTA NA ONDA {reached_wave}/{self.difficulty_spec['wave_count']}"
            outcome_color = RED
        draw_text(outcome, 92, 266, outcome_color, FONT)
        stats = [
            f"Integridade do celeiro: {self.core_hp}%",
            f"Tempo de campanha: {format_duration(self.elapsed_seconds)}",
            f"Inimigos eliminados: {self.total_kills}",
            f"Melhorias compradas: {self.total_upgrades}",
            f"Cérebros ganhos: {self.brains_earned}  ·  Saldo: {profile.brains}",
        ]
        for index, line in enumerate(stats):
            draw_text(line, 92, 305 + index * 31, WHITE if index < 4 else PURPLE, SMALL)
        if self.completed:
            draw_text(
                f"Multiplicador de dificuldade: {details['multiplier']:.2f}x",
                92,
                475,
                MUTED,
                SMALL,
            )
        else:
            draw_text("A campanha perdida não entra no ranking.", 92, 475, MUTED, SMALL)

        draw_text("PLACAR GLOBAL  ·  MELHORES JOGADORES", 550, 162, CYAN, FONT)
        draw_text("POS", 550, 198, MUTED, ARCADE_SMALL)
        draw_text("JOGADOR", 604, 198, MUTED, ARCADE_SMALL)
        draw_text("SCORE", 730, 198, MUTED, ARCADE_SMALL)
        draw_text("MODO", 910, 198, MUTED, ARCADE_SMALL)
        pygame.draw.line(screen, (69, 81, 102), (548, 222), (1010, 222), 1)

        records = leaderboard.all_records()
        for place, (entry, difficulty) in enumerate(records, 1):
            y = 232 + (place - 1) * 30
            if place == 1:
                color = (255, 228, 92)
            elif place == 2:
                color = (205, 222, 235)
            elif place == 3:
                color = (225, 151, 104)
            else:
                color = WHITE
            player = str(entry.get("player", "AAA")).upper()[:3].ljust(3, "A")
            if player == profile.active_user:
                pygame.draw.rect(screen, (31, 43, 47), (546, y - 3, 466, 26), border_radius=4)
            draw_text(f"{place:02}", 550, y, color, ARCADE_SMALL)
            draw_text(player, 604, y, MINT, ARCADE_SMALL)
            draw_text(f"{entry['score']:,}".replace(",", " "), 730, y, color, ARCADE_SMALL)
            draw_text(DIFFICULTIES[difficulty]["name"][:3], 910, y, PURPLE, ARCADE_SMALL)
        if not records:
            draw_centered_text(
                "AINDA NÃO HÁ PONTUAÇÕES SALVAS",
                (ranking.centerx, 340),
                MUTED,
                SMALL,
            )

        save_error = self.identity_save_error or self.ranking_save_error or self.brain_save_error
        if save_error:
            draw_wrapped_text(
                f"Falha ao salvar: {save_error}",
                88,
                561,
                924,
                RED,
                SMALL,
                max_lines=2,
            )
        buttons = [
            (self.result_replay_rect, "JOGAR NOVAMENTE" if self.result_saved else "TENTAR SALVAR", MINT),
            (self.result_menu_rect, "VOLTAR AO MENU", CYAN),
        ]
        for rect, label, color in buttons:
            pygame.draw.rect(screen, (29, 43, 43), rect, border_radius=9)
            pygame.draw.rect(screen, color, rect, 2, border_radius=9)
            draw_centered_text(label, rect.center, color, SMALL)
        draw_centered_text(
            "ENTER: jogar novamente  ·  ESC: menu",
            (panel.centerx, 660),
            MUTED,
            SMALL,
        )

    def draw_ui(self):
        pygame.draw.rect(screen, (18, 11, 29), (0, 0, WIDTH, 68))
        pygame.draw.line(screen, BORDER, (0, 68), (WIDTH, 68), 2)
        hud_items = [
            (24, "ABÓBORAS", fmt_money(self.money), ORANGE),
            (202, "CÉREBROS", str(profile.brains), PURPLE),
        ]
        for x, label, value, color in hud_items:
            pygame.draw.circle(screen, color, (x + 7, 34), 5)
            draw_text(label, x + 20, 10, MUTED, SMALL)
            draw_text(value, x + 20, 32, WHITE, FONT)
            pygame.draw.line(screen, (72, 55, 88), (x + 166, 14), (x + 166, 54), 1)

        core_color = MINT if self.core_hp > 60 else ORANGE if self.core_hp > 30 else RED
        draw_text("CELEIRO", 378, 10, MUTED, SMALL)
        draw_text(f"{self.core_hp}%", 378, 32, core_color, FONT)
        pygame.draw.line(screen, (72, 55, 88), (548, 14), (548, 54), 1)

        wave_count = self.difficulty_spec["wave_count"]
        pygame.draw.circle(screen, CYAN, (573, 34), 5)
        draw_text("ONDA", 586, 10, MUTED, SMALL)
        draw_text(f"{min(self.wave+1,wave_count)}/{wave_count}", 586, 32, WHITE, FONT)
        pygame.draw.line(screen, (72, 55, 88), (716, 14), (716, 54), 1)

        pygame.draw.circle(screen, (255, 142, 105), (741, 34), 5)
        draw_text("ELIMINADOS", 754, 10, MUTED, SMALL)
        draw_text(str(self.total_kills), 754, 32, WHITE, FONT)
        pygame.draw.line(screen, (72, 55, 88), (887, 14), (887, 54), 1)

        hero_color = HERO_WAVE_COLORS[self.hero_id]
        pygame.draw.circle(screen, hero_color, (912, 34), 5)
        draw_text("HERÓI", 925, 10, MUTED, SMALL)
        draw_text(self.hero["name"], 925, 32, hero_color, FONT)

        pygame.draw.rect(screen, PANEL, (0, 565, WIDTH, 155))
        pygame.draw.line(screen, BORDER, (0, 565), (WIDTH, 565), 2)
        pulse_status = "PRONTO" if self.special_cooldown <= 0 else f"{math.ceil(self.special_cooldown)}s"
        hero_status = "PRONTO" if self.hero_cooldown <= 0 else f"{math.ceil(self.hero_cooldown)}s"
        wave_button_label = (
            "ONDA EM CURSO"
            if self.wave_active
            else "INICIAR ONDA" if self.wave == 0 else "PRÓXIMA ONDA"
        )
        self.draw_action_button(
            self.auto_waves_button_rect,
            f"ONDAS {'AUTO' if self.auto_waves else 'MANUAL'}",
            MINT if self.auto_waves else CYAN,
        )
        self.draw_action_button(
            self.start_wave_button_rect,
            wave_button_label,
            MUTED if self.wave_active or self.completed or self.lost else MINT,
            enabled=not self.wave_active and not self.completed and not self.lost,
        )
        self.draw_action_button(
            self.special_button_rect,
            f"PULSO {pulse_status}",
            (255, 218, 125),
            enabled=self.special_cooldown <= 0 and not self.completed and not self.lost,
        )
        self.draw_action_button(
            self.hero_button_rect,
            f"PODER {hero_status}",
            hero_color,
            enabled=self.hero_cooldown <= 0 and self.run_started and not self.completed and not self.lost,
        )

        selected = self.selected_tower
        upgrade_cost = tower_upgrade_cost(selected.cost, selected.level) if selected else None
        upgrade_label = (
            f"MELHORAR {fmt_money(upgrade_cost)}"
            if upgrade_cost is not None
            else "NÍVEL MÁXIMO" if selected
            else "MELHORAR TORRE"
        )
        self.draw_action_button(
            self.upgrade_button_rect,
            upgrade_label,
            selected.color if selected and upgrade_cost is not None else MUTED,
            enabled=selected is not None and upgrade_cost is not None,
        )
        refund = round(TOWER_TYPES[selected.kind]["cost"] * 0.7) if selected else 0
        self.draw_action_button(
            self.sell_button_rect,
            f"VENDER +{refund}" if selected else "VENDER",
            RED if selected else MUTED,
            enabled=selected is not None,
        )
        self.draw_action_button(self.skills_button_rect, "HABILIDADES", PURPLE)

        for i, spec in enumerate(TOWER_TYPES):
            selected = self.selected_kind == i
            unlocked = profile.tower_is_unlocked(i)
            card_color = spec["color"] if unlocked else MUTED
            card = self.tower_card_rects[i]
            pygame.draw.rect(screen, (52, 34, 72) if selected else (36, 24, 54), card, border_radius=9)
            pygame.draw.rect(screen, card_color if selected or unlocked else BORDER, card, 2, border_radius=9)
            draw_wrapped_text(spec["name"], card.x + 8, card.y + 6, card.w - 16, card_color, SMALL, max_lines=1)
            if unlocked:
                draw_text(f"{fmt_money(spec['cost'])} abóboras", card.x + 8, card.y + 27, WHITE, SMALL)
                draw_wrapped_text(
                    spec["desc"],
                    card.x + 8,
                    card.y + 49,
                    card.w - 16,
                    MUTED,
                    SMALL,
                    max_lines=2,
                )
            else:
                draw_text("BLOQUEADA", card.x + 8, card.y + 29, ORANGE, SMALL)
                draw_wrapped_text(
                    "Desbloqueie na árvore de habilidades",
                    card.x + 8,
                    card.y + 51,
                    card.w - 16,
                    MUTED,
                    SMALL,
                    max_lines=2,
                )
        if self.message_time > 0:
            message_lines = wrap_text(self.message, FONT, 850)
            if len(message_lines) > 2:
                message_lines = message_lines[:2]
                message_lines[-1] = message_lines[-1].rstrip(" .") + "..."
            line_height = FONT.get_linesize()
            message_width = max(FONT.size(line)[0] for line in message_lines)
            box_width = min(880, message_width + 32)
            box = pygame.Rect(
                (WIDTH - box_width) // 2,
                82,
                box_width,
                len(message_lines) * line_height + 14,
            )
            pygame.draw.rect(screen,(40,26,60),box,border_radius=8)
            pygame.draw.rect(screen,BORDER,box,1,border_radius=8)
            for index, line in enumerate(message_lines):
                draw_centered_text(
                    line,
                    (box.centerx, box.y + 7 + index * line_height + FONT.get_height() // 2),
                    WHITE,
                    FONT,
                )
        if self.completed or self.lost:
            self.draw_result_overlay()

    def draw(self):
        screen.fill(BG)
        self.draw_map()
        self.draw_ui()
        if self.skills_open:
            self.draw_equipped_skills()
        if self.paused:
            self.draw_pause_overlay()

def toggle_fullscreen():
    if is_fullscreen():
        pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    else:
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

def is_fullscreen():
    surf = pygame.display.get_surface()
    return bool(surf and surf.get_flags() & pygame.FULLSCREEN)

def logical_mouse_position(position):
    window = pygame.display.get_surface()
    return (
        int(position[0] * WIDTH / window.get_width()),
        int(position[1] * HEIGHT / window.get_height()),
    )

def present_frame():
    window = pygame.display.get_surface()
    if window.get_size() != screen.get_size():
        pygame.transform.smoothscale(screen, window.get_size(), window)
    else:
        window.blit(screen, (0, 0))
    pygame.display.flip()

class MusicController:
    TRACKS = {
        "theme": "The_Organist_s_Final_Act_Tema.mp3",
        "facil": "Behind_The_Barricade_Fase_Fácil.mp3",
        "normal": "Weight_of_the_Headstone_Fase_Média.mp3",
        "dificil": "Teeth_Of_The_Caldera_Fase_Dificil.mp3",
        "boss": "Iron_Verdict_Chegada do chefe.mp3",
    }

    def __init__(self):
        self.current_track = None
        self.failed_tracks = set()
        self.unavailable = False
        self.volume = 0.55

    def set_volume(self, volume):
        self.volume = max(0.0, min(1.0, volume))
        if pygame.mixer.get_init() is not None:
            pygame.mixer.music.set_volume(self.volume)

    def play(self, track_id):
        if track_id == self.current_track or track_id in self.failed_tracks or self.unavailable:
            return
        if track_id not in self.TRACKS:
            raise ValueError(f"Trilha sonora desconhecida: {track_id}")
        track_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "assets",
            "soundtrack",
            self.TRACKS[track_id],
        )
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play(-1)
        except pygame.error as error:
            print(f"Não foi possível reproduzir a trilha sonora '{track_path}': {error}", file=sys.stderr)
            self.failed_tracks.add(track_id)
            if pygame.mixer.get_init() is None:
                self.unavailable = True
            return
        self.current_track = track_id

    def update(self, state, game):
        if state == "playing":
            boss_alive = any(
                enemy.is_boss and not enemy.dead and not enemy.reached
                for enemy in game.enemies
            )
            track_id = "boss" if boss_alive else game.difficulty
        else:
            track_id = "theme"
        self.play(track_id)


class MenuScreen:
    """Menu principal: arte com os botões; seleção por mouse ou teclado."""
    ITEMS = [
        ("JOGAR", "play"),
        ("ÁRVORE DE HABILIDADES", "skills"),
        ("RANKING", "ranking"),
        ("COMO JOGAR", "howto"),
        ("CONFIGURAÇÕES", "settings"),
        ("SAIR", "quit"),
    ]
    RECTS = [
        pygame.Rect(52, 326, 250, 45),
        pygame.Rect(52, 375, 250, 47),
        pygame.Rect(52, 428, 250, 47),
        pygame.Rect(52, 482, 250, 45),
        pygame.Rect(52, 534, 250, 46),
        pygame.Rect(52, 585, 250, 45),
    ]
    SKILL_NODE_SOURCE_CENTERS = [
        (1050, 210),
        (1140, 365),
        (1305, 210),
        (990, 500),
        (930, 365),
        (1305, 500),
        (1400, 640),
    ]
    TOWER_NODE_ORDER = [1, 2, 3, 4, 5]
    TOWER_NODE_SOURCE_CENTERS = [
        (424, 207),
        (282, 388),
        (562, 388),
        (424, 578),
        (424, 766),
    ]
    FADE_IN = 0.5
    GREEN = (120, 255, 130)

    def __init__(self):
        self.time = 0.0
        self.sel = 0
        self.panel = None   # None | "settings" | "howto" | "ranking" | "skills"
        self.volume_dragging = False
        self.skill_message = "Selecione um nó para consultar e alterar a habilidade."
        self.skill_selected = 0
        self.tower_message = "Selecione uma torre e use o botão para desbloqueá-la."
        self.tower_selected = 0
        self.tree_selection = None
        self.tree_hover = None
        self.skill_tree_image = None
        self.skill_action_rect = pygame.Rect(850, 635, 220, 52)
        self.profile_button_rect = pygame.Rect(890, 18, 190, 42)
        self.image = None
        path = os.path.join(BASE_DIR, "assets", "backgrounds", "menu_principal.png")
        try:
            img = pygame.image.load(path).convert()
            if img.get_size() != (WIDTH, HEIGHT):
                img = pygame.transform.smoothscale(img, (WIDTH, HEIGHT))
            self.image = img
        except (pygame.error, OSError) as error:
            self.image = None
            print(f"Não foi possível carregar o menu principal '{path}': {error}", file=sys.stderr)
        skill_tree_path = os.path.join(BASE_DIR, "assets", "backgrounds", "arvore_habilidades.png")
        try:
            source = pygame.image.load(skill_tree_path).convert()
            self.skill_tree_image = pygame.transform.smoothscale(source, (WIDTH, 545))
        except (pygame.error, OSError) as error:
            print(f"Não foi possível carregar a árvore de habilidades '{skill_tree_path}': {error}", file=sys.stderr)

    def enter(self):
        self.time = 0.0
        self.panel = None
        self.tree_selection = None
        self.tree_hover = None
        self.skill_message = "Clique em uma habilidade para ver os detalhes."
        self.tower_message = "Clique em uma torre para ver os detalhes."

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
            if event.type == pygame.KEYDOWN:
                if self.panel == "skills" and event.key in (
                    pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,
                    pygame.K_5, pygame.K_6, pygame.K_7,
                ):
                    index = event.key - pygame.K_1
                    self.skill_selected = index
                    self.tree_selection = ("skill", index)
                elif self.panel == "skills" and event.key in (
                    pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE
                ):
                    self.activate_selected_tree_node()
                elif self.panel == "settings" and event.key in (
                    pygame.K_LEFT, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_UP
                ):
                    change = 0.05 if event.key in (pygame.K_RIGHT, pygame.K_UP) else -0.05
                    music.set_volume(music.volume + change)
                elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_SPACE, pygame.K_BACKSPACE):
                    back = True
            elif event.type == pygame.MOUSEMOTION:
                if self.panel == "settings" and self.volume_dragging:
                    self.set_volume_from_x(event.pos[0])
                elif self.panel == "skills":
                    self.tree_hover = self.tree_node_at(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.panel == "settings" and self.toggle_rect().collidepoint(event.pos):
                    toggle_fullscreen()
                elif self.panel == "settings" and self.volume_slider_rect().inflate(0, 24).collidepoint(event.pos):
                    self.volume_dragging = True
                    self.set_volume_from_x(event.pos[0])
                elif self.panel == "skills" and self.skill_back_rect().collidepoint(event.pos):
                    back = True
                elif self.panel == "skills":
                    if self.skill_action_rect.collidepoint(event.pos):
                        self.activate_selected_tree_node()
                    else:
                        selection = self.tree_node_at(event.pos)
                        if selection is not None:
                            self.tree_selection = selection
                            self.tree_hover = selection
                            kind, index = selection
                            if kind == "skill":
                                self.skill_selected = index
                                self.skill_message = "Use o botão para comprar, equipar ou remover."
                            else:
                                self.tower_selected = index
                                self.tower_message = "Use o botão para desbloquear a torre."
                            self.activate_selected_tree_node()
                elif self.back_rect().collidepoint(event.pos) or not self.panel_rect().collidepoint(event.pos):
                    back = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.volume_dragging = False
            if back:
                self.panel = None
                self.volume_dragging = False
            return None
        if event.type == pygame.MOUSEMOTION:
            for i, r in enumerate(self.RECTS):
                if r.collidepoint(event.pos):
                    self.sel = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.profile_button_rect.collidepoint(event.pos):
                return "profile"
            for i, r in enumerate(self.RECTS):
                if r.collidepoint(event.pos):
                    self.sel = i
                    return self.activate(i)
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
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
        if self.panel == "skills":
            return pygame.Rect(0, 0, WIDTH, HEIGHT)
        if self.panel == "howto":
            return pygame.Rect(110, 35, 880, 650)
        if self.panel == "ranking":
            return pygame.Rect(190, 60, 720, 600)
        return pygame.Rect(320, 200, 460, 330)

    def node_rects(self, source_centers, size):
        source_width, source_height = 1672, 941
        image_width = self.skill_tree_image.get_width() if self.skill_tree_image else WIDTH
        image_height = self.skill_tree_image.get_height() if self.skill_tree_image else round(WIDTH * source_height / source_width)
        scale_x = image_width / source_width
        scale_y = image_height / source_height
        return [
            pygame.Rect(
                round(x * scale_x) - size // 2,
                round(y * scale_y) - size // 2,
                size,
                size,
            )
            for x, y in source_centers
        ]

    def skill_node_rects(self):
        return self.node_rects(self.SKILL_NODE_SOURCE_CENTERS, 68)

    def tower_node_rects(self):
        return self.node_rects(self.TOWER_NODE_SOURCE_CENTERS, 72)

    def draw_skill_glow(self, center, color):
        pulse = (math.sin(self.time * 4.5) + 1) / 2
        glow = pygame.Surface((104, 104), pygame.SRCALPHA)
        glow_center = (52, 52)
        for radius, alpha in (
            (45, 8),
            (39, 12),
            (33, 17),
            (27, 22 + round(10 * pulse)),
        ):
            pygame.draw.circle(glow, (*color, alpha), glow_center, radius)
        screen.blit(glow, (center[0] - glow_center[0], center[1] - glow_center[1]))

    def tree_node_at(self, position):
        for index, rect in enumerate(self.skill_node_rects()):
            if rect.collidepoint(position):
                return "skill", index
        for index, rect in enumerate(self.tower_node_rects()):
            if rect.collidepoint(position):
                return "tower", index
        return None

    @staticmethod
    def skill_back_rect():
        return pygame.Rect(0, 0, 190, 58)

    def activate_selected_skill(self):
        skill = SKILLS[self.skill_selected]
        self.skill_message = profile.toggle_skill(skill)

    def activate_selected_tower(self):
        kind = self.TOWER_NODE_ORDER[self.tower_selected]
        self.tower_message = profile.unlock_tower(kind)

    def activate_selected_tree_node(self):
        if self.tree_selection is None:
            return
        kind, index = self.tree_selection
        if kind == "skill":
            self.skill_selected = index
            self.activate_selected_skill()
        else:
            self.tower_selected = index
            self.activate_selected_tower()

    def back_rect(self):
        r = self.panel_rect()
        return pygame.Rect(r.centerx - 70, r.bottom - 58, 140, 38)

    def toggle_rect(self):
        r = self.panel_rect()
        return pygame.Rect(r.right - 190, r.top + 98, 150, 38)

    def volume_slider_rect(self):
        r = self.panel_rect()
        return pygame.Rect(r.x + 28, r.y + 204, r.w - 56, 8)

    def set_volume_from_x(self, x):
        slider = self.volume_slider_rect()
        music.set_volume((x - slider.left) / slider.width)

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
        left_x, right_x, y = 145, 570, 112
        column_width = 385
        draw_text("OBJETIVO", left_x, y, MINT, FONT)
        draw_wrapped_text(
            "Proteja o celeiro até o fim da campanha. Se a integridade chegar a 0%, a colheita é perdida.",
            left_x,
            y + 26,
            column_width,
            WHITE,
            SMALL,
            max_lines=3,
        )
        draw_text("CAMPANHA", left_x, y + 91, MINT, FONT)
        draw_text("Fácil: 6 ondas  |  Médio: 9  |  Difícil: 12", left_x, y + 117, ORANGE, SMALL)
        draw_text("TORRES", left_x, y + 151, MINT, FONT)
        for i, spec in enumerate(TOWER_TYPES):
            ty = y + 179 + i * 23
            pygame.draw.circle(screen, spec["color"], (left_x + 7, ty + 8), 6)
            draw_wrapped_text(
                f"{spec['name']} — {spec['desc']} (custo {spec['cost']})",
                left_x + 22,
                ty,
                column_width - 22,
                WHITE,
                SMALL,
                max_lines=1,
            )
        draw_text("INIMIGOS", left_x, y + 326, MINT, FONT)
        draw_wrapped_text(
            "Zumbis são resistentes; esqueletos avançam em bandos; fantasmas ignoram Lápides. Morcegos, aranhas e traças são rápidos; vampiros regeneram; múmias e Frankenstein têm armadura.",
            left_x,
            y + 353,
            column_width,
            MUTED,
            SMALL,
            max_lines=5,
        )

        draw_text("CONTROLES", right_x, y, MINT, FONT)
        controls = [
            ("Clique no cartão", "escolher torre"),
            ("Clique no mapa", "posicionar fora da estrada"),
            ("Clique em uma torre", "selecionar e ver alcance"),
            ("MELHORAR", "melhorar a torre selecionada"),
            ("VENDER", "vender a torre selecionada"),
            ("PRÓXIMA ONDA", "iniciar a onda manual"),
            ("ONDAS", "alternar manual / automático"),
            ("PULSO", "ativar o pulso lunar"),
            ("PODER", "usar o poder do herói"),
            ("HABILIDADES", "ver habilidades equipadas"),
            ("ESC", "abrir pausa"),
        ]
        for i, (k, d) in enumerate(controls):
            cy = y + 31 + i * 23
            draw_text(k, right_x, cy, ORANGE, SMALL)
            draw_wrapped_text(d, right_x + 170, cy, column_width - 170, WHITE, SMALL, max_lines=1)
        draw_text("RECURSOS", right_x, y + 300, MINT, FONT)
        draw_wrapped_text(
            "Abóboras compram torres e melhorias. Cérebros desbloqueiam habilidades e torres na árvore do menu. Cada chefão derrotado concede 3 cérebros.",
            right_x,
            y + 328,
            column_width,
            MUTED,
            SMALL,
            max_lines=5,
        )

    def draw_skills(self):
        if self.skill_tree_image:
            screen.blit(self.skill_tree_image, (0, 0))
        else:
            screen.fill(BG)

        brain_count_patch = pygame.Surface((52, 42))
        brain_count_patch.fill(self.skill_tree_image.get_at((970, 28))[:3] if self.skill_tree_image else BG)
        screen.blit(brain_count_patch, (978, 7))
        draw_centered_text(str(profile.brains), (1002, 28), WHITE, BIG)

        for index, (skill, rect) in enumerate(zip(SKILLS, self.skill_node_rects())):
            unlocked = skill["id"] in profile.unlocked_skills
            equipped = skill["id"] in profile.equipped_skills
            prerequisite_unlocked = (
                index == 0
                or SKILLS[index - 1]["id"] in profile.unlocked_skills
            )
            color = (
                MINT if equipped
                else CYAN if unlocked
                else ORANGE if prerequisite_unlocked and profile.brains >= skill["cost"]
                else MUTED
            )
            selected = self.tree_selection == ("skill", index)
            hovered = self.tree_hover == ("skill", index)
            if selected or hovered:
                self.draw_skill_glow(rect.center, color)
            pygame.draw.circle(
                screen,
                color,
                rect.center,
                36,
                4 if selected else 3 if hovered else 2,
            )
            badge_center = (rect.right - 2, rect.top + 4)
            pygame.draw.circle(screen, color, badge_center, 11)
            draw_centered_text(str(index + 1), badge_center, BG, SMALL)

        for index, (kind, rect) in enumerate(zip(self.TOWER_NODE_ORDER, self.tower_node_rects())):
            unlock = TOWER_UNLOCK_BY_KIND[kind]
            unlocked = profile.tower_is_unlocked(kind)
            can_unlock = (
                profile.brains >= unlock["cost"]
                and all(profile.tower_is_unlocked(required) for required in unlock["requires"])
            )
            color = MINT if unlocked else ORANGE if can_unlock else MUTED
            selected = self.tree_selection == ("tower", index)
            hovered = self.tree_hover == ("tower", index)
            if selected or hovered:
                self.draw_skill_glow(rect.center, color)
            pygame.draw.circle(
                screen,
                color,
                rect.center,
                38,
                4 if selected else 3 if hovered else 2,
            )
            badge_center = (rect.right - 2, rect.top + 4)
            pygame.draw.circle(screen, color, badge_center, 11)
            draw_centered_text(str(index + 1), badge_center, BG, SMALL)

        bottom_y = 545
        bottom = pygame.Surface((WIDTH, HEIGHT - bottom_y), pygame.SRCALPHA)
        bottom.fill((10, 5, 20, 255))
        screen.blit(bottom, (0, bottom_y))
        pygame.draw.line(screen, PURPLE, (0, bottom_y), (WIDTH, bottom_y), 2)

        if self.tree_selection is None:
            node_type, node_index = None, None
            detail = (
                "ÁRVORE DE HABILIDADES",
                "Clique em uma habilidade ou torre para consultar os detalhes.",
                "Passe o mouse apenas para destacar um nó.",
            )
            action, action_color = "SELECIONE UM NÓ", MUTED
        else:
            node_type, node_index = self.tree_selection
        if node_type == "skill":
            item = SKILLS[node_index]
            unlocked = item["id"] in profile.unlocked_skills
            equipped = item["id"] in profile.equipped_skills
            prerequisite = SKILLS[node_index - 1] if node_index > 0 else None
            prerequisite_unlocked = (
                prerequisite is None
                or prerequisite["id"] in profile.unlocked_skills
            )
            if equipped:
                status, action, action_color = "EQUIPADA", "DESEQUIPAR", RED
            elif unlocked:
                status = "DESBLOQUEADA"
                action = "EQUIPAR"
                action_color = MINT if len(profile.equipped_skills) < profile.MAX_EQUIPPED_SKILLS else MUTED
            elif not prerequisite_unlocked:
                status = f"REQUER: {prerequisite['name']}"
                action = "BLOQUEADA"
                action_color = MUTED
            else:
                status = f"CUSTO: {item['cost']} CÉREBROS"
                action = f"COMPRAR · {item['cost']}"
                action_color = MINT if profile.brains >= item["cost"] else MUTED
            detail = (
                f"HABILIDADE  {node_index + 1}. {item['name']}",
                item["description"],
                f"{status}  |  EQUIPADAS: {len(profile.equipped_skills)}/{profile.MAX_EQUIPPED_SKILLS}",
            )
        elif node_type == "tower":
            kind = self.TOWER_NODE_ORDER[node_index]
            item = TOWER_TYPES[kind]
            unlock = TOWER_UNLOCK_BY_KIND[kind]
            missing = [
                TOWER_TYPES[required]["name"]
                for required in unlock["requires"]
                if not profile.tower_is_unlocked(required)
            ]
            unlocked = profile.tower_is_unlocked(kind)
            if unlocked:
                status, action, action_color = "DESBLOQUEADA", "JÁ DESBLOQUEADA", MINT
            elif missing:
                status = "REQUER: " + " e ".join(missing)
                action, action_color = "PRÉ-REQUISITOS", MUTED
            else:
                status = f"CUSTO: {unlock['cost']} CÉREBROS"
                action = f"DESBLOQUEAR · {unlock['cost']}"
                action_color = MINT if profile.brains >= unlock["cost"] else MUTED
            detail = (
                f"TORRE  {node_index + 1}. {item['name']}",
                item["desc"],
                f"{status}  |  CUSTO NA PARTIDA: {fmt_money(item['cost'])} ABÓBORAS",
            )

        draw_text(detail[0], 30, 555, ORANGE, BIG)
        draw_wrapped_text(detail[1], 30, 588, 760, WHITE, SMALL, max_lines=2)
        draw_text(detail[2], 30, 627, PURPLE, SMALL)
        message = (
            self.skill_message if node_type == "skill"
            else self.tower_message if node_type == "tower"
            else "Sua seleção só muda ao clicar em um nó."
        )
        message_color = RED if (
            profile.last_error
            or "insuficientes" in message
            or "Limite" in message
            or "Desbloqueie primeiro" in message
        ) else MINT
        draw_wrapped_text(message, 30, 660, 760, message_color, SMALL, max_lines=2)

        pygame.draw.rect(screen, (42, 30, 58), self.skill_action_rect, border_radius=9)
        pygame.draw.rect(screen, action_color, self.skill_action_rect, 2, border_radius=9)
        draw_centered_text(action, self.skill_action_rect.center, action_color, SMALL)
        draw_centered_text("PASSE: DESTAQUE  |  CLIQUE: VER / APLICAR", (960, 700), MUTED, SMALL)

    def draw_ranking(self):
        screen.fill((3, 5, 13))
        board = pygame.Rect(130, 48, 840, 620)
        pygame.draw.rect(screen, (7, 12, 20), board)
        pygame.draw.rect(screen, CYAN, board, 4)
        pygame.draw.rect(screen, (29, 71, 66), board.inflate(-14, -14), 2)

        title = ARCADE_FONT.render("H I G H   S C O R E S", True, (255, 228, 92))
        screen.blit(title, (board.centerx - title.get_width() // 2, 72))
        subtitle = ARCADE_SMALL.render("HARVEST DEFENSE  //  LOCAL ARCADE", True, MINT)
        screen.blit(subtitle, (board.centerx - subtitle.get_width() // 2, 108))
        pygame.draw.line(screen, PURPLE, (165, 140), (935, 140), 2)

        headers = [
            (178, "RANK"),
            (285, "INITIALS"),
            (435, "SCORE"),
            (620, "MODE"),
            (760, "DATE"),
        ]
        for x, header in headers:
            draw_text(header, x, 160, CYAN, ARCADE_SMALL)
        pygame.draw.line(screen, (29, 71, 66), (165, 188), (935, 188), 1)

        records = leaderboard.all_records()
        for place, (entry, difficulty) in enumerate(records, 1):
            y = 204 + (place - 1) * 36
            if place == 1:
                color = (255, 228, 92)
            elif place == 2:
                color = (205, 222, 235)
            elif place == 3:
                color = (225, 151, 104)
            else:
                color = WHITE
            draw_text(f"{place:02}", 190, y, color, ARCADE_SMALL)
            initials = "".join(
                char for char in str(entry.get("player", "AAA")).upper() if "A" <= char <= "Z"
            )[:3].ljust(3, "A")
            draw_text(initials, 300, y, MINT, ARCADE_SMALL)
            score = f"{entry['score']:,}".replace(",", " ")
            draw_text(score, 435, y, color, ARCADE_SMALL)
            draw_text(DIFFICULTIES[difficulty]["name"][:3], 635, y, PURPLE, ARCADE_SMALL)
            draw_text(str(entry.get("date", ""))[:10], 760, y, (135, 173, 188), ARCADE_SMALL)
            if place == 1:
                draw_text("*", 875, y, (255, 228, 92), ARCADE_SMALL)

        if not records:
            message = ARCADE_SMALL.render("NO SCORES YET - PLAY TO ENTER", True, MUTED)
            screen.blit(message, (board.centerx - message.get_width() // 2, 300))
        pygame.draw.line(screen, PURPLE, (165, 566), (935, 566), 2)
        footer = ARCADE_SMALL.render("TOP 10  //  ENTER / ESC: BACK", True, MINT)
        screen.blit(footer, (board.centerx - footer.get_width() // 2, 576))
        back = self.back_rect()
        pygame.draw.rect(screen, (12, 25, 31), back)
        pygame.draw.rect(screen, CYAN, back, 2)
        draw_centered_text("VOLTAR", back.center, CYAN, ARCADE_SMALL)

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
        draw_text("Volume da música", r.x + 28, r.y + 162, WHITE, FONT)
        slider = self.volume_slider_rect()
        pygame.draw.rect(screen, (75, 57, 91), slider, border_radius=4)
        filled = pygame.Rect(slider.left, slider.top, round(slider.width * music.volume), slider.height)
        if filled.width:
            pygame.draw.rect(screen, MINT, filled, border_radius=4)
        knob_x = slider.left + round(slider.width * music.volume)
        pygame.draw.circle(screen, WHITE, (knob_x, slider.centery), 9)
        draw_text(f"{round(music.volume * 100)}%", r.right - 62, r.y + 162, ORANGE, FONT)
        draw_text("Arraste o controle ou use ← / →.", r.x + 28, r.y + 226, MUTED, SMALL)

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
                draw_outlined(label, SMALL if len(label) > 12 else FONT, WHITE, r.center)
        self.draw_selection()
        if profile.active_user is not None:
            pygame.draw.rect(screen, (18, 11, 29), self.profile_button_rect, border_radius=8)
            pygame.draw.rect(screen, CYAN, self.profile_button_rect, 2, border_radius=8)
            draw_centered_text(
                f"JOGADOR  {profile.active_user}",
                self.profile_button_rect.center,
                WHITE,
                SMALL,
            )
        if self.panel == "howto":
            self.draw_howto()
        elif self.panel == "ranking":
            self.draw_ranking()
        elif self.panel == "skills":
            self.draw_skills()
        elif self.panel == "settings":
            self.draw_settings()
        if self.time < self.FADE_IN:
            fade = pygame.Surface((WIDTH, HEIGHT))
            fade.set_alpha(int(255 * (1 - self.time / self.FADE_IN)))
            screen.blit(fade, (0, 0))


leaderboard = Leaderboard()
profile = PlayerProfile()
player_screen = PlayerIdentificationScreen()
difficulty_screen = DifficultyScreen()
hero_selection_screen = HeroSelectionScreen()
selected_difficulty = "normal"
game = Game()
title = TitleScreen()
menu = MenuScreen()
music = MusicController()
state = "title"   # "title" -> tela inicial | "profile" -> identidade | "menu" -> menu principal
running = True
while running:
    dt = min(clock.tick(60)/1000, .04)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
        if event.type == pygame.VIDEORESIZE:
            pygame.display.set_mode(event.size, pygame.RESIZABLE)
            continue
        if event.type == pygame.WINDOWRESIZED:
            continue
        if hasattr(event, "pos"):
            event_data = event.dict.copy()
            event_data["pos"] = logical_mouse_position(event.pos)
            event = pygame.event.Event(event.type, event_data)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
            toggle_fullscreen()
            continue
        if state == "title":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    player_screen.reset()
                    state = "profile"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                player_screen.reset()
                state = "profile"
            continue
        if state == "profile":
            action = player_screen.handle_event(event)
            if action == "selected":
                menu.enter()
                state = "menu"
            elif action == "back":
                state = "menu"
            elif action == "title":
                title = TitleScreen()
                state = "title"
            continue
        if state == "menu":
            action = menu.handle_event(event)
            if action == "play":
                state = "difficulty"
            elif action == "profile":
                player_screen.reset()
                state = "profile"
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
                selected_difficulty = difficulty
                state = "hero_select"
            continue
        if state == "hero_select":
            hero_id = hero_selection_screen.handle_event(event)
            if hero_id == "back":
                state = "difficulty"
            elif hero_id:
                game = Game(selected_difficulty, hero_id)
                state = "playing"
            continue
        if state == "playing" and game.paused:
            if game.pause_screen == "settings":
                menu.handle_event(event)
                if menu.panel is None:
                    game.pause_screen = "main"
                    game.pause_selection = 0
            elif game.pause_screen == "confirm":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.pause_screen = "main"
                        game.pause_selection = 0
                    elif event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                        game.pause_selection = 1 - game.pause_selection
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if game.pause_selection == 0:
                            game.paused = False
                            menu.enter()
                            state = "menu"
                        else:
                            game.pause_screen = "main"
                            game.pause_selection = 0
                elif event.type == pygame.MOUSEMOTION:
                    for index, rect in enumerate(game.confirm_button_rects):
                        if rect.collidepoint(event.pos):
                            game.pause_selection = index
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for index, rect in enumerate(game.confirm_button_rects):
                        if rect.collidepoint(event.pos):
                            if index == 0:
                                game.paused = False
                                menu.enter()
                                state = "menu"
                            else:
                                game.pause_screen = "main"
                                game.pause_selection = 0
                            break
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        game.paused = False
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        game.pause_selection = (game.pause_selection - 1) % 3
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        game.pause_selection = (game.pause_selection + 1) % 3
                    elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if game.pause_selection == 0:
                            game.paused = False
                        elif game.pause_selection == 1:
                            game.pause_screen = "settings"
                            menu.panel = "settings"
                            menu.volume_dragging = False
                        else:
                            game.pause_screen = "confirm"
                            game.pause_selection = 1
                elif event.type == pygame.MOUSEMOTION:
                    for index, rect in enumerate(game.pause_button_rects):
                        if rect.collidepoint(event.pos):
                            game.pause_selection = index
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for index, rect in enumerate(game.pause_button_rects):
                        if rect.collidepoint(event.pos):
                            game.pause_selection = index
                            if index == 0:
                                game.paused = False
                            elif index == 1:
                                game.pause_screen = "settings"
                                menu.panel = "settings"
                                menu.volume_dragging = False
                            else:
                                game.pause_screen = "confirm"
                                game.pause_selection = 1
                            break
            continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and not (game.completed or game.lost):
                if game.skills_open:
                    game.skills_open = False
                elif game.hero_targeting:
                    game.hero_targeting = False
                    game.notify("Seleção da área cancelada.", 2)
                else:
                    game.paused = True
                    game.pause_screen = "main"
                    game.pause_selection = 0
            elif game.completed or game.lost:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    if game.result_saved:
                        game = Game(game.difficulty, game.hero_id)
                    elif profile.active_user:
                        game.save_player_result(profile.active_user)
                elif event.key == pygame.K_ESCAPE:
                    menu.enter()
                    state = "menu"
            elif game.skills_open:
                pass
            else:
                if event.key == pygame.K_SPACE:
                    game.start_wave()
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                    kind = event.key - pygame.K_1
                    if profile.tower_is_unlocked(kind):
                        game.selected_kind = kind
                    else:
                        game.notify(f"{TOWER_TYPES[kind]['name']} está bloqueada. Desbloqueie-a na árvore de habilidades do menu.")
                elif event.key in (pygame.K_q, pygame.K_w, pygame.K_e):
                    kind = {pygame.K_q: 0, pygame.K_w: 1, pygame.K_e: 2}[event.key]
                    if profile.tower_is_unlocked(kind):
                        game.selected_kind = kind
                    else:
                        game.notify(f"{TOWER_TYPES[kind]['name']} está bloqueada. Desbloqueie-a na árvore de habilidades do menu.")
                elif event.key == pygame.K_u:
                    game.upgrade_selected()
                elif event.key == pygame.K_v:
                    game.sell_selected()
                elif event.key == pygame.K_f:
                    game.use_special()
                elif event.key == pygame.K_g:
                    game.use_hero_ability(logical_mouse_position(pygame.mouse.get_pos()))
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if game.completed or game.lost:
                if game.result_replay_rect.collidepoint(pos):
                    if game.result_saved:
                        game = Game(game.difficulty, game.hero_id)
                    elif profile.active_user:
                        game.save_player_result(profile.active_user)
                elif game.result_menu_rect.collidepoint(pos):
                    menu.enter()
                    state = "menu"
            elif game.skills_open:
                if game.skill_close_button_rect.collidepoint(pos) or not pygame.Rect(245,145,610,430).collidepoint(pos):
                    game.skills_open = False
            elif game.hero_targeting:
                if game.play_rect.collidepoint(pos) and game.use_hero_ability(pos):
                    game.hero_targeting = False
            elif game.auto_waves_button_rect.collidepoint(pos):
                game.toggle_wave_mode()
            elif game.start_wave_button_rect.collidepoint(pos):
                game.start_wave()
            elif game.special_button_rect.collidepoint(pos):
                game.use_special()
            elif game.hero_button_rect.collidepoint(pos):
                game.begin_hero_ability()
            elif game.upgrade_button_rect.collidepoint(pos):
                game.upgrade_selected()
            elif game.sell_button_rect.collidepoint(pos):
                game.sell_selected()
            elif game.skills_button_rect.collidepoint(pos):
                game.skills_open = True
            elif MAP_RECT.collidepoint(pos):
                found = next((t for t in reversed(game.towers) if dist(pos,(t.x,t.y)) < 22),None)
                if found:
                    game.selected_tower=found
                else:
                    game.buy_tower(pos)
            elif any(rect.collidepoint(pos) for rect in game.tower_card_rects):
                for i in range(len(TOWER_TYPES)):
                    if game.tower_card_rects[i].collidepoint(pos):
                        if profile.tower_is_unlocked(i):
                            game.selected_kind=i
                        else:
                            game.notify(f"{TOWER_TYPES[i]['name']} está bloqueada. Desbloqueie-a na árvore de habilidades do menu.")
    music.update(state, game)
    if state == "title":
        title.update(dt)
        title.draw()
    elif state == "profile":
        player_screen.draw()
    elif state == "menu":
        menu.update(dt)
        menu.draw()
    elif state == "difficulty":
        difficulty_screen.draw(menu)
    elif state == "hero_select":
        hero_selection_screen.draw(menu, selected_difficulty)
    else:
        game.update(dt)
        if (game.completed or game.lost) and not game.result_save_attempted:
            game.result_save_attempted = True
            if profile.active_user:
                game.save_player_result(profile.active_user)
            else:
                game.identity_save_error = "Identifique um jogador antes de salvar o resultado."
        game.draw()
    present_frame()

pygame.quit()
sys.exit()
