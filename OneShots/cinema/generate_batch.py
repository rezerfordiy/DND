#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
from monster_generator import MonsterCardGenerator

def generate_monster_cards_from_directory(json_dir='data', output_dir='output'):
    """Генерирует карточки из всех JSON файлов в директории"""
    generator = MonsterCardGenerator()
    
    if not os.path.exists(json_dir):
        print(f"❌ Директория {json_dir} не существует")
        return
    
    # Создаем директорию для вывода
    os.makedirs(output_dir, exist_ok=True)
    
    # Ищем все JSON файлы
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    
    if not json_files:
        print(f"❌ В директории {json_dir} не найдено JSON файлов")
        return
    
    print(f"📂 Найдено {len(json_files)} JSON файлов")
    
    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)
        print(f"🔧 Обработка: {json_file}")
        generator.generate_from_json(json_path, output_dir)
    
    print(f"✅ Все карточки сгенерированы в директории {output_dir}")

def create_index_html(output_dir='output'):
    """Создает индексный HTML файл со всеми карточками"""
    html_files = [f for f in os.listdir(output_dir) if f.endswith('.html') and f != 'index.html']
    
    if not html_files:
        return
    
    html_content = '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Библиотека монстров D&D</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
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
            }
            
            .container {
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
                padding: 20px;
                background: rgba(30, 30, 46, 0.9);
                border-radius: 15px;
                border: 2px solid #444;
            }
            
            .header h1 {
                font-size: 3rem;
                color: #ffcc00;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #aaa;
                font-size: 1.2rem;
            }
            
            .monster-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
                gap: 25px;
                margin-bottom: 40px;
            }
            
            .monster-card-preview {
                background: rgba(30, 30, 46, 0.9);
                border-radius: 10px;
                padding: 20px;
                border: 2px solid #444;
                transition: transform 0.3s, border-color 0.3s;
                text-decoration: none;
                color: inherit;
                display: block;
            }
            
            .monster-card-preview:hover {
                transform: translateY(-5px);
                border-color: #ffcc00;
            }
            
            .preview-name {
                font-size: 1.5rem;
                color: #ff9900;
                margin-bottom: 5px;
            }
            
            .preview-type {
                color: #aaa;
                font-style: italic;
                margin-bottom: 15px;
            }
            
            .preview-stats {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 10px;
                margin-bottom: 15px;
            }
            
            .preview-stat {
                text-align: center;
                padding: 8px;
                background: rgba(40, 40, 60, 0.5);
                border-radius: 5px;
            }
            
            .preview-cr {
                display: inline-block;
                background: linear-gradient(to right, #cc3300, #ff6600);
                color: white;
                padding: 5px 15px;
                border-radius: 15px;
                font-weight: bold;
            }
            
            .footer {
                text-align: center;
                padding: 20px;
                color: #777;
                border-top: 1px solid #444;
                margin-top: 40px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Библиотека монстров D&D</h1>
                <p>Все сгенерированные карточки монстров</p>
            </div>
            
            <div class="monster-grid">
    '''
    
    for html_file in sorted(html_files):
        # Извлекаем имя монстра из названия файла
        monster_name = html_file.replace('.html', '').replace('_', ' ').title()
        
        html_content += f'''
                <a href="{html_file}" class="monster-card-preview">
                    <div class="preview-name">{monster_name}</div>
                    <div class="preview-type">Карточка монстра D&D</div>
                    <div class="preview-stats">
                        <div class="preview-stat">⚔️ Атаки</div>
                        <div class="preview-stat">🛡️ Защита</div>
                        <div class="preview-stat">🎲 Броски</div>
                    </div>
                    <div class="preview-cr">Открыть карточку</div>
                </a>
        '''
    
    html_content += '''
            </div>
            
            <div class="footer">
                <p>Сгенерировано генератором монстров D&D</p>
                <p>Все карточки содержат интерактивные элементы для бросков кубиков</p>
            </div>
        </div>
    </body>
    </html>
    '''
    
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Создан индексный файл: {index_path}")

if __name__ == "__main__":
    generate_monster_cards_from_directory('data', 'output')
    create_index_html('output')