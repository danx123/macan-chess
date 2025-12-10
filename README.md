# 🐯 Macan Chess

A professional, tiger-themed chess application built with PySide6, featuring elegant jungle animal pieces and a sophisticated modern interface.

![Macan Chess](https://img.shields.io/badge/version-1.0-blue) ![Python](https://img.shields.io/badge/python-3.8+-green) ![License](https://img.shields.io/badge/license-MIT-orange)

## ✨ Features

### 🎮 Core Gameplay
- **Full chess engine** with valid move calculation
- **Check and checkmate detection**
- **Move validation** to prevent illegal moves
- **Turn-based gameplay** with automatic player switching

### 🎨 Visual Design
- **Tiger-themed pieces**: Each chess piece represented by elegant jungle animals
  - ♔ King → **Lion** (Pride leader)
  - ♕ Queen → **Panther** (Stealthy hunter)
  - ♖ Rook → **Boar** (Strong defender)
  - ♗ Bishop → **Tiger** (Swift striker)
  - ♘ Knight → **Cheetah** (Quick mover)
  - ♙ Pawn → **Rabbit** (Brave foot soldier)

- **Sophisticated color palette**:
  - Polished wood-textured board (light: #F0D9B5, dark: #B58863)
  - Gold accents and gradients
  - Earth tones throughout the interface
  - High contrast for readability

- **Visual effects**:
  - Smooth piece animations
  - Hover effects on pieces and squares
  - Highlighted valid moves
  - Last move indication with golden glow
  - Check/checkmate visual alerts

### 🕐 Game Features
- **Player timers**: 10-minute countdown for each player
- **Move history panel**: Complete game notation with animal names
- **Captured pieces display**: Visual tracker for both players
- **Status indicator**: Current player, check, and checkmate alerts

### 💾 Game Management
- **New Game**: Start fresh at any time
- **Save/Load**: Persistent game storage in `%LOCALAPPDATA%/MacanChess/`
- **Auto-save location**: Games saved with timestamps
- **Move history export**: JSON format for game analysis

### 🎯 User Interface
- **Professional desktop layout**: Optimized for 1400×900 resolution
- **Intuitive controls**: Click to select, click to move
- **Keyboard shortcuts**: 
  - `Ctrl+N` - New Game
  - `Ctrl+S` - Save Game
  - `Ctrl+O` - Load Game
  - `Ctrl+Q` - Exit
- **Menu system**: Complete game, help, and settings menus
- **About dialog**: Game information and piece guide
- **Rules reference**: Built-in chess rules explanation

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum
- **Display**: 1024×768 minimum (1400×900 recommended)

### Dependencies
```txt
PySide6>=6.5.0
```

## 🚀 Installation

### Method 1: From Source

1. **Clone the repository**:
```bash
git clone https://github.com/danx123/macan-chess.git
cd macan-chess
```

2. **Create virtual environment** (recommended):
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
python macan_chess.py
```

### Method 2: Standalone Executable

Download the pre-built executable from the [Releases](https://github.com/danx123/macan-chess/releases) page.

## 🎮 How to Play

### Starting a Game
1. Launch Macan Chess
2. White (Lion's Pride) plays first
3. Click on a piece to select it
4. Valid moves will be highlighted in green
5. Click on a highlighted square to move

### Game Controls
- **Select piece**: Left-click on your piece
- **Move piece**: Click on valid move square
- **Deselect**: Click on empty square or opponent's piece
- **New game**: Click "🔄 New Game" or `Ctrl+N`
- **Save game**: Click "💾 Save" or `Ctrl+S`
- **Load game**: Click "📂 Load" or `Ctrl+O`

### Understanding the Interface

**Left Panel**:
- White player timer
- White's captured pieces

**Center**:
- 8×8 chessboard with coordinate labels
- Current game status
- Player turn indicator

**Right Panel**:
- Black player timer
- Black's captured pieces
- Complete move history
- Control buttons

## 🏗️ Project Structure

```
macan-chess/
│
├── macan_chess.py          # Main application file
├── README.md               # This file
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
│
└── (auto-created at runtime)
    └── %LOCALAPPDATA%/MacanChess/  # Save game directory
        └── macan_chess_YYYYMMDD_HHMMSS.json
```

## 🎨 Design Philosophy

Macan Chess combines the strategic depth of chess with the majesty of jungle wildlife:

- **Professional aesthetics**: Clean, modern interface suitable for serious play
- **Thematic consistency**: Every element reinforces the jungle/tiger theme
- **User-friendly**: Intuitive controls, clear visual feedback
- **Performance**: Smooth animations, responsive UI
- **Accessibility**: High contrast, readable fonts, clear status indicators

## 📸 Screenshot
<img width="1365" height="767" alt="Screenshot 2025-12-10 113721" src="https://github.com/user-attachments/assets/4fbe5cb8-f4ac-4d84-b03c-2a3754b19be6" />


## 🔧 Technical Details

### Architecture
- **MVC pattern**: Separated game logic, UI, and data management
- **Object-oriented design**: Modular, maintainable code structure
- **Event-driven**: Qt signal/slot mechanism for responsive UI

### Key Components
- `ChessBoard`: Core game logic and move validation
- `ChessPiece`: Piece data and behavior
- `ChessBoardView`: Graphical board representation
- `ChessSquare`: Individual square with hover/click handling
- `PlayerTimer`: Countdown timer with visual feedback
- `MoveHistoryPanel`: Game notation display
- `MacanChessWindow`: Main application window

### Game Logic Features
- Valid move calculation for all piece types
- Check detection algorithm
- Checkmate verification
- Move history tracking
- Captured piece management


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup
```bash
# Clone your fork
git clone https://github.com/danx123/macan-chess.git

# Install development dependencies
pip install -r requirements.txt
pip install black pylint pytest  # Optional: code quality tools

# Run the application
python macan_chess.py
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👏 Acknowledgments

- Chess piece Unicode symbols from Unicode Standard
- PySide6 (Qt for Python) framework
- Inspired by classic chess applications and modern UI design principles


---

## 🎯 Quick Start Commands

```bash
# Install
pip install PySide6

# Run
python macan_chess.py

# Save location
%LOCALAPPDATA%\MacanChess\
# (Windows: C:\Users\YourName\AppData\Local\MacanChess\)
```

---

**Made with ❤️ and 🐯 by chess enthusiasts**

*May the strongest predator win!*
