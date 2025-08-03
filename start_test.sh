#!/bin/bash

echo "🧪 CraveBreaker - Запуск тестирования"
echo "=================================="

# Проверяем наличие токена тестового бота
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo ""
    echo "❌ ОШИБКА: Не установлен токен тестового бота"
    echo ""
    echo "📝 Пожалуйста, выполните:"
    echo "export TELEGRAM_BOT_TOKEN=ваш_токен_тестового_бота"
    echo "./start_test.sh"
    echo ""
    echo "💡 Или установите токен прямо сейчас:"
    read -p "Введите токен тестового бота: " token
    export TELEGRAM_BOT_TOKEN=$token
fi

echo ""
echo "✅ Токен настроен: ${TELEGRAM_BOT_TOKEN:0:10}..."
echo ""
echo "🚀 Запускаем тестирование улучшений..."
echo ""

# Запускаем тестовую версию
python test_with_bot.py