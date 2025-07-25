#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Обработчики сообщений и callback'ов для CraveBreaker бота
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from interventions import InterventionManager
from utils import MessageTemplates
import asyncio
import random

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self, database: Database):
        self.db = database
        self.interventions = InterventionManager()
        self.templates = MessageTemplates()
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        username = update.effective_user.username or "пользователь"
        
        # Проверяем, есть ли пользователь в базе
        user_exists = await self.db.user_exists(user_id)
        
        if not user_exists:
            # Новый пользователь - показываем онбординг
            await self.db.create_user(user_id, username)
            await self.show_onboarding(update, context)
        else:
            # Существующий пользователь - показываем главное меню
            await self.show_main_menu(update, context)
    
    async def show_onboarding(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ онбординга для новых пользователей"""
        welcome_text = self.templates.get_welcome_message()
        
        keyboard = [
            [InlineKeyboardButton("🚀 Начать использование", callback_data="onboarding_complete")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ главного меню"""
        menu_text = self.templates.get_main_menu_text()
        
        keyboard = [
            [InlineKeyboardButton("🆘 Срочная помощь", callback_data="emergency_help")],
            [InlineKeyboardButton("🔥 Новый триггер", callback_data="new_trigger")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="show_stats")],
            [InlineKeyboardButton("📖 О CraveBreaker", callback_data="about")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(menu_text, reply_markup=reply_markup)
        else:
            await update.callback_query.edit_message_text(menu_text, reply_markup=reply_markup)
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик callback запросов от inline кнопок"""
        query = update.callback_query
        await query.answer()
        
        user_id = update.effective_user.id
        data = query.data
        
        logger.info(f"Получен callback: {data} от пользователя {user_id}")
        
        # Маршрутизация callback'ов
        if data == "onboarding_complete":
            await self.show_main_menu(update, context)
            
        elif data == "emergency_help":
            await self.start_emergency_intervention(update, context)
            
        elif data == "new_trigger":
            await self.show_add_trigger(update, context)
            
        elif data == "show_stats":
            await self.show_stats(update, context)
            
        elif data == "about":
            await self.show_about(update, context)
            
        elif data == "back_to_menu":
            await self.show_main_menu(update, context)
            
        elif data.startswith("intervention_"):
            await self.handle_intervention_callback(update, context, data)
            
        elif data.startswith("trigger_"):
            await self.handle_trigger_callback(update, context, data)
            
        elif data.startswith("outcome_"):
            await self.handle_outcome_callback(update, context, data)
    
    async def start_emergency_intervention(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Запуск экстренной помощи"""
        user_id = update.effective_user.id
        
        # Записываем событие обращения за помощью
        await self.db.log_help_request(user_id)
        
        text = "🆘 **Экстренная помощь активирована!**\n\nВыберите тип поддержки:"
        
        keyboard = [
            [InlineKeyboardButton("🫁 Дыхательная техника", callback_data="intervention_breathing")],
            [InlineKeyboardButton("🤔 Коучинговый вопрос", callback_data="intervention_coaching")],
            [InlineKeyboardButton("🎮 Отвлекающая игра", callback_data="intervention_game")],
            [InlineKeyboardButton("🔙 Назад в меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def handle_intervention_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
        """Обработка выбора типа интервенции"""
        query = update.callback_query
        intervention_type = callback_data.replace("intervention_", "")
        
        if intervention_type == "breathing":
            await self.start_breathing_exercise(update, context)
        elif intervention_type == "coaching":
            await self.show_coaching_question(update, context)
        elif intervention_type == "game":
            await self.start_mini_game(update, context)
    
    async def start_breathing_exercise(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Запуск дыхательного упражнения"""
        query = update.callback_query
        
        exercise = self.interventions.get_breathing_exercise()
        
        text = f"🫁 **Дыхательное упражнение**\n\n{exercise['instruction']}\n\n_Следуйте инструкциям и дышите спокойно..._"
        
        keyboard = [
            [InlineKeyboardButton("✅ Упражнение завершено", callback_data="outcome_success")],
            [InlineKeyboardButton("❌ Не помогло", callback_data="outcome_failed")],
            [InlineKeyboardButton("🔙 Назад", callback_data="emergency_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
        
        # Запускаем таймер дыхательного упражнения
        await self.run_breathing_timer(update, context, exercise['duration'])
    
    async def run_breathing_timer(self, update: Update, context: ContextTypes.DEFAULT_TYPE, duration: int):
        """Таймер для дыхательного упражнения"""
        phases = ["Вдох... 💨", "Задержка... ⏸️", "Выдох... 🌬️", "Пауза... ⏸️"]
        
        for i in range(duration // 4):  # Каждый цикл 16 секунд
            for phase in phases:
                if i == 0:  # Только в первый раз показываем фазы
                    try:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=f"🫁 {phase}"
                        )
                        await asyncio.sleep(4)
                    except:
                        break
    
    async def show_coaching_question(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ коучингового вопроса"""
        query = update.callback_query
        
        question = self.interventions.get_coaching_question()
        
        text = f"🤔 **Коучинговый вопрос**\n\n{question}\n\n_Подумайте над этим вопросом 1-2 минуты..._"
        
        keyboard = [
            [InlineKeyboardButton("💡 Это помогло", callback_data="outcome_success")],
            [InlineKeyboardButton("❌ Не подходит", callback_data="outcome_failed")],
            [InlineKeyboardButton("🔄 Другой вопрос", callback_data="intervention_coaching")],
            [InlineKeyboardButton("🔙 Назад", callback_data="emergency_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def start_mini_game(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Запуск мини-игры для отвлечения"""
        query = update.callback_query
        
        game = self.interventions.get_mini_game()
        
        text = f"🎮 **{game['name']}**\n\n{game['description']}\n\n{game['task']}"
        
        keyboard = [
            [InlineKeyboardButton("🎯 Игра завершена", callback_data="outcome_success")],
            [InlineKeyboardButton("😔 Не отвлекло", callback_data="outcome_failed")],
            [InlineKeyboardButton("🎲 Другая игра", callback_data="intervention_game")],
            [InlineKeyboardButton("🔙 Назад", callback_data="emergency_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def handle_outcome_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
        """Обработка результата интервенции"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        outcome = callback_data.replace("outcome_", "")
        success = outcome == "success"
        
        # Записываем результат в базу данных
        await self.db.log_intervention_outcome(user_id, success)
        
        if success:
            text = "🎉 **Отлично!**\n\nВы справились с импульсом! Это большая победа.\n\n📈 Ваш прогресс записан."
        else:
            text = "😔 **Ничего страшного!**\n\nБорьба с привычками - это процесс. Попробуйте другой метод или обратитесь за помощью снова.\n\n📊 Эта попытка тоже засчитана."
        
        keyboard = [
            [InlineKeyboardButton("🆘 Попробовать снова", callback_data="emergency_help")],
            [InlineKeyboardButton("📊 Моя статистика", callback_data="show_stats")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_add_trigger(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ интерфейса добавления нового триггера"""
        query = update.callback_query
        
        text = "🔥 **Добавление нового триггера**\n\nВыберите тип привычки, с которой хотите бороться:"
        
        keyboard = [
            [InlineKeyboardButton("🍭 Сладкое", callback_data="trigger_sweet")],
            [InlineKeyboardButton("🚬 Курение", callback_data="trigger_smoking")],
            [InlineKeyboardButton("📱 Смартфон", callback_data="trigger_phone")],
            [InlineKeyboardButton("🍷 Алкоголь", callback_data="trigger_alcohol")],
            [InlineKeyboardButton("😴 Прокрастинация", callback_data="trigger_procrastination")],
            [InlineKeyboardButton("➕ Другое", callback_data="trigger_custom")],
            [InlineKeyboardButton("🔙 Назад", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def handle_trigger_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback_data: str):
        """Обработка выбора триггера"""
        query = update.callback_query
        user_id = update.effective_user.id
        
        trigger_type = callback_data.replace("trigger_", "")
        trigger_names = {
            "sweet": "Сладкое",
            "smoking": "Курение", 
            "phone": "Смартфон",
            "alcohol": "Алкоголь",
            "procrastination": "Прокрастинация"
        }
        
        if trigger_type in trigger_names:
            await self.db.add_user_trigger(user_id, trigger_names[trigger_type])
            
            text = f"✅ **Триггер добавлен!**\n\n🔥 {trigger_names[trigger_type]}\n\nТеперь вы можете отслеживать прогресс по этой привычке."
            
            keyboard = [
                [InlineKeyboardButton("➕ Добавить еще", callback_data="new_trigger")],
                [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(text, reply_markup=reply_markup)
        
        elif trigger_type == "custom":
            text = "✍️ **Пользовательский триггер**\n\nНапишите название привычки, с которой хотите бороться:"
            
            keyboard = [
                [InlineKeyboardButton("🔙 Назад", callback_data="new_trigger")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(text, reply_markup=reply_markup)
            
            # Сохраняем состояние ожидания ввода
            context.user_data['waiting_for_custom_trigger'] = True
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ статистики пользователя"""
        user_id = update.effective_user.id
        stats = await self.db.get_user_stats(user_id)
        
        text = self.templates.get_stats_message(stats)
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="show_stats")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.message:
            await update.message.reply_text(text, reply_markup=reply_markup)
        else:
            await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    
    async def show_about(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Информация о боте"""
        query = update.callback_query
        
        text = self.templates.get_about_message()
        
        keyboard = [
            [InlineKeyboardButton("🔒 Подписка (скоро)", callback_data="subscription")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(text, reply_markup=reply_markup)
    
    async def handle_text_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Проверяем, ожидаем ли мы ввод пользовательского триггера
        if context.user_data.get('waiting_for_custom_trigger'):
            await self.db.add_user_trigger(user_id, message_text)
            context.user_data['waiting_for_custom_trigger'] = False
            
            text = f"✅ **Триггер добавлен!**\n\n🔥 {message_text}\n\nТеперь вы можете отслеживать прогресс по этой привычке."
            
            keyboard = [
                [InlineKeyboardButton("➕ Добавить еще", callback_data="new_trigger")],
                [InlineKeyboardButton("📊 Статистика", callback_data="show_stats")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(text, reply_markup=reply_markup)
        else:
            # Обычное сообщение - показываем главное меню
            await self.show_main_menu(update, context)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = self.templates.get_help_message()
        
        keyboard = [
            [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(help_text, reply_markup=reply_markup)
