from ursina import *
import socket
import threading
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
# Boshqa O'yinchilar (Network Player) klassi
# ==============================================================================
class NetworkPlayer(Entity):
    def __init__(self, player_id, position, **kwargs):
        super().__init__(
            parent=scene,
            model='cube',
            color=color.blue.tint(-0.5),
            origin_y=-.5,
            position=position,
            collider='box',
            **kwargs
        )
        self.player_id = player_id
        self.name = f"Player_{player_id}"
        self.health = 20
        self.max_health = 20
        self.health_bar = HealthBar(bar_color=color.green.tint(-.2), base_color=color.green.tint(.2), max_value=self.max_health, value=self.health, scale=(1, 0.1), y=1.2, parent=self)

    def update_position(self, x, y, z):
        self.position = (x, y, z)
        
    def update_rotation(self, rot_y, rot_x):
        self.rotation_y = rot_y
        
    def update_health(self, health):
        self.health = health
        self.health_bar.value = health
        if self.health <= 0:
            self.health_bar.visible = False
            self.visible = False
            print(f"Player {self.player_id} o'ldi.")
        else:
            self.health_bar.visible = True
            self.visible = True

# ==============================================================================
# Qurol-yarog'lar va Sehrlar tizimi
# ==============================================================================

class Enchantment:
    def __init__(self, name, effect_type, value):
        self.name = name
        self.effect_type = effect_type # 'damage', 'speed', 'health', 'lifesteal', 'healer', 'defense', 'movement_speed', 'passive_heal', 'max_health', 'critical_chance'
        self.value = value

class Item:
    def __init__(self, name):
        self.name = name

class Weapon(Item):
    def __init__(self, name, damage, attack_speed, enchantments=None, color=color.white):
        super().__init__(name)
        self.base_damage = damage
        self.base_attack_speed = attack_speed
        self.enchantments = enchantments if enchantments is not None else []
        self.color = color
        self.calculate_stats()

    def calculate_stats(self):
        self.damage = self.base_damage
        self.attack_speed = self.base_attack_speed
        self.lifesteal = 0.0
        self.healer_power = 0.0
        
        for ench in self.enchantments:
            if ench.effect_type == 'damage':
                self.damage += ench.value
            elif ench.effect_type == 'speed':
                self.attack_speed += ench.value
            elif ench.effect_type == 'lifesteal':
                self.lifesteal += ench.value
            elif ench.effect_type == 'healer':
                self.healer_power += ench.value

# ==============================================================================
# 100+ Qobiliyat/Sehrlar Ro'yxati
# ==============================================================================
ENCHANTMENTS = [
    # Damage (Zarar)
    Enchantment("Sharpness I", "damage", 1.5),
    Enchantment("Sharpness II", "damage", 3.0),
    Enchantment("Sharpness III", "damage", 4.5),
    Enchantment("Sharpness IV", "damage", 6.0),
    Enchantment("Sharpness V", "damage", 7.5),
    Enchantment("Smite I", "damage", 2.0),
    Enchantment("Bane of Arthropods I", "damage", 2.0),
    
    # Speed (Tezlik)
    Enchantment("Swiftness I", "speed", 0.1),
    Enchantment("Agility I", "movement_speed", 0.1),
    
    # Lifesteal/Healer (Sog'liqni tiklash)
    Enchantment("Vampirism I", "lifesteal", 0.1),
    Enchantment("Healer I", "healer", 1.0),
    Enchantment("Regeneration I", "passive_heal", 0.5),
    
    # Defense (Himoya) - Armor uchun
    Enchantment("Protection I", "defense", 0.05),
    Enchantment("Protection II", "defense", 0.10),
    Enchantment("Resilience I", "defense", 0.1),
    Enchantment("Vigor I", "max_health", 2.0), # Maksimal sog'liqni oshirish
    Enchantment("Rage I", "critical_chance", 0.1), # Kritik zarba ehtimoli
    
    # Mace/Elytra/Talisman uchun maxsus sehrlar
    Enchantment("Smash I", "mace_smash_bonus", 0.5), # Mace: Tushish balandligiga qarab bonus zarar
    Enchantment("Gliding I", "elytra_speed_bonus", 0.2), # Elytra: Uchish tezligi bonusi
    Enchantment("Talismanic Power I", "talisman_power", 0.1), # Talisman: Barcha statlarga kichik bonus
    
    # Qo'shimcha 100+ sehrlar uchun joy (Vaqtinchalik joy)
    Enchantment("Unbreaking I", "durability", 0.1),
    Enchantment("Thorns I", "thorns_damage", 1.0),
    Enchantment("Fire Aspect I", "damage_over_time", 1.0),
    Enchantment("Knockback I", "knockback", 1.0),
    Enchantment("Poison I", "poison_effect", 1.0),
    Enchantment("Blindness I", "blindness_effect", 1.0),
    Enchantment("Feather Falling I", "fall_damage", 0.1),
    Enchantment("Aqua Affinity", "water_breathing", 1),
    Enchantment("Respiration I", "water_breathing_time", 1),
    Enchantment("Depth Strider I", "water_movement", 0.1),
    Enchantment("Curse of Vanishing", "curse", 1),
    Enchantment("Curse of Binding", "curse", 1),
    Enchantment("Mending", "repair", 1),
    Enchantment("Soul Speed I", "soul_speed", 0.1),
    Enchantment("Piercing I", "piercing", 1),
    Enchantment("Multishot", "multishot", 1),
    Enchantment("Quick Charge I", "quick_charge", 0.1),
    Enchantment("Infinity", "infinity", 1),
    Enchantment("Riptide I", "riptide", 1),
    Enchantment("Loyalty I", "loyalty", 1),
    Enchantment("Impaling I", "impaling", 1),
    Enchantment("Channeling", "channeling", 1),
    Enchantment("Efficiency I", "mining_speed", 0.1),
    Enchantment("Silk Touch", "silk_touch", 1),
    Enchantment("Fortune I", "fortune", 1),
    Enchantment("Lure I", "lure", 1),
    Enchantment("Luck of the Sea I", "luck_of_the_sea", 1),
    Enchantment("Frost Walker I", "frost_walker", 1),
    Enchantment("Silence", "silence", 1),
    # 100+ ga yetkazish uchun qo'shimcha sehrlar (kodni qisqartirish uchun qolganlari o'tkazib yuborildi)
]

