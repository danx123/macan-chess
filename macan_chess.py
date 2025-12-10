"""
Macan Chess - Professional Tiger-Themed Chess Application
Versi Final Fix: UI Modern + Logic Lengkap + AI + Save/Load
Fixed: AI Move Error
"""

import sys
import json
import random
import os
from pathlib import Path
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                               QHBoxLayout, QGraphicsView, QGraphicsScene, 
                               QGraphicsRectItem, QPushButton,
                               QLabel, QFrame, QFileDialog,
                               QMessageBox, QGraphicsTextItem, QGridLayout, 
                               QSizePolicy, QInputDialog, QDialog)
from PySide6.QtCore import Qt, QTimer, Signal, QRectF
from PySide6.QtGui import (QColor, QBrush, QLinearGradient, QPainter, QFont)

# --- KONFIGURASI ---
LOGICAL_SQUARE_SIZE = 100
BOARD_SIZE = LOGICAL_SQUARE_SIZE * 8

PIECE_SYMBOLS = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',  # White
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟'   # Black
}

ANIMAL_NAMES = {
    'K': 'Lion', 'Q': 'Panther', 'R': 'Boar', 'B': 'Tiger', 'N': 'Cheetah', 'P': 'Rabbit'
}

class ChessPiece:
    def __init__(self, piece_type, color, pos, has_moved=False):
        self.type = piece_type
        self.color = color
        self.pos = pos
        self.has_moved = has_moved
        
    def get_symbol(self):
        symbol = self.type.upper() if self.color == 'white' else self.type.lower()
        return PIECE_SYMBOLS[symbol]
    
    def get_animal_name(self):
        return ANIMAL_NAMES[self.type.upper()]

