#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Конфигурация для CraveBreaker бота
"""

import os
from typing import Dict, Any

class Config:
    """Класс конфигурации бота"""
    
    def __init__(self):
        # Основные настройки
        self.BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
        self.DATABASE_PATH = os.getenv("DATABASE_PATH", "cravebreaker.db")
        
        # Настройки интервенций
        self.DEFAULT_BREATHING_DURATION = 60  # секунды
        self.MIN_INTERVENTION_INTERVAL = 5    # минимальный интервал между интервенциями в минутах
        self.MAX_DAILY_INTERVENTIONS = 50     # максимальное количество интервенций в день
        
        # Настройки статистики
        self.STATS_RETENTION_DAYS = 365       # сколько дней хранить статистику
        self.CLEANUP_INTERVAL_DAYS = 30       # как часто чистить старые данные
        
        # Настройки пользователей
        self.MAX_TRIGGERS_PER_USER = 10       # максимальное количество триггеров на пользователя
        self.MAX_TRIGGER_NAME_LENGTH = 50     # максимальная длина названия триггера
        
        # Настройки безопасности
        self.RATE_LIMIT_REQUESTS = 100        # максимальное количество запросов в час от пользователя
        self.MAX_MESSAGE_LENGTH = 1000        # максимальная длина сообщения
        
        # Настройки разработки
        self.DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        
        # Эмодзи для интерфейса
        self.EMOJIS = {
            'emergency': '🆘',
            'trigger': '🔥', 
            'stats': '📊',
            'about': '📖',
            'success': '✅',
            'failure': '❌',
            'breathing': '🫁',
            'coaching': '🤔',
            'game': '🎮',
            'menu': '🏠',
            'back': '🔙',
            'trophy': '🏆',
            'star': '⭐',
            'fire': '🔥',
            'heart': '❤️',
            'muscle': '💪',
            'brain': '🧠'
        }
        
        # Сообщения об ошибках
        self.ERROR_MESSAGES = {
            'bot_token_missing': "❌ Токен бота не найден! Установите переменную TELEGRAM_BOT_TOKEN",
            'database_error': "❌ Ошибка базы данных. Попробуйте позже.",
            'rate_limit': "⏰ Слишком много запросов. Подождите немного.",
            'invalid_trigger': "❌ Некорректное название триггера. Используйте 2-50 символов.",
            'max_triggers': f"❌ Максимальное количество триггеров: {MAX_TRIGGERS_PER_USER}",
            'generic_error': "❌ Произошла ошибка. Попробуйте /start для перезапуска."
        }
        
        # Мотивационные сообщения
        self.MOTIVATIONAL_MESSAGES = {
            'first_success': "🎉 Ваша первая победа! Это начало больших изменений!",
            'streak_3': "🔥 3 успеха подряд! Вы в ударе!",
            'streak_7': "⭐ Неделя побед! Невероятный самоконтроль!",
            'streak_30': "🏆 Месяц успехов! Вы достигли мастерства!",
            'comeback': "💪 Отличное возвращение после неудачи!",
            'milestone_10': "🎯 10 успешных интервенций! Прогресс впечатляет!",
            'milestone_50': "💎 50 побед! Вы эксперт самоконтроля!",
            'milestone_100': "👑 100 успехов! Легендарный уровень дисциплины!"
        }
    
    def get_bot_info(self) -> Dict[str, Any]:
        """Получить информацию о настройках бота"""
        return {
            'version': '1.0.0',
            'name': 'CraveBreaker',
            'description': 'AI-бот для борьбы с навязчивыми привычками',
            'features': [
                'Экстренная помощь при импульсах',
                'Дыхательные техники', 
                'Коучинговые вопросы',
                'Отвлекающие мини-игры',
                'Отслеживание прогресса',
                'Управление триггерами'
            ],
            'supported_languages': ['ru'],
            'max_users': 'unlimited',
            'database': 'SQLite3'
        }
    
    def validate_config(self) -> bool:
        """Проверка корректности конфигурации"""
        if self.BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print(self.ERROR_MESSAGES['bot_token_missing'])
            return False
        
        if self.DEFAULT_BREATHING_DURATION < 30:
            print("❌ Слишком короткая длительность дыхательного упражнения")
            return False
            
        if self.MAX_TRIGGERS_PER_USER < 1:
            print("❌ Некорректное максимальное количество триггеров")
            return False
            
        return True
    
    def get_webhook_config(self) -> Dict[str, Any]:
        """Конфигурация для webhook (если потребуется)"""
        return {
            'webhook_url': os.getenv("WEBHOOK_URL", ""),
            'webhook_path': os.getenv("WEBHOOK_PATH", "/webhook"),
            'webhook_port': int(os.getenv("WEBHOOK_PORT", "8443")),
            'use_webhook': os.getenv("USE_WEBHOOK", "false").lower() == "true"
        }
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Конфигурация логирования"""
        return {
            'level': self.LOG_LEVEL,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'file': os.getenv("LOG_FILE", "cravebreaker.log") if not self.DEBUG_MODE else None,
            'max_size': int(os.getenv("LOG_MAX_SIZE", "10485760")),  # 10MB
            'backup_count': int(os.getenv("LOG_BACKUP_COUNT", "5"))
        }
