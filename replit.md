# CraveBreaker Telegram Bot

## Overview

CraveBreaker is a Telegram bot designed to help users combat compulsive habits and impulses through mini-interventions. The bot provides emergency support, progress tracking, breathing techniques, coaching questions, and distraction games to help users overcome unwanted behaviors.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Backend Architecture
- **Language**: Python 3.x
- **Framework**: python-telegram-bot library for Telegram API integration
- **Architecture Pattern**: Object-oriented design with separation of concerns
- **Database**: SQLite (using a custom Database class)
- **Deployment**: Single-process application designed for simple hosting

### Key Design Decisions
1. **Modular Structure**: The application is split into focused modules (handlers, database, config, utils) for maintainability
2. **Async/Await Pattern**: Uses Python's asyncio for handling Telegram API calls efficiently
3. **Configuration Management**: Centralized configuration with environment variable support
4. **Template-based Messaging**: Reusable message templates for consistent user experience

## Key Components

### 1. Bot Handlers (`bot_handlers.py`)
- **Purpose**: Manages all Telegram message and callback handlers
- **Key Features**:
  - User onboarding flow for new users
  - Command handling (/start, /help, /menu, /stats)
  - Intervention management integration
  - Message templating system

### 2. Database Layer (`database.py`)
- **Purpose**: Data persistence and user management
- **Technology**: Custom SQLite wrapper
- **Key Functions**:
  - User creation and existence checking
  - Data storage for user progress and statistics
  - Configurable data retention (365 days default)

### 3. Configuration (`config.py`)
- **Purpose**: Centralized application settings
- **Key Settings**:
  - Bot token and database path configuration
  - Intervention timing parameters (60s breathing duration, 5min minimum interval)
  - User limits (10 triggers max, 50 daily interventions)
  - Security settings (rate limiting, message length limits)
  - UI emojis and interface elements

### 4. Utilities (`utils.py`)
- **Purpose**: Message templates and helper functions
- **Key Features**:
  - Motivational quotes system
  - Welcome and menu message templates
  - Reusable text formatting utilities

### 5. Main Application (`main.py`)
- **Purpose**: Application entry point and bot setup
- **Key Responsibilities**:
  - Bot initialization and configuration
  - Handler registration (commands, callbacks, messages)
  - Logging setup and error handling

### 6. Intervention System
- **Purpose**: Core functionality for habit interruption
- **Features**: Breathing techniques, coaching questions, mini-games
- **Integration**: Managed through InterventionManager class

## Data Flow

1. **User Interaction**: User sends message or command to Telegram bot
2. **Handler Routing**: Appropriate handler method is called based on message type
3. **Database Query**: User data is retrieved or updated in SQLite database
4. **Intervention Logic**: If needed, intervention techniques are applied
5. **Response Generation**: Message templates are used to create user-friendly responses
6. **Telegram API**: Response is sent back through Telegram bot API

## External Dependencies

### Core Dependencies
- **python-telegram-bot**: Primary library for Telegram Bot API integration
- **SQLite**: Built-in Python database for data persistence
- **asyncio**: Python's built-in async library for concurrent operations

### Environment Variables
- `TELEGRAM_BOT_TOKEN`: Required bot token from BotFather
- `DATABASE_PATH`: Optional custom database file path
- `DEBUG`: Optional debug mode flag
- `LOG_LEVEL`: Optional logging level configuration

## Deployment Strategy

### Current Setup
- **Target Platform**: Any Python-compatible hosting service
- **Database**: File-based SQLite (portable, no external database required)
- **Configuration**: Environment variables for sensitive data
- **Logging**: Configurable logging levels for production monitoring

### Deployment Requirements
1. Python 3.x runtime environment
2. Access to Telegram Bot API (internet connection required)
3. Persistent storage for SQLite database file
4. Environment variable support for bot token
5. **Cloud Run Requirements** (✅ CONFIGURED):
   - ✅ Health check endpoint on `/` responding with 200 status
   - ✅ Flask server listening on port 5000 with host 0.0.0.0
   - ✅ Main entry point: `app.py` 
   - ✅ Dockerfile configured for requirements.txt
   - ✅ Production secrets: TELEGRAM_BOT_TOKEN, SESSION_SECRET
   - ✅ Container deployment via Dockerfile

### Scalability Considerations
- Single-process design suitable for small to medium user bases
- SQLite limitations may require migration to PostgreSQL for larger deployments
- Rate limiting implemented to prevent abuse
- Data cleanup mechanisms to manage storage growth

The architecture prioritizes simplicity and maintainability while providing a robust foundation for habit-breaking interventions through Telegram's messaging platform.

## Recent Changes: Latest modifications with dates

### July 24, 2025 - Cloud Run Deployment Fixes Applied
- ✅ Fixed port conflict by removing Download Server workflow
- ✅ Updated Dockerfile to use requirements.txt instead of pyproject.toml  
- ✅ Added curl dependency to Dockerfile for health checks
- ✅ Configured app.py to bind to 0.0.0.0:5000 for Cloud Run compatibility
- ✅ Health check endpoints `/` and `/health` now responding with 200 status
- ✅ Telegram bot integration working properly
- ✅ Flask threaded mode enabled for better concurrent handling
- **Status**: Ready for Cloud Run deployment with proper health checks

### 2025-07-24: PERSONALIZED DAILY MOTIVATION QUOTES GENERATOR IMPLEMENTED
- ✅ **AI-Powered Personalization** - OpenAI GPT-4o integration for unique, context-aware quotes
- ✅ **Smart Contextual Generation** - Quotes adapt to user level, streak, achievements, and time of day
- ✅ **Enhanced Achievement Celebrations** - AI-generated personalized congratulations for new badges
- ✅ **Daily Motivation Section** - New "💫 Мотивация дня" in main menu with personalized content
- ✅ **Evening Reflection Feature** - Dedicated section for end-of-day motivation and self-reflection
- ✅ **Fallback System** - Curated quotes library ensures functionality without API dependency
- ✅ **Multi-Context Support** - Different quote types for morning, success, milestones, and comebacks

