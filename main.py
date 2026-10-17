import math
import random
import sys
import pygame

# BYTE DEFENSE — protótipo jogável em Pygame
# Controles: clique em uma torre no painel inferior e depois no mapa para posicioná-la.
# Clique em uma torre já colocada para selecioná-la. Espaço: iniciar/próxima onda.
# Q/W/E: selecionar torre. U: melhorar torre selecionada. F: pulso de firewall.
# ESC: sair.

pygame.init()
pygame.display.set_caption("BYTE DEFENSE — Proteja o núcleo")
WIDTH, HEIGHT = 1100, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 18)
SMALL = pygame.font.SysFont("consolas", 14)
BIG = pygame.font.SysFont("consolas", 30, bold=True)

BG = (9, 15, 27)
GRID = (17, 30, 47)
WHITE = (225, 240, 250)
MINT = (72, 245, 190)
CYAN = (61, 204, 255)
PURPLE = (177, 110, 255)
ORANGE = (255, 170, 70)
RED = (255, 75, 100)
MUTED = (130, 157, 180)
PANEL = (15, 26, 42)
BORDER = (39, 67, 91)

MAP_RECT = pygame.Rect(24, 80, 1052, 470)
CORE = (1000, 310)
PATH = [(30, 315), (165, 315), (165, 170), (360, 170), (360, 430),
        (560, 430), (560, 245), (760, 245), (760, 360), (1000, 360)]
# The path is drawn as a connected sequence; the final core is near its endpoint.
CORE = (1015, 360)
TOWER_TYPES = [
    {"name": "Sentinela", "cost": 90, "range": 145, "damage": 18, "rate": 0.65, "color": CYAN, "desc": "Disparo equilibrado"},
    {"name": "Firewall", "cost": 145, "range": 105, "damage": 9, "rate": 0.28, "color": ORANGE, "desc": "Rajada rápida"},
    {"name": "Sandbox", "cost": 180, "range": 175, "damage": 34, "rate": 1.15, "color": PURPLE, "desc": "Ataque pesado"},
]
WAVES = [
    {"count": 9, "hp": 38, "speed": 62, "reward": 24, "name": "Arquivos suspeitos"},
    {"count": 13, "hp": 54, "speed": 72, "reward": 30, "name": "Adware"},
    {"count": 15, "hp": 72, "speed": 80, "reward": 37, "name": "Spyware"},
    {"count": 17, "hp": 94, "speed": 88, "reward": 45, "name": "Ransomware"},
    {"count": 21, "hp": 125, "speed": 98, "reward": 58, "name": "Worm mestre"},
]

def fmt_bytes(n):
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(max(0, n))
    i = 0
    while value >= 1024 and i < len(units)-1:
        value /= 1024
        i += 1
    if i == 0:
        return f"{int(value)} {units[i]}"
    return f"{value:.2f} {units[i]}"

def draw_text(text, x, y, color=WHITE, font=FONT, surface=screen):
    surface.blit(font.render(str(text), True, color), (x, y))

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

