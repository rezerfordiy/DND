#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import argparse
from datetime import datetime
from pathlib import Path

class MonsterCardGenerator:
    def __init__(self):
        self.template = self.load_template()
        
    def load_template(self):
        """Загружает HTML-шаблон из файла или использует встроенный"""
        template_file = Path(__file__).parent / "monster_template.html"
        if template_file.exists():
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return self.get_default_template()
    
    def get_default_template(self):
        """Возвращает стандартный HTML-шаблон"""
        return '''<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{monster_name} - Карточка монстра D&D</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        /* CSS стили будут здесь */
        {css}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>{monster_name}</h1>
            <p class="monster-type">{monster_type}, {alignment}</p>
            {challenge_badge}
        </div>
        
        <div class="monster-card">
            <div class="image-section">
                <div class="monster-image">
                    <img src="{image_url}" alt="{monster_name}">
                </div>
                
                <div class="stats-grid">
                    {stats_html}
                </div>
            </div>
            
            <div class="content-section">
                {patterns_html}
                
                <div class="characteristics">
                    <h3 class="section-title"><i class="fas fa-chart-bar"></i> Характеристики</h3>
                    <div class="char-list">
                        {characteristics_html}
                    </div>
                </div>
                
                {abilities_html}
                
                {actions_html}
                
                {items_html}
            </div>
        </div>
        
        <div class="footer">
            <p>{lore}</p>
            <p class="generated-info">Сгенерировано {timestamp}</p>
        </div>
    </div>
    
    <script>
        // JavaScript для бросков кубиков
        {javascript}
    </script>
</body>
</html>'''
    
    def calculate_modifier(self, value):
        """Рассчитывает модификатор характеристики"""
        return (value - 10) // 2
    
    def generate_stats_html(self, monster_data):
        """Генерирует HTML для характеристик"""
        stats = {
            'strength': 'Сила',
            'dexterity': 'Ловкость',
            'constitution': 'Телосложение',
            'intelligence': 'Интеллект',
            'wisdom': 'Мудрость',
            'charisma': 'Харизма'
        }
        
        html_parts = []
        for stat_id, stat_name in stats.items():
            value = monster_data.get(stat_id, 10)
            modifier = self.calculate_modifier(value)
            sign = '+' if modifier >= 0 else ''
            
            html_parts.append(f'''
                <div class="stat-box">
                    <div class="stat-value">{value}({sign}{modifier})</div>
                    <div class="stat-name">{stat_name}</div>
                </div>
            ''')
        
        return ''.join(html_parts)
    
    def generate_patterns_html(self, patterns):
        """Генерирует HTML для паттернов поведения"""
        if not patterns:
            return ''
        
        patterns_list = ''
        for i, pattern in enumerate(patterns, 1):
            patterns_list += f'''
                <li class="pattern-item">
                    <div class="pattern-title">Паттерн {i}</div>
                    <div class="pattern-desc">{pattern}</div>
                </li>
            '''
        
        return f'''
        <div class="patterns">
            <h3 class="section-title"><i class="fas fa-robot"></i> Паттерны поведения</h3>
            <ul class="pattern-list">
                {patterns_list}
            </ul>
        </div>
        '''
    
    def format_saving_throws(self, saving_throws, monster_data):
        """Форматирует спасброски"""
        if not saving_throws:
            return 'Нет'
        
        formatted = []
        for st in saving_throws:
            stat_name = st.get('stat', '').lower()
            bonus = st.get('bonus', 0)
            
            # Если бонус не указан, рассчитываем автоматически
            if bonus == 0 and stat_name in monster_data:
                modifier = self.calculate_modifier(monster_data[stat_name])
                proficiency = monster_data.get('proficiency_bonus', 0)
                bonus = modifier + proficiency
            
            formatted.append(f"{st['stat']} {bonus:+d}")
        
        return ', '.join(formatted)
    
    def format_skills(self, skills):
        """Форматирует навыки"""
        if not skills:
            return 'Нет'
        
        formatted = []
        for skill in skills:
            name = skill.get('name', '')
            bonus = skill.get('bonus', 0)
            formatted.append(f"{name} {bonus:+d}")
        
        return ', '.join(formatted)
    
    def generate_characteristics_html(self, monster_data):
        """Генерирует HTML для характеристик монстра"""
        characteristics = [
            {
                'name': 'Класс Доспеха',
                'value': monster_data.get('armor_class', 'Не указан')
            },
            {
                'name': 'Хиты',
                'value': f"{monster_data.get('hit_points', 0)} ({monster_data.get('hit_dice', 'Не указано')})"
            },
            {
                'name': 'Скорость',
                'value': monster_data.get('speed', 'Не указана')
            },
            # added none and skipness
            {
                'name': 'Чувства',
                'value': monster_data.get('senses', None)
            },
            {
                'name': 'Спасброски',
                'value': self.format_saving_throws(monster_data.get('saving_throws'), monster_data)
            },
            {
                'name': 'Навыки',
                'value': self.format_skills(monster_data.get('skills'))
            },
            {
                'name': 'Иммунитеты',
                'value': monster_data.get('damage_immunities', None)
            },
            {
                'name':'Сопротивления',
                'value:': monster_data.get('', None)
            },
            {
                'name': 'Языки',
                'value': monster_data.get('languages', None)
            }
        ]
        
        html_parts = []
        for char in characteristics:
            if char['value'] is None:
                continue
            html_parts.append(f'''
                <div class="char-item">
                    <span class="char-name">{char['name']}:</span>
                    <span class="char-value">{char['value']}</span>
                </div>
            ''')
        
        return ''.join(html_parts)
    
    def calculate_attack_bonus(self, action, monster_data):
        """Рассчитывает бонус атаки"""
        if action.get('attack_bonus'):
            return action['attack_bonus']
        
        # Авторасчет на основе характеристики
        ability = action.get('ability', '').lower()
        if ability in monster_data:
            modifier = self.calculate_modifier(monster_data[ability])
            proficiency = monster_data.get('proficiency_bonus', 0)
            return modifier + proficiency
        
        return 0
    
    def calculate_damage_bonus(self, action, monster_data):
        """Рассчитывает бонус урона"""
        if 'damage_bonus' in action:
            return action['damage_bonus']
        
        # Авторасчет на основе характеристики
        damage_ability = action.get('damage_ability', action.get('ability', '')).lower()
        if damage_ability in monster_data:
            return self.calculate_modifier(monster_data[damage_ability])
        
        return 0
    
    def generate_actions_html(self, actions, monster_data):
        """Генерирует HTML для действий"""
        if not actions:
            return ''
        
        actions_list = ''
        for action in actions:
            attack_bonus = self.calculate_attack_bonus(action, monster_data)
            damage_bonus = self.calculate_damage_bonus(action, monster_data)
            
            attack_text = f"{attack_bonus:+d} к попаданию" if attack_bonus else ""
            range_text = f", {action.get('range', '')}" if action.get('range') else ""
            damage_text = ""
            
            if action.get('damage_dice'):
                damage_text = f", урон: {action['damage_dice']}"
                if damage_bonus != 0:
                    damage_text += f" {damage_bonus:+d}"
                if action.get('damage_type'):
                    damage_text += f" {action['damage_type']}"
            
            description = f"<br>{action['description']}" if action.get('description') else ""
            
            # Создаем JSON для хранения данных о броске
            action_data = {
                'name': action['name'],
                'attack_bonus': attack_bonus,
                'damage_dice': action.get('damage_dice', ''),
                'damage_bonus': damage_bonus,
                'damage_type': action.get('damage_type', '')
            }
            
            actions_list += f'''
                <li class="action-item" data-action='{json.dumps(action_data, ensure_ascii=False)}'>
                    <div class="action-title">{action['name']}</div>
                    <div class="action-desc">
                        {attack_text}{range_text}{damage_text}{description}
                    </div>
                    <div class="dice-roll" style="display: none;"></div>
                </li>
            '''
        
        return f'''
        <div class="actions">
            <h3 class="section-title"><i class="fas fa-fist-raised"></i> Действия</h3>
            <ul class="action-list">
                {actions_list}
            </ul>
        </div>
        '''
    
    def generate_abilities_html(self, abilities):
        """Генерирует HTML для способностей"""
        if not abilities:
            return ''
        
        abilities_list = ''
        for ability in abilities:
            abilities_list += f'''
                <li class="ability-item">
                    <div class="ability-title">{ability['name']}</div>
                    <div class="ability-desc">{ability['description']}</div>
                </li>
            '''
        
        return f'''
        <div class="abilities">
            <h3 class="section-title"><i class="fas fa-fire"></i> Способности</h3>
            <ul class="ability-list">
                {abilities_list}
            </ul>
        </div>
        '''
    
    def generate_items_html(self, items):
        """Генерирует HTML для предметов"""
        if not items:
            return ''
        
        items_list = ''
        for item in items:
            items_list += f'''
                <li class="item-item">
                    <div class="item-title">{item['name']}</div>
                    <div class="item-desc">{item['description']}</div>
                </li>
            '''
        
        return f'''
        <div class="items">
            <h3 class="section-title"><i class="fas fa-gem"></i> Сокровища и предметы</h3>
            <ul class="item-list">
                {items_list}
            </ul>
        </div>
        '''
    
    def generate_css(self):
        """Возвращает CSS стили"""
        return '''
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #e0e0e0;
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 2.8rem;
            color: #ffcc00;
            text-shadow: 0 0 10px rgba(255, 204, 0, 0.5);
            margin-bottom: 10px;
            letter-spacing: 1px;
        }
        
        .monster-type {
            font-size: 1.4rem;
            color: #aaa;
            font-style: italic;
            margin-bottom: 15px;
        }
        
        .monster-card {
            display: flex;
            flex-wrap: wrap;
            background: rgba(30, 30, 46, 0.9);
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
            border: 2px solid #444;
        }
        
        .image-section {
            flex: 1;
            min-width: 300px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            background: rgba(20, 20, 35, 0.8);
            border-right: 2px solid #333;
        }
        
        .monster-image {
            width: 100%;
            max-width: 400px;
            height: 300px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
            margin-bottom: 20px;
            border: 3px solid #555;
        }
        
        .monster-image img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            width: 100%;
            max-width: 400px;
        }
        
        .stat-box {
            background: rgba(40, 40, 60, 0.8);
            border-radius: 8px;
            padding: 12px 5px;
            text-align: center;
            border: 1px solid #555;
            transition: transform 0.2s;
        }
        
        .stat-box:hover {
            transform: translateY(-3px);
            border-color: #ffcc00;
        }
        
        .stat-value {
            font-size: 1.8rem;
            font-weight: bold;
            color: #ffcc00;
        }
        
        .stat-name {
            font-size: 0.9rem;
            color: #aaa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .content-section {
            flex: 2;
            min-width: 500px;
            padding: 25px;
            display: flex;
            flex-direction: column;
        }
        
        .section-title {
            font-size: 1.6rem;
            color: #ffcc00;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #555;
            display: flex;
            align-items: center;
        }
        
        .section-title i {
            margin-right: 10px;
        }
        
        .characteristics {
            margin-bottom: 25px;
        }
        
        .char-list {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
        }
        
        .char-item {
            background: rgba(50, 50, 70, 0.5);
            padding: 12px 15px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            border-left: 4px solid #555;
        }
        
        .char-item:nth-child(odd) {
            border-left-color: #ff9900;
        }
        
        .char-name {
            font-weight: bold;
            color: #ccc;
        }
        
        .char-value {
            color: #ffcc00;
            font-weight: bold;
        }
        
        .patterns, .abilities, .actions, .items {
            margin-bottom: 25px;
        }
        
        .pattern-list, .ability-list, .action-list, .item-list {
            list-style-type: none;
        }
        
        .pattern-item, .ability-item, .action-item, .item-item {
            background: rgba(40, 40, 60, 0.5);
            padding: 15px;
            margin-bottom: 12px;
            border-radius: 8px;
            border-left: 4px solid #777;
            transition: background 0.3s;
        }
        
        .pattern-item:hover, .ability-item:hover, .action-item:hover, .item-item:hover {
            background: rgba(50, 50, 80, 0.7);
        }
        
        .pattern-title, .ability-title, .action-title, .item-title {
            color: #ffcc00;
            font-weight: bold;
            margin-bottom: 5px;
            font-size: 1.1rem;
        }
        
        .pattern-desc, .ability-desc, .action-desc, .item-desc {
            color: #ccc;
            line-height: 1.5;
        }
        
        .action-item {
            cursor: pointer;
        }
        
        .dice-roll {
            background: rgba(255, 204, 0, 0.1);
            padding: 8px 12px;
            border-radius: 6px;
            margin-top: 8px;
            border-left: 3px solid #ffcc00;
            font-family: monospace;
            font-size: 0.9rem;
        }
        
        .cr-badge {
            display: inline-block;
            background: linear-gradient(to right, #cc3300, #ff6600);
            color: white;
            padding: 8px 20px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.4rem;
            margin-top: 10px;
            box-shadow: 0 4px 8px rgba(204, 51, 0, 0.3);
        }
        
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #777;
            font-size: 0.9rem;
            padding-top: 20px;
            border-top: 1px solid #444;
        }
        
        .generated-info {
            font-size: 0.8rem;
            color: #666;
            margin-top: 10px;
        }
        
        @media (max-width: 900px) {
            .monster-card {
                flex-direction: column;
            }
            
            .image-section {
                border-right: none;
                border-bottom: 2px solid #333;
            }
            
            .content-section {
                min-width: 100%;
            }
            
            .char-list {
                grid-template-columns: 1fr;
            }
        }
        
        @media (max-width: 600px) {
            .stats-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .header h1 {
                font-size: 2rem;
            }
        }
        '''
    
    def generate_javascript(self):
        """Возвращает JavaScript для бросков кубиков"""
        return '''
        document.addEventListener('DOMContentLoaded', function() {
            const actionItems = document.querySelectorAll('.action-item');
        
            // Функция для парсинга записи кубиков (поддерживает d и к)
            function parseDiceNotation(diceNotation) {
                // Заменяем русскую 'к' на латинскую 'd' и парсим
                const normalized = diceNotation.toLowerCase().replace('к', 'd');
                const match = normalized.match(/(\\d+)d(\\d+)/);
                
                if (match) {
                    return {
                        count: parseInt(match[1]),
                        sides: parseInt(match[2])
                    };
                }
                return null;
            }
            
            // Функция для броска кубиков
            function rollDice(count, sides) {
                let total = 0;
                let rolls = [];
                
                for (let i = 0; i < count; i++) {
                    const roll = Math.floor(Math.random() * sides) + 1;
                    rolls.push(roll);
                    total += roll;
                }
                
                return { rolls, total };
            }
            
            actionItems.forEach(item => {
                item.addEventListener('click', function() {
                    const actionData = JSON.parse(this.getAttribute('data-action'));
                    const diceRollDiv = this.querySelector('.dice-roll');
                    
                    // Бросок атаки
                    let attackRoll = '';
                    if (actionData.attack_bonus !== undefined && actionData.attack_bonus !== null) {
                        const d20 = Math.floor(Math.random() * 20) + 1;
                        const total = d20 + actionData.attack_bonus;
                        
                        let specialEffects = '';
                        if (d20 === 20) {
                            specialEffects = ' ⚡КРИТИЧЕСКИЙ УСПЕХ!';
                        } else if (d20 === 1) {
                            specialEffects = ' 💥КРИТИЧЕСКИЙ ПРОВАЛ!';
                        }
                        
                        attackRoll = `🎯 <strong>Атака:</strong> ${d20} + ${actionData.attack_bonus} = <strong>${total}</strong>${specialEffects}`;
                    }
                    
                    // Бросок урона
                    let damageRoll = '';
                    if (actionData.damage_dice) {
                        const diceInfo = parseDiceNotation(actionData.damage_dice);
                        
                        if (diceInfo) {
                            const { count, sides } = diceInfo;
                            const damageBonus = actionData.damage_bonus || 0;
                            const { rolls, total: diceTotal } = rollDice(count, sides);
                            const totalDamage = diceTotal + damageBonus;
                            
                            damageRoll = `💥 <strong>Урон:</strong> ${rolls.join(' + ')}`;
                            
                            if (damageBonus !== 0) {
                                damageRoll += ` ${damageBonus > 0 ? '+' : ''}${damageBonus}`;
                            }
                            
                            damageRoll += ` = <strong>${totalDamage}</strong> ${actionData.damage_type || ''}`;
                            
                            // Добавляем информацию о кубиках
                            damageRoll += `<br>🎲 <em>${count}d${sides}`;
                            if (damageBonus !== 0) {
                                damageRoll += ` ${damageBonus > 0 ? '+' : ''}${damageBonus}`;
                            }
                            damageRoll += `</em>`;
                        } else {
                            damageRoll = `⚠️ Неверный формат кубиков: "${actionData.damage_dice}"`;
                        }
                    }
                    
                    // Показываем результат
                    diceRollDiv.innerHTML = `${attackRoll}${attackRoll && damageRoll ? '<br><br>' : ''}${damageRoll}`;
                    diceRollDiv.style.display = 'block';
                    
                    // Автоскрытие через 15 секунд
                    setTimeout(() => {
                        diceRollDiv.style.display = 'none';
                    }, 15000);
                });
            });
        });
        '''
    
    def generate_from_json(self, json_file_path, output_dir='output'):
        """Генерирует HTML карточку из JSON файла"""
        try:
            # Чтение JSON файла
            with open(json_file_path, 'r', encoding='utf-8') as f:
                monster_data = json.load(f)
            
            # Создаем директорию для вывода, если её нет
            os.makedirs(output_dir, exist_ok=True)
            
            # Генерация HTML
            challenge_badge = ''
            if monster_data.get('challenge_rating'):
                challenge_badge = f'<div class="cr-badge">Опасность: {monster_data["challenge_rating"]}</div>'
            
            image_url = monster_data.get('image', 'https://via.placeholder.com/400x300/2d3748/4a5568?text=No+Image')
            
            html_content = self.template.format(
                monster_name=monster_data.get('name', 'Неизвестный монстр'),
                monster_type=monster_data.get('type', 'Неизвестно'),
                alignment=monster_data.get('alignment', 'Неизвестно'),
                challenge_badge=challenge_badge,
                image_url=image_url,
                stats_html=self.generate_stats_html(monster_data),
                patterns_html=self.generate_patterns_html(monster_data.get('patterns')),
                characteristics_html=self.generate_characteristics_html(monster_data),
                abilities_html=self.generate_abilities_html(monster_data.get('abilities')),
                actions_html=self.generate_actions_html(monster_data.get('actions'), monster_data),
                items_html=self.generate_items_html(monster_data.get('items')),
                lore=monster_data.get('lore', 'Сгенерировано генератором монстров'),
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                css=self.generate_css(),
                javascript=self.generate_javascript()
            )
            
            # Сохранение файла
            output_filename = f"{monster_data.get('name', 'monster').replace(' ', '_').lower()}.html"
            output_path = os.path.join(output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ Карточка успешно создана: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"❌ Ошибка при генерации карточки: {str(e)}")
            return None
    
    def generate_batch_from_json(self, json_file_path, output_dir='output'):
        """Генерирует несколько карточек из JSON файла с массивом монстров"""
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Проверяем, является ли data массивом или одиночным объектом
            if isinstance(data, list):
                monsters = data
            else:
                monsters = [data]
            
            generated_files = []
            for i, monster_data in enumerate(monsters):
                # Создаем временный JSON файл для каждого монстра
                temp_json_path = os.path.join(output_dir, f'temp_monster_{i}.json')
                with open(temp_json_path, 'w', encoding='utf-8') as f:
                    json.dump(monster_data, f, ensure_ascii=False, indent=2)
                
                # Генерируем карточку
                output_file = self.generate_from_json(temp_json_path, output_dir)
                if output_file:
                    generated_files.append(output_file)
                
                # Удаляем временный файл
                os.remove(temp_json_path)
            
            print(f"✅ Сгенерировано {len(generated_files)} карточек")
            return generated_files
            
        except Exception as e:
            print(f"❌ Ошибка при пакетной генерации: {str(e)}")
            return []


def main():
    parser = argparse.ArgumentParser(description='Генератор карточек монстров D&D из JSON')
    parser.add_argument('json_file', help='Путь к JSON файлу с данными монстра')
    parser.add_argument('-o', '--output', default='output', help='Директория для сохранения HTML файлов')
    parser.add_argument('-b', '--batch', action='store_true', help='Обработать JSON файл как массив монстров')
    
    args = parser.parse_args()
    
    generator = MonsterCardGenerator()
    
    if args.batch:
        generator.generate_batch_from_json(args.json_file, args.output)
    else:
        generator.generate_from_json(args.json_file, args.output)


if __name__ == "__main__":
    main()