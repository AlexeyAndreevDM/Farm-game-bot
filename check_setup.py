#!/usr/bin/env python3
"""
Скрипт для проверки корректности настройки бота.
Проверяет наличие всех необходимых файлов и зависимостей.
"""
import os
import sys

def check_files():
    """Проверка наличия необходимых файлов."""
    required_files = [
        '.env',
        'requirements.txt',
        'farm_game_bot.py',
        'config/settings.py',
        'database/db_manager.py',
        'handlers/start.py',
        'utils/keyboards.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Отсутствуют файлы:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    print("✅ Все необходимые файлы на месте")
    return True

def check_env():
    """Проверка наличия токена в .env."""
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден")
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'BOT_TOKEN=' not in content:
            print("❌ BOT_TOKEN не найден в .env")
            return False
        if 'BOT_TOKEN=' in content and content.split('BOT_TOKEN=')[1].strip() == '':
            print("⚠️  BOT_TOKEN пустой в .env")
            return False
    
    print("✅ Файл .env настроен")
    return True

def check_dependencies():
    """Проверка установленных зависимостей."""
    try:
        import telebot
        print("✅ pyTelegramBotAPI установлен")
    except ImportError:
        print("❌ pyTelegramBotAPI не установлен. Выполните: pip install -r requirements.txt")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv установлен")
    except ImportError:
        print("❌ python-dotenv не установлен. Выполните: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Основная функция проверки."""
    print("🔍 Проверка конфигурации Farm Game Bot...\n")
    
    files_ok = check_files()
    print()
    
    env_ok = check_env()
    print()
    
    deps_ok = check_dependencies()
    print()
    
    if files_ok and env_ok and deps_ok:
        print("✅ Все проверки пройдены! Бот готов к запуску.")
        print("\nДля запуска бота выполните:")
        print("  python3 farm_game_bot.py")
        return 0
    else:
        print("❌ Обнаружены проблемы. Исправьте их перед запуском.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
