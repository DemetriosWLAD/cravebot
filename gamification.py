#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gamification System for CraveBreaker Bot
Implements achievement badges, streaks, levels, and rewards
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

class BadgeType(Enum):
    """Types of achievement badges"""
    STREAK = "streak"
    TECHNIQUE = "technique"
    MILESTONE = "milestone"
    SPECIAL = "special"
    PROGRESSION = "progression"

class BadgeRarity(Enum):
    """Badge rarity levels"""
    COMMON = "common"
    UNCOMMON = "uncommon"
    RARE = "rare"
    EPIC = "epic"
    LEGENDARY = "legendary"

@dataclass
class Badge:
    """Achievement badge data structure"""
    id: str
    name: str
    description: str
    emoji: str
    badge_type: BadgeType
    rarity: BadgeRarity
    requirement: Dict
    xp_reward: int
    unlocked_at: Optional[datetime] = None

@dataclass
class UserProgress:
    """User gamification progress"""
    user_id: int
    level: int = 1
    xp: int = 0
    total_interventions: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    last_intervention_date: Optional[str] = None
    badges_earned: Optional[List[str]] = None
    technique_counts: Optional[Dict[str, int]] = None
    
    def __post_init__(self):
        if self.badges_earned is None:
            self.badges_earned = []
        if self.technique_counts is None:
            self.technique_counts = {}