class Malware:
    def __init__(self, wave):
        spec = WAVES[wave]
        self.x, self.y = PATH[0]
        self.segment = 0
        self.progress = 0.0
        self.max_hp = spec["hp"] * random.uniform(.82, 1.18)
        self.hp = self.max_hp
        self.speed = spec["speed"] * random.uniform(.88, 1.12)
        self.reward = spec["reward"]
        self.radius = random.choice([10, 11, 12]) + wave // 3
        self.kind = random.choice(["virus", "bug", "trojan"]) if wave < 3 else random.choice(["virus", "trojan", "worm"])
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
        step = self.speed * dt
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
        color = RED if self.kind == "trojan" else PURPLE if self.kind == "worm" else (255, 105, 130)
        if self.hit_flash > 0:
            color = WHITE
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(surface, color, (x, y), self.radius)
        pygame.draw.circle(surface, (35, 18, 42), (x, y), max(3, self.radius//2))
        # HP bar
        w = 30
        pygame.draw.rect(surface, (38, 48, 62), (x-w//2, y-self.radius-9, w, 4), border_radius=2)
        pygame.draw.rect(surface, MINT, (x-w//2, y-self.radius-9, int(w*max(0,self.hp/self.max_hp)), 4), border_radius=2)

class Tower:
    def __init__(self, pos, kind):
        spec = TOWER_TYPES[kind]
        self.x, self.y = pos
        self.kind = kind
        self.level = 1
        self.range = spec["range"]
        self.damage = spec["damage"]
        self.rate = spec["rate"]
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

    def update(self, dt, enemies, bullets):
        self.cooldown = max(0, self.cooldown-dt)
        candidates = [e for e in enemies if not e.dead and not e.reached and dist((self.x,self.y),(e.x,e.y)) <= self.range]
        if candidates:
            self.target = max(candidates, key=lambda e: e.segment + e.progress)
            self.angle = math.atan2(self.target.y-self.y, self.target.x-self.x)
            if self.cooldown <= 0:
                bullets.append(Bullet((self.x,self.y), self.target, self.damage, self.color))
                self.cooldown = self.rate
        else:
            self.target = None

    def draw(self, surface, selected=False):
        x, y = int(self.x), int(self.y)
        if selected:
            pygame.draw.circle(surface, (*self.color,), (x,y), int(self.range), 1)
        pygame.draw.circle(surface, (18, 38, 55), (x,y), 20)
        pygame.draw.circle(surface, self.color, (x,y), 15, 3)
        pygame.draw.line(surface, self.color, (x,y),
                         (x+int(math.cos(self.angle)*19), y+int(math.sin(self.angle)*19)), 5)
        draw_text(str(self.level), x-5, y-8, WHITE, SMALL)

class Bullet:
    def __init__(self, start, target, damage, color):
        self.x, self.y = start
        self.target = target
        self.damage = damage
        self.color = color
        self.speed = 420
        self.dead = False

    def update(self, dt):
        if self.target.dead or self.target.reached:
            self.dead = True
            return
        dx, dy = self.target.x-self.x, self.target.y-self.y
        length = math.hypot(dx,dy)
        if length < self.speed*dt + 5:
            self.target.hp -= self.damage
            self.target.hit_flash = .08
            if self.target.hp <= 0:
                self.target.dead = True
            self.dead = True
        elif length:
            self.x += dx/length*self.speed*dt
            self.y += dy/length*self.speed*dt

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x),int(self.y)), 4)

class Game:
    def __init__(self):
        self.money = 320
        self.core_hp = 100
        self.towers = []
        self.enemies = []
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

    def notify(self, text, seconds=3):
        self.message = text
        self.message_time = seconds

    def start_wave(self):
        if not self.wave_active and self.wave < len(WAVES) and not self.completed and not self.lost:
            self.wave_active = True
            self.spawned = 0
            self.spawn_timer = .2
            self.wave_wait = False
            self.notify(f"FASE {self.wave+1}: {WAVES[self.wave]['name']}", 3)

    def use_special(self):
        if self.special_cooldown > 0:
            self.notify("Pulso de firewall recarregando.")
            return
        count = 0
        for e in self.enemies:
            if not e.dead and not e.reached:
                e.hp -= 42 + self.wave*8
                e.hit_flash = .15
                if e.hp <= 0:
                    e.dead = True
                    self.money += int(e.reward*self.bonus_income)
                    self.total_kills += 1
                    count += 1
        self.special_cooldown = 12
        self.special_flash = .4
        self.notify(f"Pulso de firewall! {count} malware(s) eliminado(s).", 2)

    def buy_tower(self, pos):
        if not MAP_RECT.collidepoint(pos) or on_path(pos):
            self.notify("Posicione a torre fora da rota dos malwares.")
            return
        if any(dist(pos,(t.x,t.y)) < 40 for t in self.towers):
            self.notify("As torres precisam de espaço entre si.")
            return
        spec = TOWER_TYPES[self.selected_kind]
        if self.money < spec["cost"]:
            self.notify("Bytes insuficientes para essa torre.")
            return
        self.money -= spec["cost"]
        self.towers.append(Tower(pos, self.selected_kind))
        self.selected_tower = self.towers[-1]
        self.notify(f"{spec['name']} instalada!")

    def upgrade_selected(self):
        t = self.selected_tower
        if not t:
            self.notify("Selecione uma torre primeiro.")
            return
        cost = int(t.cost * (0.8 + .65*t.level))
        if self.money < cost:
            self.notify(f"Melhoria custa {fmt_bytes(cost)}.")
            return
        self.money -= cost
        t.upgrade()
        self.notify(f"Torre melhorada para nível {t.level}.")

    def buy_skill(self, index):
        if self.unlocked[index]:
            self.notify("Esse caminho já está desbloqueado.")
            return
        cost = self.tree_costs[index]
        if self.money < cost:
            self.notify(f"Árvore de habilidades: precisa de {fmt_bytes(cost)}.")
            return
        self.money -= cost
        self.unlocked[index] = True
        if index == 0:
            self.bonus_damage = 1.35
        elif index == 1:
            self.bonus_income = 1.3
        else:
            self.fast_fire = .78
            for t in self.towers:
                t.rate *= .78
        self.notify(["Cibersegurança: dano +35%.", "Criptomineração: recompensa +30%.", "Overclock: torres atacam mais rápido."][index], 4)

    def update(self, dt):
        self.message_time = max(0, self.message_time-dt)
        self.special_cooldown = max(0, self.special_cooldown-dt)
        self.special_flash = max(0, self.special_flash-dt)
        if self.paused or self.tree_open or self.completed or self.lost:
            return
        if self.wave_active:
            self.spawn_timer -= dt
            spec = WAVES[self.wave]
            if self.spawned < spec["count"] and self.spawn_timer <= 0:
                self.enemies.append(Malware(self.wave))
                self.spawned += 1
                self.spawn_timer = max(.24, .86 - self.wave*.1)
            if self.spawned >= spec["count"] and not any(not e.dead and not e.reached for e in self.enemies):
                self.wave_active = False
                self.wave += 1
                bonus = 80 + self.wave*35
                self.money += bonus
                self.notify(f"Fase concluída! Bônus: {fmt_bytes(bonus)}. Pressione ESPAÇO.", 5)
                if self.wave >= len(WAVES):
                    self.completed = True
                    self.notify("SISTEMA PROTEGIDO — Você venceu!", 10)
        for e in self.enemies:
            if not e.dead and not e.reached:
                e.update(dt)
            if e.reached and not e.dead:
                e.dead = True
                self.core_hp -= 10 + self.wave*2
                self.notify("Malware atingiu o núcleo! Integridade reduzida.", 2)
                if self.core_hp <= 0:
                    self.lost = True
        for t in self.towers:
            t.damage = TOWER_TYPES[t.kind]["damage"] * (1 + .42*(t.level-1)) * self.bonus_damage
            t.update(dt, self.enemies, self.bullets)
        for b in self.bullets:
            b.update(dt)
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
        for p in self.particles:
            p[0] += p[2]*dt; p[1] += p[3]*dt; p[4] -= dt
        self.particles = [p for p in self.particles if p[4] > 0]

    def draw_map(self):
        pygame.draw.rect(screen, (11,22,36), MAP_RECT, border_radius=12)
        for x in range(MAP_RECT.left, MAP_RECT.right, 28):
            pygame.draw.line(screen, GRID, (x,MAP_RECT.top), (x,MAP_RECT.bottom))
        for y in range(MAP_RECT.top, MAP_RECT.bottom, 28):
            pygame.draw.line(screen, GRID, (MAP_RECT.left,y), (MAP_RECT.right,y))
        pygame.draw.lines(screen, (30,67,86), False, PATH, 34)
        pygame.draw.lines(screen, (38,104,119), False, PATH, 3)
        for x,y in PATH:
            pygame.draw.circle(screen, (45,98,116), (x,y), 5)
        # Core
        pygame.draw.circle(screen, (22,48,68), CORE, 31)
        pygame.draw.circle(screen, MINT if self.core_hp > 35 else RED, CORE, 24, 3)
        pygame.draw.rect(screen, (20,38,55), (CORE[0]-16,CORE[1]-12,32,24), border_radius=4)
        draw_text("PC", CORE[0]-13, CORE[1]-10, WHITE, SMALL)
        if self.special_flash > 0:
            pygame.draw.circle(screen, CYAN, CORE, int(50+(0.4-self.special_flash)*220), 3)
        for t in self.towers:
            t.draw(screen, t is self.selected_tower)
        for e in self.enemies:
            e.draw(screen)
        for b in self.bullets:
            b.draw(screen)
        for p in self.particles:
            color = PURPLE if p[5] in ("worm","trojan") else MINT
            pygame.draw.circle(screen, color, (int(p[0]),int(p[1])), max(1,int(4*p[4]/.35)))

    def draw_tree(self):
        overlay = pygame.Surface((WIDTH,HEIGHT), pygame.SRCALPHA)
        overlay.fill((2,8,18,220))
        screen.blit(overlay,(0,0))
        pygame.draw.rect(screen, PANEL, (245,145,610,430), border_radius=16)
        pygame.draw.rect(screen, BORDER, (245,145,610,430), 2, border_radius=16)
        draw_text("ÁRVORE DE HABILIDADES", 295, 168, MINT, BIG)
        draw_text("Escolha caminhos diferentes para adaptar sua defesa.", 295, 207, MUTED, SMALL)
        nodes = [
            (280,265,"1  CIBERSEGURANÇA","Dano das torres +35%",self.unlocked[0],self.tree_costs[0]),
            (280,350,"2  CRIPTOMINERAÇÃO","Recompensas +30%",self.unlocked[1],self.tree_costs[1]),
            (280,435,"3  OVERCLOCK","Torres atacam mais rápido",self.unlocked[2],self.tree_costs[2]),
        ]
        for x,y,title,desc,owned,cost in nodes:
            pygame.draw.rect(screen,(20,52,63) if owned else (22,34,51),(x,y,535,65),border_radius=9)
            pygame.draw.rect(screen,MINT if owned else BORDER,(x,y,535,65),2,border_radius=9)
            draw_text(title,x+16,y+9,MINT if owned else WHITE,FONT)
            draw_text(desc,x+16,y+37,MUTED,SMALL)
            draw_text("DESBLOQUEADO" if owned else fmt_bytes(cost),x+370,y+24,MINT if owned else ORANGE,SMALL)
        draw_text("Clique em um caminho para desbloquear. ESC para voltar.", 295, 530, MUTED, SMALL)

    def draw_ui(self):
        pygame.draw.rect(screen, PANEL, (0,0,WIDTH,68))
        draw_text("BYTE DEFENSE", 24, 14, MINT, BIG)
        draw_text(f"BYTES  {fmt_bytes(self.money)}", 300, 16, WHITE, FONT)
        draw_text(f"NÚCLEO  {self.core_hp}%", 500, 16, MINT if self.core_hp>35 else RED, FONT)
        draw_text(f"FASE  {min(self.wave+1,5)}/5", 675, 16, WHITE, FONT)
        draw_text(f"ELIMINADOS  {self.total_kills}", 820, 16, CYAN, FONT)
        # Bottom panel
        pygame.draw.rect(screen, PANEL, (0,565,WIDTH,155))
        pygame.draw.line(screen, BORDER, (0,565),(WIDTH,565),2)
        draw_text("TORRES (Q / W / E para selecionar)", 24, 577, MUTED, SMALL)
        for i,spec in enumerate(TOWER_TYPES):
            x = 24+i*210
            selected = self.selected_kind == i
            pygame.draw.rect(screen,(28,57,74) if selected else (18,32,49),(x,602,195,70),border_radius=9)
            pygame.draw.rect(screen,spec["color"] if selected else BORDER,(x,602,195,70),2,border_radius=9)
            draw_text(f"{i+1}. {spec['name']}",x+12,609,spec["color"],FONT)
            draw_text(f"{fmt_bytes(spec['cost'])}  |  {spec['desc']}",x+12,638,WHITE,SMALL)
        draw_text("ESPAÇO: onda", 670, 585, WHITE, SMALL)
        draw_text("F: pulso firewall", 670, 606, CYAN, SMALL)
        draw_text(f"Pulso: {'PRONTO' if self.special_cooldown<=0 else str(int(self.special_cooldown))+'s'}", 670, 627, MINT if self.special_cooldown<=0 else MUTED, SMALL)
        draw_text("U: melhorar torre", 670, 648, WHITE, SMALL)
        draw_text("T: árvore de habilidades", 850, 585, PURPLE, SMALL)
        if self.selected_tower:
            t=self.selected_tower
            cost=int(t.cost*(.8+.65*t.level))
            draw_text(f"Selecionada: {TOWER_TYPES[t.kind]['name']} Nv.{t.level}",850,608,t.color,SMALL)
            draw_text(f"Melhoria: {fmt_bytes(cost)}",850,629,WHITE,SMALL)
        else:
            draw_text("Clique numa torre para",850,608,MUTED,SMALL)
            draw_text("ver detalhes e melhorá-la.",850,628,MUTED,SMALL)
        if self.message_time > 0:
            text = FONT.render(self.message, True, WHITE)
            box = pygame.Rect(WIDTH//2-text.get_width()//2-14, 82, text.get_width()+28, 32)
            pygame.draw.rect(screen,(23,43,61),box,border_radius=8)
            pygame.draw.rect(screen,BORDER,box,1,border_radius=8)
            screen.blit(text,(box.x+14,box.y+6))
        if self.completed or self.lost:
            veil=pygame.Surface((WIDTH,HEIGHT),pygame.SRCALPHA); veil.fill((2,7,15,205)); screen.blit(veil,(0,0))
            title="SISTEMA PROTEGIDO!" if self.completed else "NÚCLEO COMPROMETIDO"
            col=MINT if self.completed else RED
            txt=BIG.render(title,True,col); screen.blit(txt,(WIDTH//2-txt.get_width()//2,260))
            sub=FONT.render("ENTER para jogar novamente  |  ESC para sair",True,WHITE)
            screen.blit(sub,(WIDTH//2-sub.get_width()//2,315))

    def draw(self):
        screen.fill(BG)
        self.draw_map()
        self.draw_ui()
        if self.tree_open:
            self.draw_tree()

game = Game()
running = True
while running:
    dt = min(clock.tick(60)/1000, .04)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game.tree_open:
                    game.tree_open = False
                else:
                    running = False
            elif game.completed or game.lost:
                if event.key == pygame.K_RETURN:
                    game = Game()
            elif game.tree_open:
                if event.key in (pygame.K_1,pygame.K_2,pygame.K_3):
                    game.buy_skill(event.key-pygame.K_1)
                elif event.key == pygame.K_t:
                    game.tree_open=False
            else:
                if event.key == pygame.K_SPACE:
                    game.start_wave()
                elif event.key == pygame.K_q:
                    game.selected_kind=0
                elif event.key == pygame.K_w:
                    game.selected_kind=1
                elif event.key == pygame.K_e:
                    game.selected_kind=2
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
                for i in range(3):
                    if pygame.Rect(24+i*210,602,195,70).collidepoint(pos):
                        game.selected_kind=i
    game.update(dt)
    game.draw()
    pygame.display.flip()

pygame.quit()
sys.exit()
