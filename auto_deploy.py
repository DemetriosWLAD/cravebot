#!/usr/bin/env python3
"""
Автоматическое развертывание CraveBreaker бота
Создает готовый к развертыванию пакет без участия пользователя
"""

import os
import zipfile
import shutil
from pathlib import Path

def create_deployment_package():
    """Создает готовый пакет для развертывания"""
    
    # Создаем папку для развертывания
    deploy_dir = Path("CraveBreaker_Deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Копируем все необходимые файлы
    files_to_copy = [
        "app.py",
        "simple_bot.py", 
        "database.py",
        "interventions.py",
        "utils.py",
        "config.py",
        "requirements.txt",
        "Dockerfile",
        "railway.json"
    ]
    
    for file_name in files_to_copy:
        if Path(file_name).exists():
            shutil.copy2(file_name, deploy_dir / file_name)
    
    # Создаем README с инструкциями
    readme_content = """# CraveBreaker Telegram Bot - Готов к развертыванию

## 🚀 МГНОВЕННОЕ РАЗВЕРТЫВАНИЕ

### Render.com (рекомендуется - проще всего):
1. Перейдите на https://render.com
2. "Get Started for Free" → войдите через GitHub  
3. "New +" → "Web Service"
4. "Connect a repository" → загрузите эти файлы в новый репозиторий
5. Start Command: `python app.py`
6. Environment Variables: `TELEGRAM_BOT_TOKEN` = ваш_токен
7. "Create Web Service"

### Railway.app:
1. https://railway.app → "Login with GitHub"
2. "New Project" → "Deploy from GitHub" 
3. Загрузите файлы в репозиторий
4. Environment Variables: `TELEGRAM_BOT_TOKEN` = ваш_токен

### Koyeb.com:
1. https://app.koyeb.com/auth/signup
2. "Login with GitHub" 
3. "Create Web Service" → "GitHub"
4. Environment Variables: `TELEGRAM_BOT_TOKEN` = ваш_токен

## ✅ ВСЕ ГОТОВО!
Все файлы настроены для автоматического запуска.
Просто загрузите их на любую платформу - бот заработает сам.

## 🎯 ФУНКЦИИ БОТА:
- 25 дыхательных техник
- 50 медитативных практик  
- 50 отвлекающих игр
- Персональный коучинг
- Статистика прогресса
- Работа 24/7 без вашего компьютера
"""
    
    with open(deploy_dir / "README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    # Создаем архив
    zip_path = "CraveBreaker_Deploy.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(deploy_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(deploy_dir)
                zipf.write(file_path, arc_path)
    
    print("✅ ГОТОВО! Создан архив CraveBreaker_Deploy.zip")
    print("📁 Все файлы скопированы в папку CraveBreaker_Deploy/")
    print("🚀 Загрузите содержимое папки на любую облачную платформу")
    
    return deploy_dir, zip_path

if __name__ == "__main__":
    create_deployment_package()