# ==============================================================================
# Qurol-yarog'lar Ro'yxati
# ==============================================================================
DIAMOND_SWORD = Weapon("Diamond Sword", 5.0, 1.6, enchantments=[ENCHANTMENTS[0], ENCHANTMENTS[7]], color=color.cyan)
HEALER_SWORD = Weapon("Healer's Blade", 3.0, 1.8, enchantments=[ENCHANTMENTS[10], ENCHANTMENTS[11]], color=color.pink)
AXE_OF_DESTRUCTION = Weapon("Axe of Destruction", 8.0, 0.9, enchantments=[ENCHANTMENTS[4], ENCHANTMENTS[22]], color=color.red)
NETHERITE_SWORD = Weapon("Netherite Sword", 6.0, 1.6, enchantments=[ENCHANTMENTS[4], ENCHANTMENTS[13], ENCHANTMENTS[16]], color=color.black)
MACE_OF_ANARCHY = Weapon("Mace of Anarchy", 4.0, 0.6, enchantments=[ENCHANTMENTS[2], ENCHANTMENTS[20]], color=color.gold) # Mace: past attack speed, high damage potential
ELYTRA_ITEM = Weapon("Elytra", 0.0, 0.0, enchantments=[ENCHANTMENTS[14], ENCHANTMENTS[15]], color=color.dark_gray) # Elytra: Defense and movement
TALISMAN_OF_POWER = Weapon("Talisman of Power", 0.0, 0.0, enchantments=[ENCHANTMENTS[16], ENCHANTMENTS[17]], color=color.orange) # Talisman: Max Health and Critical Chance

