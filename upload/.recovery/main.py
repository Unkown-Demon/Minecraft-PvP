from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import time
from ursina.prefabs.health_bar import HealthBar
import random

# O'yin sozlamalari
app = Ursina()
window.title = "Zor PvP Arena"
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = True

# ==============================================================================
# Kub (Voxel) klassi - Dunyo bloklari uchun
# ==============================================================================
class Voxel(Button):
    def __init__(self, position=(0,0,0), texture='grass', color=color.white):
        super().__init__(
            parent = scene,
            position = position,
            model = 'cube',
            origin_y = 0.5,
            texture = texture,
            color = color,
            highlight_color = color.lime,
            scale = 1,
            collider = 'box'
        )

# ==============================================================================
# Dunyoni yaratish (Flat World - Tekis Dunyo)
# ==============================================================================
def generate_flat_world(size=100, height=0):
    """
    100x100 o'lchamli tekis dunyo yaratadi.
    Bu bizning asosiy PvP maydonimiz bo'ladi.
    """
    for x in range(size):
        for z in range(size):
            # Asosiy maydon (100x100)
            Voxel(position=(x, height, z), texture='grass', color=color.green)
            Voxel(position=(x, height - 1, z), texture='dirt', color=color.brown)
            Voxel(position=(x, height - 2, z), texture='dirt', color=color.brown)
            Voxel(position=(x, height - 3, z), texture='stone', color=color.gray)

# ==============================================================================
# O'yinchi (Player) klassi
# ==============================================================================
# ==============================================================================
# Dushman (Enemy) klassi
# ==============================================================================
class Enemy(Button):
    def __init__(self, position=(0, 1, 0), health=20, **kwargs):
        super().__init__(
            parent=scene,
            position=position,
            model='cube',
            origin_y=0.5,
            texture='brick',
            color=color.red,
            highlight_color=color.orange,
            scale=1,
            collider='box',
            **kwargs
        )
        self.name = "Enemy"
        self.health = health
        self.max_health = health
        self.health_bar = HealthBar(bar_color=color.red.tint(-.2), base_color=color.red.tint(.2), max_value=self.max_health, value=self.health, scale=(1, 0.1), y=1.2, parent=self)

    def take_damage(self, damage):
        self.health -= damage
        self.health_bar.value = self.health
        print(f"{self.name} took {damage} damage. Health: {self.health}")
        if self.health <= 0:
            destroy(self)
            print(f"{self.name} defeated!")

# ==============================================================================
# Qurol-yarog'lar va Sehrlar tizimi
# ==============================================================================

class Enchantment:
    def __init__(self, name, effect_type, value):
        self.name = name
        self.effect_type = effect_type # 'damage', 'speed', 'health', 'lifesteal', 'healer'
        self.value = value

class Item(Entity):
    def __init__(self, name, model, texture, **kwargs):
        super().__init__(
            parent=scene,
            model=model,
            texture=texture,
            collider='box',
            **kwargs
        )
        self.name = name

class Weapon(Item):
    def __init__(self, name, damage, attack_speed, model='cube', texture='sword', enchantments=None, **kwargs):
        super().__init__(name, model, texture, **kwargs)
        self.base_damage = damage
        self.base_attack_speed = attack_speed
        self.enchantments = enchantments if enchantments is not None else []
        self.calculate_stats()

    def calculate_stats(self):
        self.damage = self.base_damage
        self.attack_speed = self.base_attack_speed
        self.lifesteal = 0
        self.healer_power = 0
        
        for ench in self.enchantments:
            if ench.effect_type == 'damage':
                self.damage += ench.value
            elif ench.effect_type == 'speed':
                self.attack_speed += ench.value
            elif ench.effect_type == 'lifesteal':
                self.lifesteal += ench.value
            elif ench.effect_type == 'healer':
                self.healer_power += ench.value

# 100+ qobiliyat/sehrlar uchun misollar
ENCHANTMENTS = [
    Enchantment("Sharpness I", "damage", 1.5),
    Enchantment("Sharpness II", "damage", 3.0),
    Enchantment("Swiftness I", "speed", 1.0),
    Enchantment("Vampirism I", "lifesteal", 0.1), # 10% lifesteal
    Enchantment("Healer I", "healer", 5.0), # Har bir hujumda 5 HP tiklash
    Enchantment("Protection I", "health", 5.0), # Armor uchun
]

# Qurol-yarog'lar misollari
DIAMOND_SWORD = Weapon("Diamond Sword", 7.0, 1.6, enchantments=[ENCHANTMENTS[0]])
HEALER_SWORD = Weapon("Healer's Blade", 4.0, 1.0, enchantments=[ENCHANTMENTS[4]])

