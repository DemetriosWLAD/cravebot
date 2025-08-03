# CraveBreaker Telegram Bot

## Overview
CraveBreaker is a Telegram bot designed to help users combat compulsive habits and impulses. It provides immediate mini-interventions, tracks progress, offers breathing techniques, coaching questions, and distraction games. The project aims to offer accessible support for behavioral change, with ambitions for future monetization through features like audio meditations.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture

### Backend
- **Language**: Python 3.x
- **Framework**: `python-telegram-bot` for Telegram API integration.
- **Architecture Pattern**: Object-oriented design with a modular structure (handlers, database, config, utils).
- **Database**: SQLite (using a custom `Database` class) for user and progress data.
- **Deployment**: Designed as a single-process application, supporting various hosting environments including Docker and Cloud Run.

### Key Design Decisions
- **Modularity**: Separation of concerns into focused modules for maintainability.
- **Asynchronous Operations**: Utilizes Python's `asyncio` for efficient Telegram API handling.
- **Configuration**: Centralized settings with environment variable support.
- **Template-based Messaging**: Consistent user experience through reusable message templates.
- **Intervention System**: Core functionality encompassing breathing techniques, coaching questions, and mini-games.
- **Gamification**: Includes achievement badges, XP levels, and streak tracking to enhance user engagement.
- **User Interface (UI/UX)**: Simplistic and intuitive, primarily text-based with emoji integration. Navigation is streamlined through simplified menus and contextual routing.
- **Data Flow**: User interaction is routed through handlers, querying/updating the SQLite database, applying intervention logic, and generating templated responses via the Telegram API.
- **Scalability Considerations**: Currently optimized for small to medium user bases; designed to allow for future migration to more robust database solutions like PostgreSQL if needed.

### Core Features
- **User Onboarding**: Guided setup for new users.
- **Command Handling**: Standard Telegram commands (`/start`, `/help`, `/menu`, `/stats`).
- **Intervention Management**: Provides emergency support for habit interruption.
- **Progress Tracking**: Stores user statistics and progress.
- **Motivational System**: Delivers personalized daily motivational quotes.
- **Gamification**: Implements achievements, XP, levels, and streak tracking.
- **F.A.Q. Section**: Comprehensive guidance on bot features.

- **Personal Coach Integration**: Connects users with a certified coach and related channels.
- **Trigger Input System**: Interactive system for users to log and manage their triggers.

## External Dependencies

- **`python-telegram-bot`**: The primary library for interacting with the Telegram Bot API.
- **SQLite**: Used as the embedded database for persistent storage.
- **`asyncio`**: Python's built-in library for concurrent programming.
- **Flask**: Used for implementing health check endpoints in deployment environments.
- **Gunicorn**: Recommended for production WSGI deployments.
- **Google Forms**: Integrated for the personal coach booking system.
- **Payment Gateways**: (Specifics not detailed, but implied by "multiple payment methods" for audio meditations).
- **Environment Variables**:
    - `TELEGRAM_BOT_TOKEN`: Required for Telegram API authentication.
    - `DATABASE_PATH`: Optional path for the SQLite database file.
    - `DEBUG`: Optional flag for debug mode.
    - `LOG_LEVEL`: Optional configuration for logging verbosity.