# ==============================================================================
# O'yinchi (PvPPlayer) klassi
# ==============================================================================
class PvPPlayer(FirstPersonController):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # O'yinchi xususiyatlari
        self.health = 20.0
        self.max_health = 20.0
        self.critical_chance = 0.05 # Boshlang'ich 5% kritik zarba ehtimoli
        self.critical_damage_multiplier = 1.5 # Kritik zarba koeffitsienti
        
        # Tana/Armor sozlamalari
        self.armor_defense = 0.0 # Armor orqali qo'shilgan himoya
        self.armor_health_bonus = 0 # Armor orqali qo'shilgan sog'liq
        self.max_health += self.armor_health_bonus # Maksimal sog'liqni yangilash
        
        self.lifesteal = 0.0
        self.healer_power = 0.0
        self.defense = 0.0 # Zarar kamaytirish foizi (0.0 dan 1.0 gacha)
        self.movement_speed_bonus = 0.0 # Harakat tezligi bonusi
        self.passive_heal_rate = 0.0 # Passiv davolash tezligi (HP/sekund)
        self.last_passive_heal = time.time()
        self.last_attack_time = time.time()
        
        # Maxsus qobiliyat sozlamalari
        self.dash_cooldown = 5.0
        self.last_dash_time = time.time()
        
        # Inventar sozlamalari
        # Slot 0-8: Hotbar
        # Slot 9: Armor (Vaqtincha)
        # Slot 10: Elytra (Vaqtincha)
        # Slot 11: Talisman (Vaqtincha)
        self.inventory = [DIAMOND_SWORD, MACE_OF_ANARCHY, ELYTRA_ITEM, TALISMAN_OF_POWER, None, None, None, None, None]
        self.inventory.append(Weapon("Diamond Chestplate", 0, 0, enchantments=[ENCHANTMENTS[13], ENCHANTMENTS[16]], color=color.blue)) # Slot 9: Armor
        self.inventory.append(ELYTRA_ITEM) # Slot 10: Elytra
        self.inventory.append(TALISMAN_OF_POWER) # Slot 11: Talisman
        
        self.current_slot = 0
        self.update_weapon_from_inventory()
        self.setup_hotbar_ui()
        
        self.attack_cooldown = 1 / self.attack_speed
        
        # Hujum Cooldown UI
        self.cooldown_bar = HealthBar(
            bar_color=color.yellow, 
            base_color=color.dark_gray, 
            max_value=self.attack_cooldown, 
            value=self.attack_cooldown, 
            scale=(0.3, 0.02), 
            position=(-0.15, -0.45), 
            parent=camera.ui
        )
        
        # Sog'liq paneli
        self.health_bar = HealthBar(
            bar_color=color.red, 
            base_color=color.dark_red, 
            max_value=self.max_health, 
            value=self.health, 
            scale=(0.3, 0.02), 
            position=(0.15, -0.45), 
            parent=camera.ui
        )
        
        # Qurol modeli (test uchun)
        self.sword = Entity(
            parent=camera.ui, 
            model='cube', 
            scale=(0.05, 0.2, 0.05), 
            color=self.current_weapon.color,
            position=(0.5, -0.3, 0.5), 
            rotation=(90, 0, 0),
            origin=(0, -0.5, 0)
        )
        self.sword.visible = False
        
        # Inventar UI elementlari
        self.hotbar_slots = []
        
        # Tarmoq sozlamalari
        self.client_socket = None
        self.player_id = None
        self.other_players = {} # {id: NetworkPlayer}
        self.is_connected = False
        self.last_pos_update = time.time()
        self.last_rot_update = time.time(        self.server_host = '127.0.0.1' # Lokal test uchun
        self.server_port = 5555
        
        # Chat va Command sozlamalari
        self.chat_input = InputField(y=-.3, scale=.5, parent=camera.ui, active=False)
        self.chat_input.input_field.text_field.font_size = 20
        self.chat_input.input_field.text_field.color = color.white
        self.chat_input.input_field.text_field.background = True
        self.chat_input.input_field.text_field.background_color = color.black33
        self.chat_input.input_field.text_field.y = -0.4
        self.chat_input.input_field.text_field.x = -0.4
        self.chat_input.input_field.text_field.scale = 0.5
        self.chat_input.input_field.text_field.visible = False
        self.chat_input.input_field.text_field.on_submit = self.send_chat_or_command
        
        self.chat_log = Text(text="", y=0.45, x=-0.8, scale=1.5, parent=camera.ui)
        self.chat_log.line_height = 1.5
        self.chat_log.max_lines = 10
        self.chat_log.visible = True
        
        self.connect_to_server()amalari
        self.chat_input = InputField(y=-.3, scale=.5, parent=camera.ui, active=False)
        self.chat_input.input_field.text_field.font_size = 20
        self.chat_input.input_field.text_field.color = color.white
        self.chat_input.input_field.text_field.background = True
        self.chat_input.input_field.text_field.background_color = color.black33
        self.chat_input.input_field.text_field.y = -0.4
        self.chat_input.input_field.text_field.x = -0.4
        self.chat_input.input_field.text_field.scale = 0.5
        self.chat_input.input_field.text_field.visible = False
        self.chat_input.input_field.text_field.on_submit = self.send_chat_or_command
        
        self.chat_log = Text(text="", y=0.45, x=-0.8, scale=1.5, parent=camera.ui)
        self.chat_log.line_height = 1.5
        self.chat_log.max_lines = 10
        self.chat_log.visible = True
        
        self.connect_to_server()

    def update(self):
        # Inventar slotini yangilash
        self.update_hotbar_selection()
        
        # Cooldownni yangilash
        time_since_last_attack = time.time() - self.last_attack_time
        self.cooldown_bar.value = min(time_since_last_attack, self.attack_cooldown)
        
        # Maxsus qobiliyatni ishlatish uchun Cooldownni tekshirish (masalan, Dash)
        if held_keys['q'] and time.time() - self.last_dash_time > self.dash_cooldown:
            self.dash()
            self.last_dash_time = time.time()
        
        # Passiv davolash (Regeneration)
        if self.passive_heal_rate > 0 and time.time() - self.last_passive_heal >= 1.0:
            self.health = min(self.max_health, self.health + self.passive_heal_rate)
            self.health_bar.value = self.health
            self.last_passive_heal = time.time()
        
        # O'yinchi harakati va boshqaruvini tekshirish
        super().update()
        
        # Tarmoq yangilanishlari
        if self.is_connected:
            if time.time() - self.last_pos_update > 0.05: # 20 FPS
                self.send_position()
                self.last_pos_update = time.time()
            
            if time.time() - self.last_rot_update > 0.1: # 10 FPS
                self.send_rotation()
                self.last_rot_update = time.time()

        # Hujum mexanikasi
        if mouse.left and time.time() - self.last_attack_time >= self.attack_cooldown:
            self.attack()
            self.last_attack_time = time.time()
            
        # Inventar slotini almashtirish (1-9 tugmalari)
        for i in range(1, 10):
            if held_keys[str(i)]:
                self.switch_weapon(i - 1)
                break
                
        # Chatni ochish
        if held_keys['t'] and not self.chat_input.active:
            self.chat_input.active = True
            self.chat_input.input_field.text_field.visible = True
            self.chat_input.input_field.text_field.text = ""
            
        if held_keys['escape'] and self.chat_input.active:
            self.chat_input.active = False
            self.chat_input.input_field.text_field.visible = False
                
        # Chatni ochish
        if held_keys['t'] and not self.chat_input.active:
            self.chat_input.active = True
            self.chat_input.input_field.text_field.visible = True
            self.chat_input.input_field.text_field.text = ""
            
        if held_keys['escape'] and self.chat_input.active:
            self.chat_input.active = False
            self.chat_input.input_field.text_field.visible = False

    def attack(self):
        # Hujum animatsiyasi
        self.sword.visible = True
        self.sword.rotation_x = 90
        self.sword.animate_rotation_x(120, duration=.1, curve=curve.out_quad)
        invoke(lambda: self.sword.animate_rotation_x(90, duration=.1, curve=curve.in_quad), delay=.1)
        invoke(lambda: setattr(self.sword, 'visible', False), delay=.2)
        # Hujum hisobi
        hit_info = raycast(self.world_position + Vec3(0, 1.5, 0), self.forward, distance=5, ignore=[self, self.sword])
        if hit_info.hit:
            target = hit_info.entity
            base_damage = self.attack_damage * random.uniform(0.9, 1.1) # Kichik tasodifiy zarba
            damage_dealt = base_damage
            
            # Mace PvP mexanikasi (Tushish balandligiga qarab bonus zarar)
            if self.current_weapon and self.current_weapon.name.startswith("Mace"):
                fall_damage_bonus = max(0, self.y - target.y) * 2.0 # Oddiy hisob
                
                # Mace sehrini qo'llash
                mace_smash_bonus = 0.0
                for ench in self.current_weapon.enchantments:
                    if ench.effect_type == 'mace_smash_bonus':
                        mace_smash_bonus += ench.value
                        
                damage_dealt += fall_damage_bonus * (1 + mace_smash_bonus)
                print(f"Mace Smash Bonus: {fall_damage_bonus * (1 + mace_smash_bonus):.2f} damage.")
            
            # Kritik zarba hisobi
            if random.random() < self.critical_chance:
                damage_dealt *= self.critical_damage_multiplier
                print("CRITICAL HIT!")us = max(0, self.y - target.y) * 2.0 # Oddiy hisob
                
                # Mace sehrini qo'llash
                mace_smash_bonus = 0.0
                for ench in self.current_weapon.enchantments:
                    if ench.effect_type == 'mace_smash_bonus':
                        mace_smash_bonus += ench.value
                        
                damage_dealt += fall_damage_bonus * (1 + mace_smash_bonus)
                print(f"Mace Smash Bonus: {fall_damage_bonus * (1 + mace_smash_bonus):.2f} damage.")
            
            # Kritik zarba hisobi
            if random.random() < self.critical_chance:
                damage_dealt *= self.critical_damage_multiplier
                print("CRITICAL HIT!")
            
            if hasattr(target, 'take_damage'):
                if isinstance(target, NetworkPlayer):
                    # Boshqa o'yinchiga zarar yetkazishni serverga yuborish
                    self.send_damage(target.player_id, damage_dealt)
                # Dushman/NPC uchun lokal zarar hisobi
                elif hasattr(target, 'defense'):
                    target.take_damage(damage_dealt)
            
            # Lifesteal mexanikasi
            if self.lifesteal > 0:
                heal_amount = damage_dealt * self.lifesteal
                self.health = min(self.max_health, self.health + heal_amount)
                self.health_bar.value = self.health

            # Healer mexanikasi
            if self.healer_power > 0:
                self.health = min(self.max_health, self.health + self.healer_power)
                self.health_bar.value = self.health

            print(f"Hit: {target.name} for {damage_dealt:.2f} damage.")

    def connect_to_server(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.server_host, self.server_port))
            self.client_socket.setblocking(False) # Bloklanmaydigan rejim
            self.is_connected = True
            print("Serverga ulanish muvaffaqiyatli.")
            
            # Ma'lumotlarni qabul qilish uchun alohida thread
            threading.Thread(target=self.receive_data, daemon=True).start()
            
        except ConnectionRefusedError:
            print("Serverga ulanib bo'lmadi. Server ishga tushirilganligiga ishonch hosil qiling.")
        except Exception as e:
            print(f"Ulanish xatosi: {e}")

    def receive_data(self):
        buffer = ""
        while self.is_connected:
            try:
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                buffer += data
                
                while '\n' in buffer:
                    message, buffer = buffer.split('\n', 1)
                    self.handle_server_message(message)
                    
            except BlockingIOError:
                time.sleep(0.01)
            except ConnectionResetError:
                print("Server ulanishni uzdi.")
                self.is_connected = False
                break
            except Exception as e:
                print(f"Ma'lumot qabul qilish xatosi: {e}")
                self.is_connected = False
                break

    def send_chat_or_command(self):
        text = self.chat_input.text
        self.chat_input.text = ""
        self.chat_input.active = False
        self.chat_input.input_field.text_field.visible = False
        
        if text.startswith('/'):
            self.handle_command(text)
        elif text:
            self.send_message(f"CHAT:{self.name}: {text}")
            self.add_chat_message(f"<{self.name}> {text}")

    def handle_command(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == '/help':
            self.add_chat_message("--- Admin Buyruqlari ---")
            self.add_chat_message("/help - Buyruqlar ro'yxati")
            self.add_chat_message("/gamemode <0|1> - O'yin rejimini o'zgartirish (0: Survival, 1: Creative)")
            self.add_chat_message("/heal - Sog'liqni to'ldirish")
            self.add_chat_message("/fly - Uchish rejimini yoqish/o'chirish")
            self.add_chat_message("/give <item> - Inventarga buyum berish (Vaqtincha ishlamaydi)")
            self.add_chat_message("/tp <x> <y> <z> - Koordinatalarga teleportatsiya")
            self.add_chat_message("--- 50+ buyruq uchun asos yaratildi ---")
            
        elif cmd == '/gamemode':
            if not args:
                self.add_chat_message("Xato: /gamemode <0|1> ishlatilishi kerak.")
                return
            
            mode = args[0]
            if mode == '1':
                self.add_chat_message("Creative Mode yoqildi.")
                self.speed = 10 # Tezlikni oshirish
                self.gravity = 0 # Uchish
                self.collider = 'box' # Bloklar orqali o'tishni o'chirish
            elif mode == '0':
                self.add_chat_message("Survival Mode yoqildi.")
                self.speed = 6
                self.gravity = 1
                self.collider = 'box'
            else:
                self.add_chat_message("Xato: Noto'g'ri rejim. Faqat 0 yoki 1 kiriting.")
                
        elif cmd == '/heal':
            self.health = self.max_health
            self.health_bar.value = self.health
            self.add_chat_message("Sog'liq to'ldirildi.")
            
        elif cmd == '/fly':
            if self.gravity == 1:
                self.gravity = 0
                self.add_chat_message("Uchish rejimi yoqildi.")
            else:
                self.gravity = 1
                self.add_chat_message("Uchish rejimi o'chirildi.")
                
        elif cmd == '/tp':
            if len(args) != 3:
                self.add_chat_message("Xato: /tp <x> <y> <z> ishlatilishi kerak.")
                return
            try:
                x, y, z = float(args[0]), float(args[1]), float(args[2])
                self.position = (x, y, z)
                self.add_chat_message(f"Teleportatsiya: {x}, {y}, {z}")
            except ValueError:
                self.add_chat_message("Xato: Koordinatalar noto'g'ri formatda.")
                
        else:
            self.add_chat_message(f"Noma'lum buyruq: {cmd}")

    def add_chat_message(self, message):
        # Yangi xabarni chat logiga qo'shish
        current_lines = self.chat_log.text.split('\n')
        if len(current_lines) >= self.chat_log.max_lines:
            current_lines.pop(0) # Eng eski xabarni o'chirish
        
        current_lines.append(message)
        self.chat_log.text = '\n'.join(current_lines)

    def send_chat_or_command(self):
        text = self.chat_input.text
        self.chat_input.text = ""
        self.chat_input.active = False
        self.chat_input.input_field.text_field.visible = False
        
        if text.startswith('/'):
            self.handle_command(text)
        elif text:
            self.send_message(f"CHAT:{self.name}: {text}")
            self.add_chat_message(f"<{self.name}> {text}")

    def handle_command(self, command):
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]
        
        if cmd == '/help':
            self.add_chat_message("--- Admin Buyruqlari ---")
            self.add_chat_message("/help - Buyruqlar ro'yxati")
            self.add_chat_message("/gamemode <0|1> - O'yin rejimini o'zgartirish (0: Survival, 1: Creative)")
            self.add_chat_message("/heal - Sog'liqni to'ldirish")
            self.add_chat_message("/fly - Uchish rejimini yoqish/o'chirish")
            self.add_chat_message("/give <item> - Inventarga buyum berish (Vaqtincha ishlamaydi)")
            self.add_chat_message("/tp <x> <y> <z> - Koordinatalarga teleportatsiya")
            self.add_chat_message("--- 50+ buyruq uchun asos yaratildi ---")
            
        elif cmd == '/gamemode':
            if not args:
                self.add_chat_message("Xato: /gamemode <0|1> ishlatilishi kerak.")
                return
            
            mode = args[0]
            if mode == '1':
                self.add_chat_message("Creative Mode yoqildi.")
                self.speed = 10 # Tezlikni oshirish
                self.gravity = 0 # Uchish
                self.collider = 'box' # Bloklar orqali o'tishni o'chirish
            elif mode == '0':
                self.add_chat_message("Survival Mode yoqildi.")
                self.speed = 6
                self.gravity = 1
                self.collider = 'box'
            else:
                self.add_chat_message("Xato: Noto'g'ri rejim. Faqat 0 yoki 1 kiriting.")
                
        elif cmd == '/heal':
            self.health = self.max_health
            self.health_bar.value = self.health
            self.add_chat_message("Sog'liq to'ldirildi.")
            
        elif cmd == '/fly':
            if self.gravity == 1:
                self.gravity = 0
                self.add_chat_message("Uchish rejimi yoqildi.")
            else:
                self.gravity = 1
                self.add_chat_message("Uchish rejimi o'chirildi.")
                
        elif cmd == '/tp':
            if len(args) != 3:
                self.add_chat_message("Xato: /tp <x> <y> <z> ishlatilishi kerak.")
                return
            try:
                x, y, z = float(args[0]), float(args[1]), float(args[2])
                self.position = (x, y, z)
                self.add_chat_message(f"Teleportatsiya: {x}, {y}, {z}")
            except ValueError:
                self.add_chat_message("Xato: Koordinatalar noto'g'ri formatda.")
                
        else:
            self.add_chat_message(f"Noma'lum buyruq: {cmd}")

    def add_chat_message(self, message):
        # Yangi xabarni chat logiga qo'shish
        current_lines = self.chat_log.text.split('\n')
        if len(current_lines) >= self.chat_log.max_lines:
            current_lines.pop(0) # Eng eski xabarni o'chirish
        
        current_lines.append(message)
        self.chat_log.text = '\n'.join(current_lines)

    def handle_server_message(self, message):
        if message.startswith("ID:"):
            self.player_id = int(message.split(':')[1])
            print(f"Mening ID: {self.player_id}")
            
        elif message.startswith("CHAT:"):
            try:
                self.add_chat_message(message[5:]) # "CHAT:" dan keyingi qismini olish
            except:
                pass
                
        elif message.startswith("CHAT:"):
            try:
                self.add_chat_message(message[5:]) # "CHAT:" dan keyingi qismini olish
            except:
                pass
                
        elif message.startswith("NEW_PLAYER:"):
            try:
                _, player_id, x, y, z = message.split(':')
                player_id = int(player_id)
                x, y, z = float(x), float(y), float(z)
                
                if player_id != self.player_id and player_id not in self.other_players:
                    new_player = NetworkPlayer(player_id, (x, y, z))
                    self.other_players[player_id] = new_player
                    print(f"Yangi o'yinchi qo'shildi: {player_id}")
            except:
                print(f"NEW_PLAYER xatosi: {message}")
                
        elif message.startswith("MOVE:"):
            try:
                _, player_id, x, y, z = message.split(':')
                player_id = int(player_id)
                x, y, z = float(x), float(y), float(z)
                
                if player_id in self.other_players:
                    self.other_players[player_id].update_position(x, y, z)
            except:
                pass
                
        elif message.startswith("ROT:"):
            try:
                _, player_id, rot_y, rot_x = message.split(':')
                player_id = int(player_id)
                rot_y, rot_x = float(rot_y), float(rot_x)
                
                if player_id in self.other_players:
                    self.other_players[player_id].update_rotation(rot_y, rot_x)
            except:
                pass
                
        elif message.startswith("HEALTH:"):
            try:
                _, player_id, health = message.split(':')
                player_id = int(player_id)
                health = float(health)
                
                if player_id in self.other_players:
                    self.other_players[player_id].update_health(health)
            except:
                pass
                
        elif message.startswith("RESPAWN:"):
            try:
                _, player_id, x, y, z = message.split(':')
                player_id = int(player_id)
                x, y, z = float(x), float(y), float(z)
                
                if player_id in self.other_players:
                    self.other_players[player_id].update_position(x, y, z)
                    self.other_players[player_id].update_health(20.0) # Respawn sog'lig'i
                    print(f"Player {player_id} respawn bo'ldi.")
            except:
                pass
                
        elif message.startswith("DISCONNECT:"):
            try:
                player_id = int(message.split(':')[1])
                if player_id in self.other_players:
                    destroy(self.other_players[player_id])
                    del self.other_players[player_id]
                    print(f"O'yinchi uzildi: {player_id}")
            except:
                pass
                
        elif message == "SERVER_FULL":
            print("Server to'la. Keyinroq urinib ko'ring.")
            self.is_connected = False
            self.client_socket.close()

    def send_message(self, message):
        if self.is_connected:
            try:
                self.client_socket.sendall((message + '\n').encode('utf-8'))
            except Exception as e:
                print(f"Xabar yuborish xatosi: {e}")
                self.is_connected = False

    def send_position(self):
        pos = self.position
        self.send_message(f"POS:{pos[0]:.2f}:{pos[1]:.2f}:{pos[2]:.2f}")
        
    def send_rotation(self):
        rot_y = self.rotation_y
        rot_x = camera.rotation_x
        self.send_message(f"ROT:{rot_y:.2f}:{rot_x:.2f}")

    def dash(self):
        """O'yinchi oldinga qisqa masofaga tez harakatlanadi."""
        dash_distance = 3.0
        dash_duration = 0.1
        
        start_pos = self.position
        forward_vector = self.forward
        target_pos = start_pos + forward_vector * dash_distance
        
        self.animate_position(target_pos, duration=dash_duration, curve=curve.linear)
        self.send_position()

    def update_weapon_from_inventory(self):
        """Inventardagi tanlangan qurolni o'yinchiga qo'llash."""
        new_weapon = self.inventory[self.current_slot]
        
        # Qurol effektlarini yangilash
        if new_weapon and isinstance(new_weapon, Weapon):
            self.current_weapon = new_weapon
            self.attack_damage = self.current_weapon.damage
            self.attack_speed = self.current_weapon.attack_speed
            self.lifesteal = self.current_weapon.lifesteal
            self.healer_power = self.current_weapon.healer_power
            self.attack_cooldown = 1 / self.attack_speed
            self.cooldown_bar.max_value = self.attack_cooldown
            
            # Sehr effektlarini qo'llash
            self.defense = 0.0
            self.movement_speed_bonus = 0.0
            self.passive_heal_rate = 0.0
            self.critical_chance = 0.05 # Boshlang'ich qiymat
            self.speed = 6.0 # Boshlang'ich tezlik
            
            for ench in self.current_weapon.enchantments:
                if ench.effect_type == 'defense':
                    self.defense += ench.value
                elif ench.effect_type == 'movement_speed':
                    self.movement_speed_bonus += ench.value
                elif ench.effect_type == 'passive_heal':
                    self.passive_heal_rate += ench.value
                elif ench.effect_type == 'critical_chance':
                    self.critical_chance += ench.value
            
            self.speed += self.movement_speed_bonus # Harakat tezligini yangilash
            self.sword.color = self.current_weapon.color
            
        else:
            # Qurol yo'q bo'lsa
            self.current_weapon = None
            self.attack_damage = 1.0
            self.attack_speed = 4.0
            self.lifesteal = 0.0
            self.healer_power = 0.0
            self.attack_cooldown = 1 / self.attack_speed
            self.cooldown_bar.max_value = self.attack_cooldown
            self.defense = 0.0
            self.movement_speed_bonus = 0.0
            self.passive_heal_rate = 0.0
            self.critical_chance = 0.05
            self.speed = 6.0
            self.sword.color = color.gray
            
        self.apply_armor_effects() # Armor effektlarini qo'llash

    def apply_item_effects(self):
        """Armor, Elytra va Talisman effektlarini o'yinchiga qo'llash."""
        self.armor_defense = 0.0
        self.armor_health_bonus = 0
        self.elytra_speed_bonus = 0.0
        self.talisman_power = 0.0
        
        # Armor (Slot 9)
        armor = self.inventory[9]
        if armor and isinstance(armor, Weapon):
            for ench in armor.enchantments:
                if ench.effect_type == 'defense':
                    self.armor_defense += ench.value
                elif ench.effect_type == 'max_health':
                    self.armor_health_bonus += ench.value
                    
        # Elytra (Slot 10)
        elytra = self.inventory[10]
        if elytra and isinstance(elytra, Weapon):
            for ench in elytra.enchantments:
                if ench.effect_type == 'elytra_speed_bonus':
                    self.elytra_speed_bonus += ench.value
                    
        # Talisman (Slot 11)
        talisman = self.inventory[11]
        if talisman and isinstance(talisman, Weapon):
            for ench in talisman.enchantments:
                if ench.effect_type == 'talisman_power':
                    self.talisman_power += ench.value
                    
        # Umumiy statlarga qo'shish
        self.defense += self.armor_defense
        self.max_health = 20 + self.armor_health_bonus
        self.health = min(self.health, self.max_health)
        self.health_bar.max_value = self.max_health
        self.health_bar.value = self.health
        
        # Talisman bonusini qo'llash (misol uchun, barcha statlarga)
        self.defense += self.talisman_power * 0.1
        self.movement_speed_bonus += self.talisman_power * 0.1
        self.critical_chance += self.talisman_power * 0.05
        
        # Elytra mexanikasini keyinroq qo'shamiz
        
    def setup_hotbar_ui(self):

    def setup_hotbar_ui(self):
        """Inventar paneli (Hotbar) UI elementlarini yaratish."""
        hotbar_y = -0.4
        slot_size = 0.1
        
        for i in range(9):
            # Slot ramkasi
            slot = Entity(
                parent=camera.ui,
                model='quad',
                texture='white_cube',
                color=color.dark_gray,
                scale=(slot_size, slot_size * 1.2),
                position=(-0.45 + i * slot_size * 1.1, hotbar_y),
                z=1
            )
            self.hotbar_slots.append(slot)
            
            # Qurol belgisi (hozircha faqat rang)
            if self.inventory[i]:
                item_icon = Entity(
                    parent=slot,
                    model='quad',
                    color=self.inventory[i].color if hasattr(self.inventory[i], 'color') else color.white,
                    scale=(0.8, 0.8),
                    z=-1
                )
                
    def update_hotbar_selection(self):
        """Tanlangan slotni vizual yangilash."""
        for i, slot in enumerate(self.hotbar_slots):
            if i == self.current_slot:
                slot.color = color.yellow
            else:
                slot.color = color.dark_gray
                
    def switch_weapon(self, slot_index):
        """Qurolni almashtirish."""
        if 0 <= slot_index < 9: # Faqat hotbar slotlarini almashtirish
            self.current_slot = slot_index
            self.update_weapon_from_inventory()
            self.update_hotbar_selection()

    def send_damage(self, target_id, damage):
        self.send_message(f"DAMAGE:{target_id}:{damage:.2f}")

# ==============================================================================
# O'yinni ishga tushirish
# ==============================================================================
generate_flat_world(size=100)
player = PvPPlayer(model='cube', color=color.blue, origin_y=-.5, speed=6)
player.position = (50, 1, 50) # Maydon markaziga joylashtirish

# Dushman qo'shish (test uchun)
# enemy1 = Enemy(position=(55, 1, 55))
# enemy2 = Enemy(position=(45, 1, 45))

# Kamera sozlamalari
camera.clip_plane_far = 200 # Ko'rish masofasini oshirish

app.run()