# ==============================================================================
# Dushman (Enemy) klassi
# ==============================================================================
class Enemy(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # O'yinchi xususiyatlari (keyinroq 1.9+ PvP uchun kengaytiriladi)
        self.health = 20
        self.max_health = 20
        self.current_weapon = DIAMOND_SWORD # Boshlang'ich qurol
        self.attack_damage = self.current_weapon.damage
        self.attack_speed = self.current_weapon.attack_speed # 1.9+ ga o'xshash
        self.lifesteal = self.current_weapon.lifesteal
        self.healer_power = self.current_weapon.healer_power
        self.last_attack_time = time.time()
        self.attack_cooldown = 1 / self.attack_speed
        self.cooldown_bar.max_value = self.attack_cooldown # Cooldown bar max qiymatini yangilash
        
        # Hujum Cooldown UI
        self.cooldown_bar = HealthBar(
            bar_color=color.yellow, 
            base_color=color.dark_gray, 
            max_value=self.attack_cooldown, 
            value=self.attack_cooldown, 
            scale=(0.5, 0.02), 
            position=(0, -0.45), 
            parent=camera.ui
        )
        
        # Qo'l/Qurol vizuali
        self.sword = Entity(
            parent=camera.ui, 
            model='cube', 
            color=color.gray, 
            scale=(0.1, 0.5, 0.1), 
            position=(0.5, -0.3, 0.5), 
            rotation=(90, 0, 0),
            origin=(0, -0.5, 0)
        )
        self.sword.visible = False

    def update(self):
        # Cooldownni yangilash
        time_since_last_attack = time.time() - self.last_attack_time
        self.cooldown_bar.value = min(time_since_last_attack, self.attack_cooldown)
        
        # O'yinchi harakati va boshqaruvini tekshirish
        # O'yinchi harakati va boshqaruvini tekshirish
        super().update()
        
        # Hujum mexanikasi (3-bosqichda to'liq amalga oshiriladi)
        if mouse.left and time.time() - self.last_attack_time >= self.attack_cooldown:
            self.attack()
            self.last_attack_time = time.time()

    def attack(self):
        # Hujum animatsiyasi
        self.sword.visible = True
        self.sword.rotation_x = 90
        self.sword.animate_rotation_x(120, duration=.1, curve=curve.out_quad)
        invoke(lambda: self.sword.animate_rotation_x(90, duration=.1, curve=curve.in_quad), delay=.1)
        invoke(lambda: setattr(self.sword, 'visible', False), delay=.2)

        # Hujum hisobi (keyinroq dushmanlar uchun)
        hit_info = raycast(self.world_position + Vec3(0, 1.5, 0), self.forward, distance=5, ignore=[self, self.sword])
        if hit_info.hit:
            target = hit_info.entity
            damage_dealt = self.attack_damage * random.uniform(0.9, 1.1) # Kichik tasodifiy zarba
            
            if hasattr(target, 'take_damage'):
                target.take_damage(damage_dealt)
            
            # Lifesteal mexanikasi
            if self.lifesteal > 0:
                heal_amount = damage_dealt * self.lifesteal
                self.health = min(self.max_health, self.health + heal_amount)
                print(f"Lifesteal: Healed {heal_amount:.2f} HP.")

            # Healer mexanikasi
            if self.healer_power > 0:
                self.health = min(self.max_health, self.health + self.healer_power)
                print(f"Healer: Healed {self.healer_power:.2f} HP.")

            print(f"Hit: {target.name} for {damage_dealt:.2f} damage.")

# ==============================================================================
# O'yinni ishga tushirish
# ==============================================================================
generate_flat_world(size=100)
player = PvPPlayer(model='cube', color=color.blue, origin_y=-.5, speed=6)
player.current_weapon = HEALER_SWORD # Test uchun Healer Sword berish
player.attack_damage = player.current_weapon.damage
player.attack_speed = player.current_weapon.attack_speed
player.lifesteal = player.current_weapon.lifesteal
player.healer_power = player.current_weapon.healer_power
player.position = (50, 1, 50) # Maydon markaziga joylashtirish

# Dushman qo'shish (test uchun)
enemy1 = Enemy(position=(55, 1, 55))
enemy2 = Enemy(position=(45, 1, 45))

# Kamera sozlamalari
camera.clip_plane_far = 200 # Ko'rish masofasini oshirish

# Chiqish tugmasi
def input(key):
    if key == 'escape':
        quit()

app.run()
