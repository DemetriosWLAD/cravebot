#!/usr/bin/env python3
"""
Простое развертывание бота через веб-интерфейс
Создает сервер для скачивания файлов
"""

from flask import Flask, send_file, render_template_string
import os
import zipfile
from pathlib import Path

app = Flask(__name__)

# HTML шаблон для интерфейса
DOWNLOAD_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CraveBreaker - Скачать файлы развертывания</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; background: #f5f5f5; }
        .container { background: white; padding: 40px; border-radius: 15px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; margin-bottom: 30px; }
        .download-btn { 
            display: inline-block; 
            background: #3498db; 
            color: white; 
            padding: 15px 30px; 
            text-decoration: none; 
            border-radius: 8px; 
            font-size: 18px; 
            margin: 10px;
            transition: background 0.3s;
        }
        .download-btn:hover { background: #2980b9; }
        .success { background: #d4edda; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        .instruction { background: #fff3cd; padding: 20px; border-radius: 8px; margin: 20px 0; text-align: left; }
        .file-list { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; text-align: left; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 CraveBreaker Bot - Готов к развертыванию!</h1>
        
        <div class="success">
            ✅ Все файлы подготовлены автоматически!<br>
            Скачайте архив и разверните на любой облачной платформе
        </div>

        <a href="/download-zip" class="download-btn">📦 Скачать CraveBreaker_Deploy.zip</a>
        
        <div class="file-list">
            <h3>📁 Что включено в архив:</h3>
            <ul>
                <li><strong>app.py</strong> - главный файл запуска для облачных платформ</li>
                <li><strong>simple_bot.py</strong> - Telegram бот с 125 техниками поддержки</li>
                <li><strong>database.py</strong> - система хранения данных пользователей</li>
                <li><strong>interventions.py</strong> - 25 дыхательных + 50 медитативных + 50 игровых техник</li>
                <li><strong>utils.py, config.py</strong> - вспомогательные модули</li>
                <li><strong>requirements.txt</strong> - список необходимых библиотек</li>
                <li><strong>Dockerfile, railway.json</strong> - конфигурации для развертывания</li>
                <li><strong>README.md</strong> - подробные инструкции по развертыванию</li>
            </ul>
        </div>

        <div class="instruction">
            <h3>🎯 Быстрое развертывание:</h3>
            <p><strong>1. Render.com (рекомендуется):</strong></p>
            <ul>
                <li>Перейдите на <a href="https://render.com" target="_blank">render.com</a></li>
                <li>"Get Started for Free" → войдите через GitHub</li>
                <li>Создайте репозиторий на GitHub и загрузите содержимое архива</li>
                <li>"New +" → "Web Service" → выберите репозиторий</li>
                <li>Start Command: <code>python app.py</code></li>
                <li>Environment Variables: <code>TELEGRAM_BOT_TOKEN</code> = ваш токен от @BotFather</li>
                <li>"Create Web Service"</li>
            </ul>
            
            <p><strong>2. Railway.app:</strong></p>
            <ul>
                <li><a href="https://railway.app" target="_blank">railway.app</a> → "Login with GitHub"</li>
                <li>"New Project" → "Deploy from GitHub"</li>
                <li>Environment Variables: <code>TELEGRAM_BOT_TOKEN</code></li>
            </ul>
        </div>

        <div class="success">
            🎉 Результат: Бот будет работать 24/7 в облаке!<br>
            Все техники поддержки, персональный коучинг и статистика включены.
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DOWNLOAD_TEMPLATE)

@app.route('/download-zip')
def download_zip():
    """Скачивание готового архива"""
    zip_path = "CraveBreaker_Deploy.zip"
    
    if os.path.exists(zip_path):
        return send_file(zip_path, as_attachment=True, download_name="CraveBreaker_Deploy.zip")
    else:
        return "Архив не найден. Перезапустите проект для создания файлов.", 404

if __name__ == '__main__':
    print("🚀 Запуск сервера для скачивания файлов...")
    print("📂 Откройте в браузере: http://localhost:5000")
    print("📦 Или перейдите по ссылке в правом верхнем углу Replit")
    app.run(host='0.0.0.0', port=5000, debug=True)