# Phonetic Translator

Translate text between languages via phonetic transcription (IPA).

## Features

- 🌍 **18+ Languages**: English, Spanish, French, German, Italian, Portuguese, Dutch, Russian, Chinese, Japanese, Korean, Arabic, Hindi, Turkish, Polish, Swedish, Vietnamese, Thai
- 🎯 **Real Libraries**: Uses `epitran`, `panphon`, and `g2p_en` for production-quality results
- 🚀 **Multiple Interfaces**: CLI, Python API, FastAPI server
- 🐳 **Docker Ready**: Deploy anywhere with Docker
- 🧪 **Fully Tested**: 140+ tests with pytest

## Installation

```bash
# Clone
git clone https://github.com/yourname/phonetic-translator.git
cd phonetic-translator

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install
pip install -r requirements.txt
pip install -e .