### 2025-07-24: GAMIFICATION SYSTEM IMPLEMENTED
- ✅ **Full Gamification System Added** - Achievement badges, XP levels, and streak tracking
- ✅ **Achievement Badges System** - 15+ different badges for milestones, streaks, and progress
- ✅ **XP and Level System** - Users earn XP for successful interventions, level up progression
- ✅ **Streak Tracking** - Daily intervention streaks with special achievements
- ✅ **Badge Notifications** - Real-time badge earning with XP rewards
- ✅ **Progress Visualization** - Comprehensive achievements screen showing user progress
- ✅ **Database Integration** - User progress and badges stored in SQLite database
- ✅ **Enhanced User Engagement** - Gamification integrated into all intervention success flows

### 2025-07-24: ПОЛНОЕ АВТОМАТИЧЕСКОЕ РАЗВЕРТЫВАНИЕ ЗАВЕРШЕНО  
- ✅ **Бот развернут в облаке Replit** - работает 24/7 без участия пользователя
- ✅ **Активирована система Replit Deployments** - автоматическое масштабирование и перезапуски
- ✅ **Добавлена функция скачивания файлов** - endpoint /files для загрузки архива развертывания
- ✅ **Создан полный пакет развертывания** - CraveBreaker_Deploy.zip с инструкциями
- ✅ **Решена проблема 24/7 работы** - бот больше не зависит от компьютера пользователя
- ✅ **Все функции активны**: 125 техник поддержки, персональный коучинг, статистика

### 2025-07-23: Expanded Feature Set - 125 Total Techniques
- ✅ **25 Breathing Techniques**: From basic 4-7-8 to advanced pranayama techniques
  - Классические техники (5): 4-7-8, квадратное, треугольное, дыхание 5-5, брюшное
  - Успокаивающие техники (5): океана, пчелы, лунное, в счет 6, сердечное
  - Энергизирующие техники (5): огненное, солнечное, силы, ступенчатое, воина
  - Специальные техники (5): альтернативное, льва, волны, в цвете, со звуком
  - Продвинутые техники (5): ретенционное, шипения, свистка, пранаяма 1-4-2, освобождения
- ✅ **50 Meditation Practices**: Complete mindfulness and meditation collection
  - Базовые медитации (10): дыхания, сканирование тела, ходьбы, звуков, на пламя
  - Практики осознанности (10): питание, мытье посуды, эмоций, мыслей, благодарности
  - Визуализации (10): света, горы, океана, дерева, лотоса и другие
  - Мантра-медитации (10): ОМ, Со Хам, покоя, сострадания, мудрости
  - Продвинутые практики (10): пустоты, свидетеля, "Кто я?", единства, тишины
- ✅ **50 Distraction Games**: Interactive mental exercises and activities
  - Математические игры (10): обратный счет, умножение, последовательности, загадки
  - Словесные игры (10): алфавитные категории, рифмы, синонимы, ассоциации
  - Визуальные игры (10): цветовая радуга, мысленная комната, геометрия, путешествия
  - Физические упражнения (10): пальчиковая гимнастика, дыхательная гимнастика, массаж
  - Креативные игры (10): изобретения, истории, дизайн, музыка, планирование
- ✅ **New Meditation Section**: Added "🧘‍♀️ Медитация и осознанность" to intervention menu
- ✅ **Enhanced User Experience**: All techniques now show names and detailed instructions
- ✅ **Navigation Improvements**: Added "try another technique" buttons for each category

### 2025-07-23: Updated Coach Branding
- ✅ Updated coach description to "сертифицированным лайф- и бизнес-коучем Международной Федерации Коучинга"
- ✅ Maintained @CoaCerto for personal messaging and @SpotCoach for channel content

### 2025-07-23: Deployment-Ready Configuration Applied
- ✅ Added Flask-based health check server with endpoints: `/`, `/health`, `/status`
- ✅ Created `app.py` as main entry point for Cloud Run deployment
- ✅ Configured dual-service architecture: Flask health server + Telegram bot in threads
- ✅ Updated workflow to serve on port 5000 as required for deployment
- ✅ Added `Dockerfile` and `cloudbuild.yaml` for container deployment
- ✅ Fixed database query null handling for production stability
- ✅ All health check endpoints verified working (200 status codes)
- ✅ Bot successfully running with proper Cloud Run configuration

### 2025-07-23: Personal Coach Integration  
- ✅ Added "Мой персональный коуч" section to main menu
- ✅ Integrated Google Forms booking system (https://forms.gle/C8Bo6N43AsKMBb2f9)
- ✅ Created "Чисто отвести душу" emotional support option
- ✅ Connected @SpotCoach "канал пользы" and @CoaCerto direct messaging
- ✅ Streamlined coaching services with 4 clear options
- ✅ Updated coaching contact to redirect to @CoaCerto instead of @SpotCoach

### Previous: 2025-07-23: Создание MVP версии CraveBreaker бота  
- Создан полнофункциональный Simple CraveBreaker Bot (simple_bot.py)
- Бот работает напрямую с Telegram Bot API без использования python-telegram-bot
- Реализованы все ключевые функции: экстренная помощь, интервенции, статистика
- База данных SQLite для хранения пользователей и статистики
- Решена проблема с конфликтом пакетов telegram
- Бот успешно запущен и готов к тестированию