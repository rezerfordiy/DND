import pygame
import json
import os

# Инициализация
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("D&D Soundboard")
font = pygame.font.SysFont('Arial', 20)

# Загрузка конфигурации
def load_config():
    try:
        with open('soundboard.json', 'r') as f:
            return json.load(f)
    except:
        print("cannot open file")
        return {
            "sounds": {
                # "Взрыв": {"file": "sword.wav", "type": "sound"},
                "Моцарт": {"file": "../source/Моцарт - Симфония 40.mp3", "type": "music"},
                "Вивальди": {"file": "../source/AntonioVivaldi_Spring.mp3", "type": "music"},
                "Лифт": {"file": "../source/lift.mpeg", "type": "music"},
                "Песняры": {"file": "static/kosil.mpeg", "type": "music"},
                "Эпичная": {"file": "static/fight.mpeg", "type": "music"},
                "В кузне": {"file": "../source/iBenji - Boom (feat. Talabun).mp3", "type": "music"},
                "На вулкане": {"file": "../source/DOOM.mpeg", "type": "music"},
                "Матушка": {"file": "../source/Матушка.mpeg", "type": "music"},
                "Матушка полная": {"file": "../source/Матушка полная.mpeg", "type": "music"},
                "Крик": {"file": "../source/Wilhelm_scream.mpeg", "type": "sound"},
                "Бум": {"file": "../source/the-sound-of-a-small-explosion.mp3", "type": "sound"},
                # "Моцарт": {"file": "../source/Моцарт - Симфония 40.mp3", "type": "music"},
                
                

            },
            "volume": 0.7
        }

# Сохранение конфигурации
def save_config():
    with open('soundboard.json', 'w') as f:
        json.dump(config, f, indent=2)

# Создание кнопок
def create_buttons():
    buttons = []
    sounds = config['sounds'].items()
    
    for i, (name, data) in enumerate(sounds):
        row = i // 3
        col = i % 3
        rect = pygame.Rect(50 + col * 250, 50 + row * 150, 200, 100)
        
        # Определяем цвет в зависимости от типа
        if data['type'] == 'music':
            base_color = (180, 70, 130)  # Фиолетовый для музыки
        else:
            base_color = (70, 130, 180)  # Синий для звуков
            
        buttons.append({
            'rect': rect,
            'name': name,
            'file': data['file'],
            'type': data['type'],
            'base_color': base_color,
            'color': base_color,
            'active': False  # Для музыки: активно ли воспроизведение
        })
    return buttons

# Основная конфигурация
config = load_config()
buttons = create_buttons()
pygame.mixer.music.set_volume(config['volume'])

# Главный цикл
running = True
current_music = None  # Текущая играющая музыка

while running:
    screen.fill((25, 25, 35))  # Тёмный фон
    
    # Отрисовка кнопок
    for btn in buttons:
        # Если это музыка и она активна, делаем кнопку светлее
        if btn['type'] == 'music' and btn['active']:
            color = (min(btn['base_color'][0] + 50, 255),
                     min(btn['base_color'][1] + 50, 255),
                     min(btn['base_color'][2] + 50, 255))
        else:
            color = btn['color']
            
        pygame.draw.rect(screen, color, btn['rect'], 0, 10)
        pygame.draw.rect(screen, (180, 180, 200), btn['rect'], 3, 10)
        text = font.render(btn['name'], True, (255, 255, 255))
        screen.blit(text, (btn['rect'].centerx - text.get_width()//2, 
                         btn['rect'].centery - text.get_height()//2))
    
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            # Проверка нажатия кнопок
            for btn in buttons:
                if btn['rect'].collidepoint(pos):
                    if btn['type'] == 'sound':
                        # Обработка звуков (как раньше)
                        try:
                            sound = pygame.mixer.Sound(btn['file'])
                            sound.set_volume(config['volume'])
                            sound.play()
                            btn['color'] = (180, 70, 80)  # Подсветка при нажатии
                        except:
                            print(f"Ошибка загрузки: {btn['file']}")
                    elif btn['type'] == 'music':
                        # Обработка музыки (включить/выключить)
                        if btn['active']:
                            pygame.mixer.music.stop()
                            btn['active'] = False
                        else:
                            # Останавливаем другую музыку, если играет
                            if current_music:
                                current_music['active'] = False
                            try:
                                pygame.mixer.music.load(btn['file'])
                                pygame.mixer.music.play(-1)  # -1 означает зацикливание
                                btn['active'] = True
                                current_music = btn
                            except:
                                print(f"Ошибка загрузки музыки: {btn['file']}")
        
        # Сброс цвета кнопок (только для звуков)
        if event.type == pygame.MOUSEBUTTONUP:
            for btn in buttons:
                if btn['type'] == 'sound':
                    btn['color'] = btn['base_color']
    
    pygame.display.flip()

# Сохранение перед выходом
save_config()
pygame.quit()