class GamificationSystem:
    """Main gamification system manager"""
    
    def __init__(self):
        self.badges = self._initialize_badges()
        self.level_thresholds = [0, 100, 250, 500, 1000, 1750, 2750, 4000, 5500, 7500, 10000]
        
    def _initialize_badges(self) -> Dict[str, Badge]:
        """Initialize all available badges"""
        badges = {}
        
        # Streak Badges
        streak_badges = [
            ("first_intervention", "🌱 Первый шаг", "Провел первую интервенцию", BadgeRarity.COMMON, {"interventions": 1}, 25),
            ("streak_3", "🔥 Тепло", "3 дня подряд", BadgeRarity.COMMON, {"streak": 3}, 50),
            ("streak_7", "⚡ Неделя силы", "7 дней подряд", BadgeRarity.UNCOMMON, {"streak": 7}, 100),
            ("streak_14", "💪 Двухнедельный воин", "14 дней подряд", BadgeRarity.RARE, {"streak": 14}, 200),
            ("streak_30", "🏆 Чемпион месяца", "30 дней подряд", BadgeRarity.EPIC, {"streak": 30}, 500),
            ("streak_100", "👑 Легенда дисциплины", "100 дней подряд", BadgeRarity.LEGENDARY, {"streak": 100}, 1000),
        ]
        
        for badge_id, name, desc, rarity, req, xp in streak_badges:
            badges[badge_id] = Badge(badge_id, name, desc, name.split()[0], BadgeType.STREAK, rarity, req, xp)
        
        # Technique Mastery Badges
        technique_badges = [
            ("breathing_master", "🫁 Мастер дыхания", "Использовал 10 разных дыхательных техник", BadgeRarity.UNCOMMON, {"breathing_techniques": 10}, 150),
            ("meditation_guru", "🧘 Гуру медитации", "Использовал 15 разных медитативных практик", BadgeRarity.RARE, {"meditation_techniques": 15}, 200),
            ("game_champion", "🎮 Чемпион игр", "Попробовал 20 разных отвлекающих игр", BadgeRarity.RARE, {"game_techniques": 20}, 200),
            ("technique_explorer", "🗺️ Исследователь техник", "Использовал все 125 техник", BadgeRarity.LEGENDARY, {"total_unique_techniques": 125}, 1500),
        ]
        
        for badge_id, name, desc, rarity, req, xp in technique_badges:
            badges[badge_id] = Badge(badge_id, name, desc, name.split()[0], BadgeType.TECHNIQUE, rarity, req, xp)
        
        # Milestone Badges
        milestone_badges = [
            ("interventions_10", "🎯 Новичок", "10 интервенций", BadgeRarity.COMMON, {"total_interventions": 10}, 75),
            ("interventions_50", "🚀 Энтузиаст", "50 интервенций", BadgeRarity.UNCOMMON, {"total_interventions": 50}, 150),
            ("interventions_100", "💎 Эксперт", "100 интервенций", BadgeRarity.RARE, {"total_interventions": 100}, 300),
            ("interventions_500", "🌟 Мастер", "500 интервенций", BadgeRarity.EPIC, {"total_interventions": 500}, 750),
            ("interventions_1000", "🔮 Гранд-мастер", "1000 интервенций", BadgeRarity.LEGENDARY, {"total_interventions": 1000}, 1500),
        ]
        
        for badge_id, name, desc, rarity, req, xp in milestone_badges:
            badges[badge_id] = Badge(badge_id, name, desc, name.split()[0], BadgeType.MILESTONE, rarity, req, xp)
        
        # Special Achievement Badges
        special_badges = [
            ("night_owl", "🦉 Сова", "Интервенция после полуночи", BadgeRarity.UNCOMMON, {"late_night_intervention": True}, 100),
            ("early_bird", "🐦 Жаворонок", "Интервенция до 6 утра", BadgeRarity.UNCOMMON, {"early_morning_intervention": True}, 100),
            ("weekend_warrior", "⚔️ Воин выходных", "10 интервенций в выходные", BadgeRarity.RARE, {"weekend_interventions": 10}, 200),
            ("comeback_kid", "🔄 Возвращение", "Вернулся после 7+ дней перерыва", BadgeRarity.UNCOMMON, {"comeback": True}, 150),
            ("coaching_seeker", "💬 Ищущий совета", "Обратился к персональному коучу", BadgeRarity.COMMON, {"used_coaching": True}, 50),
        ]
        
        for badge_id, name, desc, rarity, req, xp in special_badges:
            badges[badge_id] = Badge(badge_id, name, desc, name.split()[0], BadgeType.SPECIAL, rarity, req, xp)
        
        return badges
    
    def check_and_award_badges(self, user_progress: UserProgress, intervention_data: Dict) -> List[Badge]:
        """Check for new badge achievements and award them"""
        newly_earned = []
        
        for badge_id, badge in self.badges.items():
            if badge_id in user_progress.badges_earned:
                continue
                
            if self._check_badge_requirement(badge, user_progress, intervention_data):
                user_progress.badges_earned.append(badge_id)
                user_progress.xp += badge.xp_reward
                badge.unlocked_at = datetime.now()
                newly_earned.append(badge)
        
        return newly_earned
    
    def _check_badge_requirement(self, badge: Badge, progress: UserProgress, intervention_data: Dict) -> bool:
        """Check if badge requirements are met"""
        req = badge.requirement
        
        if "interventions" in req:
            return progress.total_interventions >= req["interventions"]
        
        if "streak" in req:
            return progress.current_streak >= req["streak"]
        
        if "total_interventions" in req:
            return progress.total_interventions >= req["total_interventions"]
        
        if "breathing_techniques" in req:
            breathing_count = sum(1 for technique, count in progress.technique_counts.items() 
                               if technique.startswith("breathing_") and count > 0)
            return breathing_count >= req["breathing_techniques"]
        
        if "meditation_techniques" in req:
            meditation_count = sum(1 for technique, count in progress.technique_counts.items() 
                                if technique.startswith("meditation_") and count > 0)
            return meditation_count >= req["meditation_techniques"]
        
        if "game_techniques" in req:
            game_count = sum(1 for technique, count in progress.technique_counts.items() 
                           if technique.startswith("game_") and count > 0)
            return game_count >= req["game_techniques"]
        
        if "total_unique_techniques" in req:
            unique_count = sum(1 for count in progress.technique_counts.values() if count > 0)
            return unique_count >= req["total_unique_techniques"]
        
        # Special badge checks
        if "late_night_intervention" in req:
            current_hour = datetime.now().hour
            return current_hour >= 0 and current_hour < 6
        
        if "early_morning_intervention" in req:
            current_hour = datetime.now().hour
            return current_hour >= 5 and current_hour < 8
        
        if "weekend_interventions" in req:
            weekend_count = intervention_data.get("weekend_count", 0)
            return weekend_count >= req["weekend_interventions"]
        
        if "comeback" in req:
            return intervention_data.get("is_comeback", False)
        
        if "used_coaching" in req:
            return intervention_data.get("used_coaching", False)
        
        return False
    
    def calculate_level(self, xp: int) -> int:
        """Calculate user level based on XP"""
        for level, threshold in enumerate(self.level_thresholds):
            if xp < threshold:
                return level
        return len(self.level_thresholds)
    
    def get_xp_for_next_level(self, current_xp: int) -> Tuple[int, int]:
        """Get XP needed for next level and current level progress"""
        current_level = self.calculate_level(current_xp)
        
        if current_level >= len(self.level_thresholds):
            return 0, 0  # Max level reached
        
        current_threshold = self.level_thresholds[current_level - 1] if current_level > 0 else 0
        next_threshold = self.level_thresholds[current_level]
        
        xp_for_next = next_threshold - current_xp
        progress_in_level = current_xp - current_threshold
        
        return xp_for_next, progress_in_level
    
    def update_streak(self, user_progress: UserProgress) -> bool:
        """Update user streak based on intervention date"""
        today = datetime.now().date().isoformat()
        
        if user_progress.last_intervention_date is None:
            # First intervention
            user_progress.current_streak = 1
            user_progress.longest_streak = 1
            user_progress.last_intervention_date = today
            return True
        
        last_date = datetime.fromisoformat(user_progress.last_intervention_date).date()
        current_date = datetime.now().date()
        
        days_diff = (current_date - last_date).days
        
        if days_diff == 0:
            # Same day, no streak change
            return False
        elif days_diff == 1:
            # Consecutive day, increase streak
            user_progress.current_streak += 1
            user_progress.longest_streak = max(user_progress.longest_streak, user_progress.current_streak)
            user_progress.last_intervention_date = today
            return True
        else:
            # Streak broken, reset
            user_progress.current_streak = 1
            user_progress.last_intervention_date = today
            return True
    
    def format_badge_message(self, badges: List[Badge]) -> str:
        """Format badge achievement message"""
        if not badges:
            return ""
        
        message = "🎉 **НОВЫЕ ДОСТИЖЕНИЯ!**\n\n"
        
        for badge in badges:
            rarity_emoji = {
                BadgeRarity.COMMON: "⚪",
                BadgeRarity.UNCOMMON: "🟢", 
                BadgeRarity.RARE: "🔵",
                BadgeRarity.EPIC: "🟣",
                BadgeRarity.LEGENDARY: "🟡"
            }
            
            message += f"{badge.emoji} **{badge.name}** {rarity_emoji[badge.rarity]}\n"
            message += f"*{badge.description}*\n"
            message += f"💎 +{badge.xp_reward} XP\n\n"
        
        return message
    
    def get_user_stats_message(self, user_progress: UserProgress) -> str:
        """Generate user statistics and achievements message"""
        level = self.calculate_level(user_progress.xp)
        xp_needed, progress_in_level = self.get_xp_for_next_level(user_progress.xp)
        
        message = f"📊 **ТВОЯ СТАТИСТИКА**\n\n"
        message += f"🏆 **Уровень:** {level}\n"
        message += f"💎 **Опыт:** {user_progress.xp}\n"
        
        if xp_needed > 0:
            message += f"⬆️ **До следующего уровня:** {xp_needed} XP\n"
        else:
            message += f"👑 **МАКСИМАЛЬНЫЙ УРОВЕНЬ!**\n"
        
        message += f"📈 **Интервенций:** {user_progress.total_interventions}\n"
        message += f"🔥 **Текущая серия:** {user_progress.current_streak} дней\n"
        message += f"🎯 **Лучшая серия:** {user_progress.longest_streak} дней\n"
        message += f"🏅 **Достижений:** {len(user_progress.badges_earned)}\n\n"
        
        # Show recent badges
        if user_progress.badges_earned:
            message += "🏆 **ПОСЛЕДНИЕ ДОСТИЖЕНИЯ:**\n"
            recent_badges = user_progress.badges_earned[-3:]  # Show last 3
            for badge_id in recent_badges:
                if badge_id in self.badges:
                    badge = self.badges[badge_id]
                    message += f"{badge.emoji} {badge.name}\n"
        
        return message
    
    def get_available_badges_message(self) -> str:
        """Get message showing available badges to earn"""
        message = "🎯 **ДОСТУПНЫЕ ДОСТИЖЕНИЯ**\n\n"
        
        # Group badges by type
        badge_groups = {
            BadgeType.STREAK: "🔥 **СЕРИИ**",
            BadgeType.MILESTONE: "🎯 **РУБЕЖИ**", 
            BadgeType.TECHNIQUE: "🛠️ **МАСТЕРСТВО**",
            BadgeType.SPECIAL: "⭐ **ОСОБЫЕ**"
        }
        
        for badge_type, title in badge_groups.items():
            type_badges = [b for b in self.badges.values() if b.badge_type == badge_type]
            if not type_badges:
                continue
                
            message += f"{title}\n"
            for badge in sorted(type_badges, key=lambda x: x.xp_reward):
                rarity_emoji = {
                    BadgeRarity.COMMON: "⚪",
                    BadgeRarity.UNCOMMON: "🟢", 
                    BadgeRarity.RARE: "🔵",
                    BadgeRarity.EPIC: "🟣",
                    BadgeRarity.LEGENDARY: "🟡"
                }
                message += f"{badge.emoji} {badge.name} {rarity_emoji[badge.rarity]} (+{badge.xp_reward} XP)\n"
                message += f"   *{badge.description}*\n"
            message += "\n"
        
        return message

# Global instance
gamification_system = GamificationSystem()