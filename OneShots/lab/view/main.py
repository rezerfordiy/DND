import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QSplitter, 
                             QGraphicsView, QGraphicsScene, QGraphicsPixmapItem,
                             QGraphicsEllipseItem, QListWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QFileDialog, QSlider,
                             QLabel, QCheckBox, QGroupBox)
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QRectF

class NPC:
    def __init__(self, x, y, radius=20, color=QColor(255, 0, 0), image_path=None):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.image_path = image_path
        self.visible = True
        
    def get_pixmap(self):
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if not pixmap.isNull():
                return pixmap.scaled(self.radius*2, self.radius*2, Qt.KeepAspectRatio)
        return None

class MapManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта и NPC - Редактор")
        self.setGeometry(100, 100, 1200, 600)
        
        # Основные данные
        self.map_pieces = []
        self.npcs = []
        self.current_map_index = -1
        self.display_rect = QRectF(0, 0, 400, 400)  # Видимая область карты
        
        # Создаем интерфейс
        self.init_ui()
        
    def init_ui(self):
        # Основной разделитель
        splitter = QSplitter(Qt.Horizontal)
        
        # Панель управления
        control_panel = QWidget()
        control_layout = QVBoxLayout()
        
        # Управление картой
        map_group = QGroupBox("Управление картой")
        map_layout = QVBoxLayout()
        
        self.map_list = QListWidget()
        self.map_list.itemClicked.connect(self.select_map_piece)
        
        self.add_map_btn = QPushButton("Добавить часть карты")
        self.add_map_btn.clicked.connect(self.add_map_piece)
        
        self.remove_map_btn = QPushButton("Удалить выбранную часть")
        self.remove_map_btn.clicked.connect(self.remove_map_piece)
        
        self.visible_check = QCheckBox("Видимость выбранной части")
        self.visible_check.setChecked(True)
        self.visible_check.stateChanged.connect(self.toggle_map_visibility)
        
        map_layout.addWidget(self.map_list)
        map_layout.addWidget(self.add_map_btn)
        map_layout.addWidget(self.remove_map_btn)
        map_layout.addWidget(self.visible_check)
        map_group.setLayout(map_layout)
        
        # Управление видимой областью
        area_group = QGroupBox("Видимая область карты")
        area_layout = QVBoxLayout()
        
        self.x_slider = QSlider(Qt.Horizontal)
        self.x_slider.setRange(0, 100)
        self.x_slider.valueChanged.connect(self.update_display_rect)
        
        self.y_slider = QSlider(Qt.Horizontal)
        self.y_slider.setRange(0, 100)
        self.y_slider.valueChanged.connect(self.update_display_rect)
        
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(10, 100)
        self.width_slider.setValue(100)
        self.width_slider.valueChanged.connect(self.update_display_rect)
        
        self.height_slider = QSlider(Qt.Horizontal)
        self.height_slider.setRange(10, 100)
        self.height_slider.setValue(100)
        self.height_slider.valueChanged.connect(self.update_display_rect)
        
        area_layout.addWidget(QLabel("Позиция X:"))
        area_layout.addWidget(self.x_slider)
        area_layout.addWidget(QLabel("Позиция Y:"))
        area_layout.addWidget(self.y_slider)
        area_layout.addWidget(QLabel("Ширина (%):"))
        area_layout.addWidget(self.width_slider)
        area_layout.addWidget(QLabel("Высота (%):"))
        area_layout.addWidget(self.height_slider)
        area_group.setLayout(area_layout)
        
        # Управление NPC
        npc_group = QGroupBox("Управление NPC")
        npc_layout = QVBoxLayout()
        
        self.add_npc_btn = QPushButton("Добавить NPC")
        self.add_npc_btn.clicked.connect(self.add_npc)
        
        npc_layout.addWidget(self.add_npc_btn)
        npc_group.setLayout(npc_layout)
        
        # Собираем панель управления
        control_layout.addWidget(map_group)
        control_layout.addWidget(area_group)
        control_layout.addWidget(npc_group)
        control_layout.addStretch()
        control_panel.setLayout(control_layout)
        
        # Панель отображения
        self.display_widget = QWidget()
        display_layout = QVBoxLayout()
        
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)
        
        display_layout.addWidget(self.view)
        self.display_widget.setLayout(display_layout)
        
        # Добавляем панели в разделитель
        splitter.addWidget(control_panel)
        splitter.addWidget(self.display_widget)
        splitter.setSizes([300, 900])
        
        self.setCentralWidget(splitter)
        
    def add_map_piece(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите изображение карты", "", "Images (*.png *.jpg *.jpeg)")
        if file_path:
            self.map_pieces.append({
                'path': file_path,
                'visible': True,
                'pixmap_item': None
            })
            self.update_map_list()
            self.display_map()
            
    def remove_map_piece(self):
        if self.current_map_index >= 0 and self.current_map_index < len(self.map_pieces):
            self.map_pieces.pop(self.current_map_index)
            self.current_map_index = -1
            self.update_map_list()
            self.display_map()
            
    def select_map_piece(self, item):
        self.current_map_index = self.map_list.row(item)
        if self.current_map_index >= 0 and self.current_map_index < len(self.map_pieces):
            self.visible_check.setChecked(self.map_pieces[self.current_map_index]['visible'])
            
    def toggle_map_visibility(self, state):
        if self.current_map_index >= 0 and self.current_map_index < len(self.map_pieces):
            self.map_pieces[self.current_map_index]['visible'] = state == Qt.Checked
            self.display_map()
            
    def update_map_list(self):
        self.map_list.clear()
        for i, piece in enumerate(self.map_pieces):
            self.map_list.addItem(f"Часть {i+1} {'(видима)' if piece['visible'] else '(скрыта)'}")
            
    def update_display_rect(self):
        # Обновляем видимую область на основе значений слайдеров
        if self.current_map_index >= 0 and self.current_map_index < len(self.map_pieces):
            pixmap = QPixmap(self.map_pieces[self.current_map_index]['path'])
            if not pixmap.isNull():
                img_width = pixmap.width()
                img_height = pixmap.height()
                
                x = self.x_slider.value() / 100 * img_width
                y = self.y_slider.value() / 100 * img_height
                width = self.width_slider.value() / 100 * img_width
                height = self.height_slider.value() / 100 * img_height
                
                self.display_rect = QRectF(x, y, width, height)
                self.display_map()
                
    def display_map(self):
        self.scene.clear()
        
        # Отображаем видимые части карты
        for piece in self.map_pieces:
            if piece['visible']:
                pixmap = QPixmap(piece['path'])
                if not pixmap.isNull():
                    # Если это текущая выбранная часть, применяем видимую область
                    if piece == self.map_pieces[self.current_map_index] if self.current_map_index >= 0 else False:
                        cropped = pixmap.copy(self.display_rect.toRect())
                        item = self.scene.addPixmap(cropped)
                    else:
                        item = self.scene.addPixmap(pixmap)
                    piece['pixmap_item'] = item
                    
        # Отображаем NPC
        for npc in self.npcs:
            if npc.visible:
                npc_pixmap = npc.get_pixmap()
                if npc_pixmap:
                    item = self.scene.addPixmap(npc_pixmap)
                    item.setPos(npc.x - npc.radius, npc.y - npc.radius)
                else:
                    item = QGraphicsEllipseItem(npc.x - npc.radius, npc.y - npc.radius, 
                                              npc.radius*2, npc.radius*2)
                    item.setBrush(npc.color)
                    self.scene.addItem(item)
                    
        self.view.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        
    def add_npc(self):
        if len(self.map_pieces) > 0:
            # Просто добавляем NPC в центр первой видимой карты
            for piece in self.map_pieces:
                if piece['visible']:
                    pixmap = QPixmap(piece['path'])
                    if not pixmap.isNull():
                        x = pixmap.width() / 2
                        y = pixmap.height() / 2
                        self.npcs.append(NPC(x, y))
                        self.display_map()
                        break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapManager()
    window.show()
    sys.exit(app.exec_())