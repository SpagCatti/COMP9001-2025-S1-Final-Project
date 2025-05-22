# JapaneseStudy 📚

A comprehensive command-line application for studying Japanese vocabulary and characters, featuring JLPT-level quizzes, progress tracking, and mistake review functionality.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)

## Features ✨

### 🎯 **JLPT Vocabulary Quizzes**
- Support for all JLPT levels (N5-N1)
- Multiple choice questions with randomized options
- Progress tracking for mastered vocabulary
- Real-time feedback and scoring

### 📝 **Character Recognition Quiz**
- Test your knowledge of Japanese characters
- Randomized character selection
- Immediate feedback on answers

### 📖 **Study Materials**
- Browse vocabulary by JLPT level
- View character lists with readings
- Organized display with pronunciation guides

### 🔄 **Mistake Management**
- Automatic tracking of incorrect answers
- Dedicated mistake practice sessions
- Review system to clear mistakes from your list
- Persistent mistake storage across sessions

### 📊 **Progress Tracking**
- Track mastered vocabulary for each JLPT level
- Visual progress indicators in menus
- Persistent progress storage

## Installation 🚀

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses only Python standard library)

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/JapaneseStudy.git
cd JapaneseStudy
```

2. Create the data directory and CSV files:
```bash
mkdir data
```

3. Add your vocabulary and character data files (see [Data Format](#data-format) section)

4. Run the application:
```bash
python main.py
```

## Data Format 📋

### JLPT Vocabulary Files
Create CSV files in the `data/` directory with the following format:

**File names:** `jlpt_n5.csv`, `jlpt_n4.csv`, `jlpt_n3.csv`, `jlpt_n2.csv`, `jlpt_n1.csv`

**Format:**
```csv
Kanji,Kana,Meaning
挨拶,あいさつ,greeting
学校,がっこう,school
```

### Character File
**File name:** `data/characters.csv`

**Format:**
```csv
Character,Correct Answer
あ,a
か,ka
```

## Project Structure 📁

```
JapaneseStudy/
├── main.py                 # Main application entry point
├── ui_handler.py          # User interface and menu handling
├── quiz_manager.py        # Quiz logic and question generation
├── data_loader.py         # Data loading and CSV operations
├── progress_manager.py    # User progress tracking
├── mistake_tracker.py     # Mistake logging and review
├── data/                  # Data directory
│   ├── jlpt_n5.csv       # N5 vocabulary
│   ├── jlpt_n4.csv       # N4 vocabulary
│   ├── jlpt_n3.csv       # N3 vocabulary
│   ├── jlpt_n2.csv       # N2 vocabulary
│   ├── jlpt_n1.csv       # N1 vocabulary
│   ├── characters.csv     # Character data
│   ├── user_progress.csv  # User progress (auto-generated)
│   └── mistakes.csv       # Mistake tracking (auto-generated)
└── README.md
```

## Usage Guide 🎮

### Main Menu Options

1. **JLPT Quiz** - Take vocabulary quizzes by level
2. **Character Quiz** - Practice Japanese character recognition
3. **Learn the Vocabs** - Browse vocabulary by JLPT level
4. **Learn the Characters** - View all available characters
5. **Mistake Practice** - Review and clear your mistakes
6. **Reset** - Clear all progress and mistakes
7. **Quit** - Exit the application

### Quiz Features

- **Question Format**: Displays Kana with Kanji in parentheses (e.g., あいさつ (挨拶))
- **Answer Options**: Multiple choice (A, B, C, D)
- **Quit Option**: Press 'Q' to quit mid-quiz (progress won't be saved)
- **Immediate Review**: Option to review mistakes right after each quiz

### Progress System

- Correctly answered vocabulary is automatically marked as "mastered"
- Progress is displayed as "X/Y mastered!" in the JLPT quiz menu
- Progress persists between sessions
- Duplicate answers won't inflate your progress count

## Technical Details ⚙️

### Dependencies
- `csv` - CSV file handling
- `random` - Question randomization
- `datetime` - Timestamp tracking
- `os` - File system operations
- `typing` - Type hints for better code documentation

### Data Storage
- **CSV Format**: All data stored in human-readable CSV files
- **Unicode Support**: Full UTF-8 encoding for Japanese characters
- **Automatic File Creation**: Progress and mistake files created automatically
- **Error Handling**: Graceful handling of missing or corrupted files

### Key Features
- **Duplicate Prevention**: Progress system prevents counting the same vocabulary multiple times
- **Mistake Tracking**: Persistent mistake storage with count and timestamp
- **Safe Sampling**: Handles cases where vocabulary lists have fewer than 10 items
- **Input Validation**: Case-insensitive input handling

## Contributing 🤝

Contributions are welcome! Here are some ways you can help:

1. **Add Vocabulary Data**: Contribute comprehensive JLPT vocabulary lists
2. **Bug Reports**: Report any issues you encounter
3. **Feature Requests**: Suggest new features or improvements
4. **Code Improvements**: Submit pull requests for bug fixes or enhancements

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

## Troubleshooting 🔧

### Common Issues

**"Task failed. jlpt_n5.csv cannot be found"**
- Ensure you have created the `data/` directory
- Add the required CSV files with proper formatting

**"No vocabulary data found for N5!"**
- Check that your CSV files have the correct column headers
- Verify the file encoding is UTF-8

**Progress not saving**
- Ensure the application has write permissions in the `data/` directory
- Check that the CSV files aren't opened in another application

## Acknowledgments 🙏

- Inspired by the need to study for my upcoming JLPT test in a month...

## Future Enhancements 🚀

- [ ] Web-based interface
- [ ] Audio pronunciation support
- [ ] Spaced repetition algorithm
- [ ] Export/import functionality
- [ ] Study statistics and analytics
- [ ] Configurable quiz settings

---

**Happy studying! 頑張って！** 🇯🇵
