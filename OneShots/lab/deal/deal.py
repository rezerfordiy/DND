
# "gender": ['ая', 'на', 'а', 'ась', 'ла', 'ой', 'ла']


data = {
    "lab": {
        "boss": {
            "name": "Доктор Бум"
        },
        "name": ["Лаборатория гениального Доктора Бума", "Лаборатории гениального Доктора Бума"],
        "salary": "***Достаточного, чтобы не сбежал сразу*** 213123123", # gender не забудь
    },
    "player": {
        "name": "Артем",
        "gender": ['ый', 'ен', '', 'ся', '', 'ым', 'ел'],
        "num": 12490142,
        "profession": "Лаборант-Универсал (Выживающий)",
    },
    "num": 12423412,
}

if __name__ == '__main__':
    with open('договор.txt', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # Заменяем все вхождения {lab.boss.name} на {lab[boss][name]} и т.д.
    # Это нужно, потому что в файле используется синтаксис с точками, а format требует квадратных скобок
    replacements = {
        "{lab.boss.name}": "{lab[boss][name]}",
        "{lab[name][0]}": "{lab[name][0]}",  # Уже правильный формат
        "{lab[name][1]}": "{lab[name][1]}",
        "{player[name]}": "{player[name]}",
        "{player[gender][0]}": "{player[gender][0]}",
        "{player[gender][1]}": "{player[gender][1]}",
        "{player[gender][2]}": "{player[gender][2]}",
        "{player[gender][3]}": "{player[gender][3]}",
        "{player[gender][4]}": "{player[gender][4]}",
        "{player[gender][5]}": "{player[gender][5]}",
        "{player[gender][6]}": "{player[gender][6]}",
        "{player[num]}": "{player[num]}",
        "{player[profession]}": "{player[profession]}",
        "{num}": "{num}",
        "{lab[salary]}": "{lab[salary]}",
    }
    
    for old, new in replacements.items():
        template = template.replace(old, new)
    
    with open('output.txt', 'w', encoding='utf-8') as f:
        f.write(template.format(**data))