class ChessBoard:
    """Logika permainan catur (Game Logic) yang ditingkatkan"""
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.current_player = 'white'
        self.move_history = []
        self.captured_pieces = {'white': [], 'black': []}
        self.king_positions = {'white': (7, 4), 'black': (0, 4)}
        self.game_mode = 'pvp' # 'pvp' atau 'pve'
        self.init_board()
        
    def init_board(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.captured_pieces = {'white': [], 'black': []}
        self.move_history = []
        self.current_player = 'white'
        
        piece_order = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        # Black
        for col, piece_type in enumerate(piece_order):
            self.board[0][col] = ChessPiece(piece_type, 'black', (0, col))
        for col in range(8):
            self.board[1][col] = ChessPiece('P', 'black', (1, col))
        self.king_positions['black'] = (0, 4)
            
        # White
        for col, piece_type in enumerate(piece_order):
            self.board[7][col] = ChessPiece(piece_type, 'white', (7, col))
        for col in range(8):
            self.board[6][col] = ChessPiece('P', 'white', (6, col))
        self.king_positions['white'] = (7, 4)
    
    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None

    def _is_on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def get_all_valid_moves(self, color):
        """Mendapatkan semua gerakan legal untuk satu warna (untuk AI/Checkmate)"""
        all_moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == color:
                    moves = self.get_valid_moves(r, c)
                    for target in moves:
                        all_moves.append(((r, c), target))
        return all_moves

    def get_valid_moves(self, row, col):
        piece = self.get_piece(row, col)
        if not piece: return []
        
        moves = []
        piece_type = piece.type.upper()
        potential_moves = []
        
        if piece_type == 'P':
            d = -1 if piece.color == 'white' else 1
            # Maju 1
            if self._is_on_board(row+d, col) and self.board[row+d][col] is None:
                potential_moves.append((row+d, col))
                # Maju 2 (Awal)
                start_row = 6 if piece.color == 'white' else 1
                if row == start_row and self.board[row+2*d][col] is None:
                    potential_moves.append((row+2*d, col))
            # Makan
            for dc in [-1, 1]:
                if self._is_on_board(row+d, col+dc):
                    target = self.board[row+d][col+dc]
                    if target and target.color != piece.color:
                        potential_moves.append((row+d, col+dc))
                        
        elif piece_type == 'N':
            offsets = [(2,1), (2,-1), (-2,1), (-2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
            for dr, dc in offsets:
                if self._is_on_board(row+dr, col+dc):
                    target = self.board[row+dr][col+dc]
                    if target is None or target.color != piece.color:
                        potential_moves.append((row+dr, col+dc))

        elif piece_type == 'K':
            offsets = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
            for dr, dc in offsets:
                if self._is_on_board(row+dr, col+dc):
                    target = self.board[row+dr][col+dc]
                    if target is None or target.color != piece.color:
                        potential_moves.append((row+dr, col+dc))

        else: # R, B, Q (Sliding pieces)
            directions = []
            if piece_type in ['R', 'Q']: directions.extend([(0, 1), (0, -1), (1, 0), (-1, 0)])
            if piece_type in ['B', 'Q']: directions.extend([(1, 1), (1, -1), (-1, 1), (-1, -1)])
            
            for dr, dc in directions:
                for i in range(1, 8):
                    nr, nc = row + dr*i, col + dc*i
                    if not self._is_on_board(nr, nc): break
                    target = self.board[nr][nc]
                    if target is None:
                        potential_moves.append((nr, nc))
                    else:
                        if target.color != piece.color:
                            potential_moves.append((nr, nc))
                        break

        # --- Filter: Apakah gerakan menyebabkan Raja sendiri Check? ---
        legal_moves = []
        for tr, tc in potential_moves:
            if not self._would_be_in_check(row, col, tr, tc):
                legal_moves.append((tr, tc))
                
        return legal_moves

    def _would_be_in_check(self, fr, fc, tr, tc):
        """Simulasi gerakan untuk cek legalitas"""
        piece = self.board[fr][fc]
        target = self.board[tr][tc]
        
        # Simpan state lama
        original_pos = piece.pos
        old_king_pos = self.king_positions[piece.color]
        
        # Lakukan gerakan sementara
        self.board[tr][tc] = piece
        self.board[fr][fc] = None
        piece.pos = (tr, tc)
        if piece.type.upper() == 'K':
            self.king_positions[piece.color] = (tr, tc)
            
        # Cek apakah raja diserang
        in_check = self.is_check(piece.color)
        
        # Kembalikan state
        self.board[fr][fc] = piece
        self.board[tr][tc] = target
        piece.pos = original_pos
        self.king_positions[piece.color] = old_king_pos
        
        return in_check

    def is_check(self, color_to_check):
        """Apakah raja warna tersebut sedang diserang?"""
        king_r, king_c = self.king_positions[color_to_check]
        opponent = 'black' if color_to_check == 'white' else 'white'
        
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == opponent:
                    if p.type.upper() == 'P':
                        d = -1 if p.color == 'white' else 1
                        if abs(c - king_c) == 1 and r + d == king_r:
                            return True
                    elif p.type.upper() == 'K':
                        if abs(r - king_r) <= 1 and abs(c - king_c) <= 1:
                            return True
                    elif p.type.upper() == 'N':
                         if (abs(r-king_r), abs(c-king_c)) in [(1,2), (2,1)]: return True
                    else:
                        # Sliding
                        dr, dc = king_r - r, king_c - c
                        if dr == 0 or dc == 0 or abs(dr) == abs(dc):
                            step_r = 0 if dr == 0 else (1 if dr > 0 else -1)
                            step_c = 0 if dc == 0 else (1 if dc > 0 else -1)
                            is_diag = (step_r != 0 and step_c != 0)
                            if is_diag and p.type.upper() == 'R': continue
                            if not is_diag and p.type.upper() == 'B': continue
                            
                            curr_r, curr_c = r + step_r, c + step_c
                            path_blocked = False
                            while (curr_r, curr_c) != (king_r, king_c):
                                if self.board[curr_r][curr_c] is not None:
                                    path_blocked = True
                                    break
                                curr_r += step_r
                                curr_c += step_c
                            if not path_blocked: return True
        return False

    def is_checkmate(self, color):
        if not self.is_check(color): return False
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.color == color:
                    if len(self.get_valid_moves(r, c)) > 0:
                        return False
        return True

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]
        
        if captured:
            self.captured_pieces[self.current_player].append(captured)
        
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.pos = (to_row, to_col)
        piece.has_moved = True
        
        if piece.type.upper() == 'K':
            self.king_positions[piece.color] = (to_row, to_col)
        
        # Notasi
        move_notation = f"{piece.get_animal_name()} {chr(from_col + 97)}{8 - from_row} → {chr(to_col + 97)}{8 - to_row}"
        if captured: move_notation += f" ×{captured.get_animal_name()}"
        
        opponent = 'black' if self.current_player == 'white' else 'white'
        is_check = self.is_check(opponent)
        is_mate = self.is_checkmate(opponent)
        
        if is_mate: move_notation += " #"
        elif is_check: move_notation += " +"
            
        self.move_history.append(move_notation)
        self.current_player = opponent
        
        return True, is_mate

    # --- AI LOGIC (FIXED) ---
    def make_computer_move(self):
        """Logika sederhana AI - Return tuple (koordinat_gerakan, is_mate)"""
        moves = self.get_all_valid_moves('black')
        if not moves: 
            return None, False

        values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 100}
        
        best_move = None
        best_score = -1000
        
        random.shuffle(moves) # Randomize agar tidak monoton
        
        for (fr, fc), (tr, tc) in moves:
            score = 0
            target = self.board[tr][tc]
            if target:
                score = values.get(target.type.upper(), 0)
            
            # Bonus posisi tengah
            if 2 <= tr <= 5 and 2 <= tc <= 5:
                score += 0.1
            
            # Sedikit logika defensive (sangat simple) - hindari tempat yg diserang pawn (opsional)
            # score -= 0.05 # Biar AI mau trade

            if score > best_score:
                best_score = score
                best_move = ((fr, fc), (tr, tc))
        
        if best_move:
            (fr, fc), (tr, tc) = best_move
            success, is_mate = self.move_piece(fr, fc, tr, tc)
            return (fr, fc, tr, tc), is_mate # FIX: Return koordinat!
            
        return None, False

    # --- SAVE / LOAD ---
    def to_dict(self):
        board_data = []
        for r in range(8):
            row_data = []
            for c in range(8):
                p = self.board[r][c]
                if p:
                    row_data.append({
                        'type': p.type,
                        'color': p.color,
                        'has_moved': p.has_moved
                    })
                else:
                    row_data.append(None)
            board_data.append(row_data)
            
        return {
            'board': board_data,
            'turn': self.current_player,
            'history': self.move_history,
            'captured_w': [p.type for p in self.captured_pieces['white']],
            'captured_b': [p.type for p in self.captured_pieces['black']],
            'mode': self.game_mode
        }

    def load_from_dict(self, data):
        self.current_player = data['turn']
        self.move_history = data['history']
        self.game_mode = data.get('mode', 'pvp')
        
        for r in range(8):
            for c in range(8):
                p_data = data['board'][r][c]
                if p_data:
                    self.board[r][c] = ChessPiece(p_data['type'], p_data['color'], (r,c), p_data['has_moved'])
                    if p_data['type'].upper() == 'K':
                        self.king_positions[p_data['color']] = (r, c)
                else:
                    self.board[r][c] = None
        
        self.captured_pieces['white'] = [ChessPiece(t, 'black', (0,0)) for t in data['captured_w']]
        self.captured_pieces['black'] = [ChessPiece(t, 'white', (0,0)) for t in data['captured_b']]


# --- UI CLASSES ---

class ChessPieceGraphics(QGraphicsTextItem):
    def __init__(self, piece):
        super().__init__()
        self.piece = piece
        self.setPlainText(piece.get_symbol())
        font = QFont("Segoe UI Emoji", int(LOGICAL_SQUARE_SIZE * 0.7))
        self.setFont(font)
        
        if piece.color == 'white':
            self.setDefaultTextColor(QColor(255, 250, 240)) 
        else:
            self.setDefaultTextColor(QColor(20, 20, 20))
        
        rect = self.boundingRect()
        self.setTransformOriginPoint(rect.width() / 2, rect.height() / 2)
        self.setPos(-rect.width() / 2, -rect.height() / 2)
        self.setZValue(10)

class ChessSquare(QGraphicsRectItem):
    def __init__(self, row, col, board_view):
        super().__init__(0, 0, LOGICAL_SQUARE_SIZE, LOGICAL_SQUARE_SIZE)
        self.row = row
        self.col = col
        self.board_view = board_view
        self.is_light = (row + col) % 2 == 0
        self.piece_graphics = None
        
        if self.is_light: c = QColor(240, 217, 181) 
        else: c = QColor(181, 136, 99)
            
        self.normal_brush = self._create_gradient(c)
        self.selected_brush = QBrush(QColor(255, 255, 50, 180)) 
        self.valid_move_brush = QBrush(QColor(100, 255, 100, 150))
        self.last_move_brush = QBrush(QColor(255, 200, 0, 100))
        
        self.setBrush(self.normal_brush)
        self.setPen(Qt.NoPen)
        self.setPos(col * LOGICAL_SQUARE_SIZE, row * LOGICAL_SQUARE_SIZE)
        self.setAcceptHoverEvents(True)
        
    def _create_gradient(self, color):
        grad = QLinearGradient(0, 0, LOGICAL_SQUARE_SIZE, LOGICAL_SQUARE_SIZE)
        grad.setColorAt(0, color.lighter(105))
        grad.setColorAt(1, color.darker(105))
        return QBrush(grad)

    def set_piece(self, piece):
        if self.piece_graphics:
            if self.piece_graphics.scene():
                self.piece_graphics.scene().removeItem(self.piece_graphics)
            self.piece_graphics = None
            
        if piece:
            self.piece_graphics = ChessPieceGraphics(piece)
            self.piece_graphics.setParentItem(self)
            rect = self.piece_graphics.boundingRect()
            self.piece_graphics.setPos(
                (LOGICAL_SQUARE_SIZE - rect.width()) / 2, 
                (LOGICAL_SQUARE_SIZE - rect.height()) / 2
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.board_view.square_clicked(self.row, self.col)
        
    def highlight(self, mode='normal'):
        if mode == 'selected': self.setBrush(self.selected_brush)
        elif mode == 'valid': self.setBrush(self.valid_move_brush)
        elif mode == 'last': self.setBrush(self.last_move_brush)
        else: self.setBrush(self.normal_brush)

class ChessBoardView(QGraphicsView):
    move_made = Signal(bool) # Bool: is_game_over
    
    def __init__(self, chess_board):
        super().__init__()
        self.chess_board = chess_board
        self.scene = QGraphicsScene(0, 0, BOARD_SIZE, BOARD_SIZE)
        self.setScene(self.scene)
        
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.selected_square = None
        self.valid_moves = []
        self.last_move = None
        self.input_enabled = True
        
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.NoFrame)
        self.setBackgroundBrush(QBrush(QColor(30, 25, 20)))
        
        self._create_board()
        self.update_board()
        
    def _create_board(self):
        for row in range(8):
            for col in range(8):
                sq = ChessSquare(row, col, self)
                self.scene.addItem(sq)
                self.squares[row][col] = sq
                
        font = QFont("Arial", 12, QFont.Bold)
        for i in range(8):
            txt = self.scene.addText(chr(97 + i), font)
            txt.setDefaultTextColor(QColor(200, 200, 200))
            txt.setPos(i * LOGICAL_SQUARE_SIZE + 40, BOARD_SIZE + 5)
            
            txt = self.scene.addText(str(8 - i), font)
            txt.setDefaultTextColor(QColor(200, 200, 200))
            txt.setPos(-25, i * LOGICAL_SQUARE_SIZE + 40)

        self.scene.setSceneRect(-30, -30, BOARD_SIZE + 60, BOARD_SIZE + 60)

    def update_board(self):
        for r in range(8):
            for c in range(8):
                p = self.chess_board.get_piece(r, c)
                self.squares[r][c].set_piece(p)
                
        if self.last_move:
            fr, fc, tr, tc = self.last_move
            self.squares[fr][fc].highlight('last')
            self.squares[tr][tc].highlight('last')

    def square_clicked(self, row, col):
        if not self.input_enabled: return

        if self.chess_board.game_mode == 'pve' and self.chess_board.current_player == 'black':
            return

        if self.selected_square:
            fr, fc = self.selected_square
            if (row, col) in self.valid_moves:
                result, is_mate = self.chess_board.move_piece(fr, fc, row, col)
                self.last_move = (fr, fc, row, col)
                self.update_board()
                self.clear_selection()
                self.move_made.emit(is_mate)
                return
            self.clear_selection()
        
        piece = self.chess_board.get_piece(row, col)
        if piece and piece.color == self.chess_board.current_player:
            self.selected_square = (row, col)
            self.valid_moves = self.chess_board.get_valid_moves(row, col)
            self.squares[row][col].highlight('selected')
            for r, c in self.valid_moves:
                self.squares[r][c].highlight('valid')

    def clear_selection(self):
        if self.selected_square:
            r, c = self.selected_square
            self.squares[r][c].highlight()
        for r, c in self.valid_moves:
            self.squares[r][c].highlight()
        self.selected_square = None
        self.valid_moves = []
        if self.last_move:
            fr, fc, tr, tc = self.last_move
            self.squares[fr][fc].highlight('last')
            self.squares[tr][tc].highlight('last')

    def resizeEvent(self, event):
        self.fitInView(self.scene.sceneRect(), Qt.KeepAspectRatio)
        super().resizeEvent(event)

class InfoPanel(QFrame):
    def __init__(self, title, color_theme):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        self.title_lbl = QLabel(title)
        self.title_lbl.setStyleSheet("font-weight: bold; font-size: 14px; color: #FFF;")
        self.title_lbl.setAlignment(Qt.AlignCenter)
        
        self.content_lbl = QLabel()
        self.content_lbl.setStyleSheet("font-size: 16px; color: #EEE;")
        self.content_lbl.setAlignment(Qt.AlignCenter)
        self.content_lbl.setWordWrap(True)
        
        layout.addWidget(self.title_lbl)
        layout.addWidget(self.content_lbl)
        
        bg = "#4A3B32" if color_theme == "dark" else "#8B7355"
        self.setStyleSheet(f"""
            QFrame {{ background-color: {bg}; border-radius: 8px; border: 1px solid #AAA; }}
        """)
        
    def set_content(self, text):
        self.content_lbl.setText(text)

class MacanChessWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chess_board = ChessBoard()
        
        self.setWindowTitle("Macan Chess - Tiger's Strategy")
        self.setStyleSheet("""
            QMainWindow { background-color: #211e1b; }
            QLabel { color: #f0f0f0; font-family: 'Segoe UI'; }
            QPushButton {
                background-color: #d4af37; color: #211e1b;
                border-radius: 5px; padding: 10px; font-weight: bold; font-size: 14px;
            }
            QPushButton:hover { background-color: #ebd275; }
        """)
        
        self.setup_ui()
        self.ask_game_mode()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # --- LEFT PANEL ---
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        self.captured_white = InfoPanel("White Captured", "light")
        self.captured_white.set_content("-")
        left_layout.addWidget(self.captured_white)
        left_layout.addStretch()
        
        # --- CENTER PANEL ---
        center_panel = QWidget()
        center_layout = QVBoxLayout(center_panel)
        
        title = QLabel("🐯 MACAN CHESS 🐯")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #D4AF37; margin-bottom: 10px;")
        
        self.board_view = ChessBoardView(self.chess_board)
        self.board_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.board_view.move_made.connect(self.on_move_made)
        
        self.status_lbl = QLabel("White's Turn")
        self.status_lbl.setAlignment(Qt.AlignCenter)
        self.status_lbl.setStyleSheet("font-size: 18px; color: #FFF; background: #333; padding: 5px; border-radius: 5px;")
        
        center_layout.addWidget(title, 0)
        center_layout.addWidget(self.board_view, 1)
        center_layout.addWidget(self.status_lbl, 0)
        
        # --- RIGHT PANEL ---
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        self.captured_black = InfoPanel("Black Captured", "dark")
        self.captured_black.set_content("-")
        
        self.history_lbl = QLabel("Move History")
        self.history_lbl.setAlignment(Qt.AlignCenter)
        self.history_box = QLabel()
        self.history_box.setStyleSheet("background: #333; color: #AAA; padding: 10px; border-radius: 5px;")
        self.history_box.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.history_box.setWordWrap(True)
        
        # Controls
        btn_layout = QGridLayout()
        self.btn_save = QPushButton("Save")
        self.btn_load = QPushButton("Load")
        self.btn_new = QPushButton("New Game")
        
        self.btn_save.clicked.connect(self.save_game)
        self.btn_load.clicked.connect(self.load_game)
        self.btn_new.clicked.connect(self.reset_game)
        
        btn_layout.addWidget(self.btn_save, 0, 0)
        btn_layout.addWidget(self.btn_load, 0, 1)
        btn_layout.addWidget(self.btn_new, 1, 0, 1, 2)
        
        right_layout.addWidget(self.captured_black)
        right_layout.addWidget(self.history_lbl)
        right_layout.addWidget(self.history_box, 1)
        right_layout.addLayout(btn_layout)
        
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(center_panel, 6)
        main_layout.addWidget(right_panel, 2)

    def ask_game_mode(self):
        items = ["Player vs Player", "Player vs Computer"]
        item, ok = QInputDialog.getItem(self, "Pilih Mode", 
                                        "Ingin bermain mode apa?", items, 0, False)
        if ok and item:
            if item == "Player vs Computer":
                self.chess_board.game_mode = 'pve'
                self.status_lbl.setText("White's Turn (You)")
            else:
                self.chess_board.game_mode = 'pvp'
                self.status_lbl.setText("White's Turn")
        else:
            self.chess_board.game_mode = 'pvp'

    def on_move_made(self, is_mate):
        self.update_ui()
        
        if is_mate:
            winner = "White" if self.chess_board.current_player == "black" else "Black"
            QMessageBox.information(self, "Game Over", f"Checkmate! {winner} wins!")
            self.board_view.input_enabled = False
            return

        # Cek jika AI perlu jalan (Mode PvE, giliran Hitam)
        if self.chess_board.game_mode == 'pve' and self.chess_board.current_player == 'black':
            self.board_view.input_enabled = False # Kunci input player
            self.status_lbl.setText("Black (Computer) Thinking...")
            QTimer.singleShot(800, self.trigger_ai_move)

    def trigger_ai_move(self):
        # FIX IS HERE: Mengambil tuple koordinat gerakan, bukan object piece
        move_coords, is_mate = self.chess_board.make_computer_move()
        
        if move_coords:
            # Set highlight move terakhir
            self.board_view.last_move = move_coords
            self.board_view.update_board()
            self.update_ui()
            
            if is_mate:
                 QMessageBox.information(self, "Game Over", f"Checkmate! Computer wins!")
            else:
                self.board_view.input_enabled = True # Buka kunci
                self.status_lbl.setText("White's Turn (You)")
        else:
            # Stalemate / Draw situation logic simple
            QMessageBox.information(self, "Game Over", "Stalemate / No moves left!")

    def update_ui(self):
        current = "White" if self.chess_board.current_player == 'white' else "Black"
        if self.chess_board.game_mode == 'pve':
            label = f"{current}'s Turn" + (" (You)" if current == 'White' else " (Computer)")
        else:
            label = f"{current}'s Turn"
            
        if self.chess_board.is_check(self.chess_board.current_player):
            label += " - CHECK!"
        self.status_lbl.setText(label)
        
        w_caps = " ".join([p.get_symbol() for p in self.chess_board.captured_pieces['white']])
        b_caps = " ".join([p.get_symbol() for p in self.chess_board.captured_pieces['black']])
        self.captured_white.set_content(w_caps if w_caps else "-")
        self.captured_black.set_content(b_caps if b_caps else "-")
        
        moves = self.chess_board.move_history[-10:]
        hist_text = "\n".join(moves)
        self.history_box.setText(hist_text)

    def save_game(self):
        data = self.chess_board.to_dict()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Game", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(data, f, indent=4)
                QMessageBox.information(self, "Success", "Game saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save: {str(e)}")

    def load_game(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Game", "", "JSON Files (*.json)")
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                self.chess_board.load_from_dict(data)
                self.board_view.update_board()
                self.board_view.last_move = None
                self.board_view.clear_selection()
                self.update_ui()
                QMessageBox.information(self, "Success", "Game loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not load: {str(e)}")

    def reset_game(self):
        reply = QMessageBox.question(self, "Reset", "Start new game?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.chess_board.init_board()
            self.board_view.update_board()
            self.board_view.last_move = None
            self.board_view.clear_selection()
            self.board_view.input_enabled = True
            self.ask_game_mode()
            self.update_ui()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MacanChessWindow()
    window.showMaximized()
    sys.exit(app.exec())