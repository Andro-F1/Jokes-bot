#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ukrainian Telegram Bot with Random Jokes, Magic 8-Ball, Who Are You Today Game, and Language Support
Uses pyTelegramBotAPI for Telegram integration
"""

import telebot
from telebot import types
import random
import os
import logging
import time
from typing import List, Dict, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class UkrainianJokeBot:
    """Ukrainian Telegram bot with jokes, 8-ball, role game, and language support"""
    
    def __init__(self):
        # Get bot token from environment variables with fallback
        self.token = os.getenv("TELEGRAM_BOT_TOKEN", "7780156035:AAEz5429RugouRncofxQM9ub9lp7Q5HQNAU")
        
        # Initialize bot
        try:
            self.bot = telebot.TeleBot(self.token)
            logger.info("Bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize bot: {e}")
            raise
        
        # Language settings and tracking
        self.user_languages = {}  # Store user language preferences
        self.used_jokes = {}  # Track used jokes per user
        self.last_roles = {}  # Track last roles to avoid repetition
        
        # Magic 8-ball answers for Ukrainian
        self.magic_answers_uk = [
            "Так ✅", "Ні ❌", "Можливо 🤔", "Запитай ще раз 🔄", "Я не впевнений 😶",
            "Очевидно!", "100%", "Тобі це не сподобається...", "Шанси малі, але є.",
            "Точно ні!", "Безумовно так!", "Краще не варто", "Зірки кажуть так",
            "Мої джерела кажуть ні", "Перспективи хороші", "Залежить від тебе",
            "Не розраховуй на це", "Так, але будь обережний", "Спробуй ще раз пізніше",
            "Все можливо!", "Ти жартуєш?", "Навіть не думай!", "Мрій далі!",
            "Куля каже: LOL", "Спитай у мами", "42 - відповідь на все", "Навпаки!",
            "Тільки в четвер", "Коли сонце зайде на заході", "Магія не працює сьогодні",
            "Переверни телефон і спитай знову", "Куля думає...", "Помилка 404",
            "Спробуй інакше сформулювати", "Так, але ні", "Ні, але так",
            "Може і так, а може і ні", "Куля на технічному обслуговуванні",
            "Спитай у кота", "Тільки якщо танцюватимеш", "Коли свині полетять",
            "Зірки не відповідають", "Куля спить", "Перезавантаж мізки і спитай знову",
            "Обов’язково ні!", "Обов’язково так!", "Можливо, але навряд чи",
            "Куля в злому настрої", "Поклич бабусю", "Ні за що!",
            "За твоїм власним ризиком", "Коли кактус полетить", "Просто LMAO",
            "Не моє діло", "Запитай своє свідоме", "Ні в якому разі!",
            "Куля на профилактиці", "Будь ласка і ні", "Можливо так, а можливо — автобус",
            "Куля в отпуске", "Запитай в Google", "Ніколи не говори ніколи"
        ]
        
        # Magic 8-ball answers for English  
        self.magic_answers_en = [
            "Yes ✅", "No ❌", "Maybe 🤔", "Ask again 🔄", "I'm not sure 😶",
            "Obviously!", "100%", "You won't like it...", "Chances are small but exist.",
            "Definitely no!", "Absolutely yes!", "Better not", "Stars say yes",
            "My sources say no", "Outlook good", "It's up to you",
            "Don't count on it", "Yes, but be careful", "Try again later",
            "Everything is possible!", "Are you kidding?", "Not even close!", "Dream on!",
            "Ball says: LOL", "Ask your mom", "42 is the answer to everything", "Opposite!",
            "Only on Thursday", "When sun sets in the west", "Magic doesn't work today",
            "Flip your phone and ask again", "Ball is thinking...", "Error 404",
            "Try rephrasing", "Yes, but no", "No, but yes",
            "Maybe yes, maybe no", "Ball is under maintenance",
            "Ask the cat", "Only if you dance", "When pigs fly",
            "Stars are not responding", "Ball is sleeping", "Reboot brain and ask again",
            "Absolutely not!", "Absolutely yes!", "Maybe, but probably not",
            "Ball is in a bad mood", "Call your grandma", "Not a chance!",
            "At your own risk", "When cactus flies", "Just LMAO",
            "Not my business", "Ask your conscience", "In no way!",
            "Ball is on maintenance", "Please, just no", "Maybe yes, maybe bus",
            "Ball is on vacation", "Ask Google", "Never say never"
        ]

        # Ukrainian roles for "Who are you today" game
        self.roles_uk = [
            "🥷 Ти сьогодні — ніндзя, але забув маску.",
            "🦸‍♂️ Ти супергерой… тільки без суперсили.",
            "🛌 Ти як подушка — всі тебе люблять, але тільки коли хочуть спати.",
            "⚡ Ти сьогодні як розряджений телефон — всі нервуються, але нічого не роблять.",
            "🍕 Ти як останній шматочок піци — всі хочуть, але ніхто не бере.",
            "🎲 Ти головний гравець у грі під назвою 'життя'.",
            "💾 Ти як флешка на 2 ГБ — ще існуєш, але нікому не потрібен.",
            "🐒 Ти сьогодні — мавпа, яка дивиться на людей і думає, хто тут справжній еволюціонер.",
            "🎭 Ти головний герой серіалу, який ще не зняли.",
            "🛠️ Ти сьогодні — костиль, але без тебе нічого не працює.",
            "🧟‍♂️ Ти зомбі, але замість мізків полюєш смартфони.",
            "🤖 Ти робот, який навчився лінуватися.",
            "🐱 Ти кіт, який притворяється людиною.",
            "🦄 Ти магічний єдиноріг, але ріг зламався.",
            "👎 Ти сьогодні — розумний мем, але ніхто не розуміє.",
            "🎨 Ти художник, який малює емоції на повітрі.",
            "🕵️‍♂️ Ти детектив, який розслідує зникнення власної мотивації.",
            "📺 Ти старий телевізор — всі ностальгують, але ніхто не вмикає.",
            "🕰️ Ти тайм машина, але застряг у понеділку.",
            "🌭 Ти хот-дог у вегетаріанському кафе — сидиш і не розумієш, що тут робиш.",
            "🚽 Ти мудрець, який медитує у туалеті.",
            "🎆 Ти феєрверк, який згорає на роботі.",
            "🧛‍♀️ Ти вампір, але замість крові п'єш каву.",
            "🐌 Ти черв'як, який вирішив стати метеликом, але застряг по дорозі.",
            "🌊 Ти цунамі, але у склянці води.",
            "🧭 Ти компас, який завжди вказує на південь.",
            "🏝️ Ти турист, який загубився в інтернеті.",
            "🐈‍⬛ Ти чорний кіт, який приносить щастя через меми.",
            "🎪 Ти цирк, але клоуни в декреті.",
            "🚁 Ти гелікоптер, який боїться висоти.",
            "📱 Ти додаток, який ніхто не скачує.",
            "🥪 Ти сендвіч, який намагається дієтувати.",
            "🔋 Ти повербанк, який сам потребує зарядки.",
            "🎯 Ти мішень, але всі стріляють повз.",
            "🧸 Ти плюшевий ведмедик у світі дорослих проблем."
        ]
        
        # English roles for "Who are you today" game
        self.roles_en = [
            "🥷 You're a ninja today, but forgot your mask.",
            "🦸‍♂️ You're a superhero... just without superpowers.",
            "🛌 You're like a pillow — everyone loves you, but only when they want to sleep.",
            "⚡ You're like a dead phone battery today — everyone's nervous but does nothing.",
            "🍕 You're like the last slice of pizza — everyone wants it but nobody takes it.",
            "🎲 You're the main player in the game called 'life'.",
            "💾 You're like a 2GB flash drive — still exist but nobody needs you.",
            "🐒 You're a monkey today, watching people and wondering who's the real evolutionist.",
            "🎭 You're the main character in a TV show that hasn't been filmed yet.",
            "🛠️ You're a crutch today, but nothing works without you.",
            "🧟‍♂️ You're a zombie, but instead of brains you hunt smartphones.",
            "🤖 You're a robot who learned how to procrastinate.",
            "🐱 You're a cat pretending to be human.",
            "🦄 You're a magical unicorn, but the horn is broken.",
            "👎 You're a smart meme today, but nobody gets it.",
            "🎨 You're an artist painting emotions in the air.",
            "🕵️‍♂️ You're a detective investigating the disappearance of your own motivation.",
            "📺 You're an old TV — everyone's nostalgic but nobody turns you on.",
            "🕰️ You're a time machine stuck on Monday.",
            "🌭 You're a hot dog in a vegetarian cafe — sitting and not understanding what you're doing here.",
            "🚽 You're a wise man meditating in the toilet.",
            "🎆 You're a firework that burns out at work.",
            "🧛‍♀️ You're a vampire, but instead of blood you drink coffee.",
            "🐌 You're a worm who decided to become a butterfly but got stuck halfway.",
            "🌊 You're a tsunami in a glass of water.",
            "🧭 You're a compass that always points south.",
            "🏝️ You're a tourist lost on the internet.",
            "🐈‍⬛ You're a black cat bringing luck through memes.",
            "🎪 You're a circus, but clowns are on maternity leave.",
            "🚁 You're a helicopter afraid of heights.",
            "📱 You're an app that nobody downloads.",
            "🥪 You're a sandwich trying to diet.",
            "🔋 You're a power bank that needs charging itself.",
            "🎯 You're a target, but everyone misses.",
            "🧸 You're a teddy bear in a world of adult problems."
        ]

        # Ukrainian jokes collection (100 jokes without Russian words)
        self.jokes_uk: List[str] = [
            "Ти як Wi-Fi — всі підключаються, але пароль не знають.",
            "Життя — це не GTA, але я все одно чекаю, коли дадуть чіти.",
            "Краще бути в офлайні, ніж у боргах.",
            "Ти не дивний, ти — обмежена версія для колекціонерів!",
            "Моя зарплата як інтернет в селі — існує теоретично.",
            "Понеділок — це не день тижня, це стан душі.",
            "Ти як батарейка на 1% — ще працюєш, але всі нервують.",
            "Життя дало мені лимони, але я забув купити цукор.",
            "Ти сьогодні сяєш як екран телефону в темряві — яскраво і дратує.",
            "Ти як Google — у тебе є відповіді на все, але ніхто не читає далі першого рядка.",
            "Твоє життя — це як Windows Update: довго, дивно і завжди не вчасно.",
            "Кажуть, що сон — це для слабаків. Ну, тоді я найслабший супергерой у світі.",
            "Ти як зарядка від iPhone — всім потрібен, але ніхто не хоче купувати.",
            "Ніколи не здавайся… хіба що пароль занадто складний.",
            "Ти як вихідний день — всі тебе чекають, але ти швидко закінчуєшся.",
            "Моє терпіння як батарейка старого телефону — сідає несподівано.",
            "Ти як реклама на YouTube — спочатку дратуєш, потім звикаєш.",
            "Життя як Instagram — всі показують тільки найкраще.",
            "Ти як чашка кави вранці — без тебе день не починається.",
            "Мій настрій як погода в Україні — мінливий і непередбачуваний.",
            "Ти як паспорт — важливий, але використовуєшся рідко.",
            "Моя мотивація як сигнал у ліфті — є, але слабкий.",
            "Ти як селфі — виглядаєш краще з фільтрами.",
            "Життя як тест на водійські права — здаєш кілька разів до перемоги.",
            "Ти як піца — навіть коли погана, все одно смачна.",
            "Мій розклад як обіцянки політиків — теоретично існує.",
            "Ти як WiFi у кафе — всі хочуть підключитися.",
            "Життя як гра — чим далі, тим складніші рівні.",
            "Ти як ранкова кава — гіркий, але необхідний.",
            "Мій бюджет як метелик — красивий, але швидко зникає.",
            "Ти як зарядка телефону — завжди загубляєшся, коли потрібен.",
            "Життя як автобус — якщо спізнився, чекай наступний.",
            "Ти як відпустка — довгоочікуваний і швидкоплинний.",
            "Мій сон як інтернет — коли потрібен найбільше, не працює.",
            "Ти як субота — найкращий день тижня.",
            "Життя як смартфон — чим новіше, тим швидше розряджається.",
            "Ти як лайк у соцмережі — приємний і безкоштовний.",
            "Мій настрій як курс валют — щодня змінюється.",
            "Ти як домашня їжа — проста, але найсмачніша.",
            "Життя як квест — багато завдань, але винагорода невідома.",
            "Ти як ранкова пробіжка — корисний, але важкий.",
            "Мій розум як Google Chrome — відкрито 100 вкладок одночасно.",
            "Ти як вечірня прогулянка — спокійний і приємний.",
            "Життя як навігатор — іноді веде не туди, куди хотів.",
            "Ти як улюблена пісня — можна слухати безкінечно.",
            "Мій настрій як погода — змінюється кожну годину.",
            "Ти як вихідні — закінчуєшся занадто швидко.",
            "Життя як відеогра — маєш кілька життів, але не знаєш скільки.",
            "Ти як ранкова зарядка — потрібен, але часто пропускається.",
            "Мій спокій як сигнал мобільного — зникає в найпотрібніший момент.",
            "Ти як улюблений серіал — чекаєш продовження.",
            "Життя як фільм — іноді комедія, іноді драма.",
            "Ти як весняне сонце — довгоочікуваний і теплий.",
            "Мій час як метро в годину пік — завжди в русі, але повільно.",
            "Ти як домашній затишок — простий, але дорогий.",
            "Життя як школа — урок за уроком, іспит за іспитом.",
            "Ти як ранкова свіжість — бадьорий і натхненний.",
            "Мій лінивець як панда — мила, але повільна.",
            "Ти як книга — чим глибше, тим цікавіше.",
            "Життя як танці — головне відчувати ритм.",
            "Ти як теплий плед — обіймаєш і заспокоюєш.",
            "Мій гумор як борщ — не всім до смаку.",
            "Ти як зоряне небо — прекрасний і загадковий.",
            "Життя як автомобіль — іноді глохне, але завжди можна завести.",
            "Ти як літній дощ — освіжаєш і радуєш.",
            "Мій режим дня як розклад поїздів — теоретично існує.",
            "Ти як домашній улюбленець — милий і відданий.",
            "Життя як покупки — завжди витрачаєш більше, ніж планував.",
            "Ти як сніданок — найважливіший і найкращий.",
            "Мій настрій як маятник — туди-сюди постійно.",
            "Ти як перша любов — незабутній і особливий.",
            "Життя як пазл — збираєш по частинках.",
            "Ти як ранкова роса — свіжий і чистий.",
            "Мій спокій як відпустка — рідкий, але цінний.",
            "Ти як улюблена страва — завжди піднімаєш настрій.",
            "Життя як марафон — важливо не швидкість, а витривалість.",
            "Ти як зимовий вечір — затишний і теплий.",
            "Мій оптимізм як смартфон — іноді потребує підзарядки.",
            "Ти як веселка після дощу — красивий і обнадійливий.",
            "Життя як велосипед — треба крутити педалі, щоб їхати.",
            "Ти як улюбленець учителя — особливий і помітний.",
            "Мій сон як кіт — коли хочу, тоді й приходить.",
            "Ти як літо — яскравий, теплий і незабутній.",
            "Життя як шахи — треба думати на кілька ходів вперед.",
            "Ти як морський бриз — свіжий і заспокійливий.",
            "Мій настрій як погода в горах — може змінитися миттєво.",
            "Ти як домашня випічка — ароматний і затишний.",
            "Життя як театр — всі грають свої ролі.",
            "Ти як ранкові птахи — активний і бадьорий.",
            "Мій лінивець як черепаха — повільно, але впевнено.",
            "Ти як зимові свята — довгоочікуваний і радісний.",
            "Життя як книга — кожен день нова сторінка.",
            "Ти як осіннє листя — барвистий і неповторний.",
            "Мій настрій як хмари — іноді темні, іноді світлі.",
            "Ти як ранкова йога — гнучкий і збалансований.",
            "Життя як сад — що посієш, те й пожнеш.",
            "Ти як теплий чай — заспокоюєш і зігріваєш.",
            "Мій час як річка — тече і не повертається.",
            "Ти як веселе кіно — піднімаєш настрій.",
            "Життя як подорож — важливий не пункт призначення, а шлях.",
            "Ти як весняні квіти — ніжний і прекрасний.",
            "Мій гумор як приправа — додає смак до життя.",
            "Ти як зимовий затишок — теплий і комфортний.",
            "Життя як конструктор — збираєш з того, що є.",
            "Ти як ранкове сонце — променистий і енергійний.",
            "Мій настрій як калейдоскоп — постійно змінюються фарби.",
            "Ти як улюблена мелодія — приємно слухати знову і знову.",
            "Життя як садівництво — треба поливати й доглядати.",
            "Ти як морська хвиля — сильний і вільний.",
            "Мій сон як гірський потік — чистий і освіжаючий.",
            "Ти як домашній затишок — простий, але дорогий серцю."
        ]
        
        # English jokes collection (50 jokes)
        self.jokes_en: List[str] = [
            "You're like Wi-Fi — everyone connects, but nobody knows the password.",
            "Life isn't GTA, but I'm still waiting for the cheat codes.",
            "Better to be offline than in debt.",
            "You're not weird, you're a limited collector's edition!",
            "My salary is like village internet — theoretically exists.",
            "Monday isn't a day of the week, it's a state of mind.",
            "You're like a 1% battery — still working but everyone's nervous.",
            "Life gave me lemons, but I forgot to buy sugar.",
            "You shine today like a phone screen in the dark — bright and annoying.",
            "You're like Google — you have answers to everything, but nobody reads past the first line.",
            "Your life is like Windows Update: long, weird and always at the wrong time.",
            "They say sleep is for the weak. Well, I'm the weakest superhero in the world.",
            "You're like an iPhone charger — everyone needs you but nobody wants to buy you.",
            "Never give up... unless the password is too complicated.",
            "You're like the weekend — everyone's waiting for you but you end too quickly.",
            "My patience is like an old phone battery — dies unexpectedly.",
            "You're like YouTube ads — annoying at first, then you get used to it.",
            "Life is like Instagram — everyone shows only the best parts.",
            "You're like morning coffee — the day doesn't start without you.",
            "My mood is like Ukrainian weather — changeable and unpredictable.",
            "You're like a passport — important but rarely used.",
            "My motivation is like elevator signal — exists but weak.",
            "You're like a selfie — look better with filters.",
            "Life is like a driving test — you take it several times until you win.",
            "You're like pizza — even when bad, still tasty.",
            "My schedule is like politicians' promises — theoretically exists.",
            "You're like cafe WiFi — everyone wants to connect.",
            "Life is like a game — the further you go, the harder the levels.",
            "You're like morning coffee — bitter but necessary.",
            "My budget is like a butterfly — beautiful but disappears quickly.",
            "You're like a phone charger — always lost when needed most.",
            "Life is like a bus — if you're late, wait for the next one.",
            "You're like vacation — long-awaited and fleeting.",
            "My sleep is like internet — when needed most, doesn't work.",
            "You're like Saturday — the best day of the week.",
            "Life is like a smartphone — the newer it is, the faster it drains.",
            "You're like a social media like — pleasant and free.",
            "My mood is like currency rates — changes daily.",
            "You're like home food — simple but the tastiest.",
            "Life is like a quest — many tasks but unknown reward.",
            "You're like morning jog — useful but difficult.",
            "My mind is like Google Chrome — 100 tabs open at once.",
            "You're like evening walk — calm and pleasant.",
            "Life is like GPS — sometimes leads you wrong way.",
            "You're like favorite song — can listen endlessly.",
            "My mood is like weather — changes every hour.",
            "You're like weekends — end too quickly.",
            "Life is like a video game — you have several lives but don't know how many.",
            "You're like morning exercise — needed but often skipped."
        ]
        
        # Track used jokes to avoid repetition
        self.used_jokes_uk = {}
        self.used_jokes_en = {}
        
        # Setup message handlers
        self.setup_handlers()
    
    def get_user_language(self, user_id: int) -> str:
        """Get user's preferred language"""
        return self.user_languages.get(user_id, 'uk')
    
    def create_main_keyboard(self, lang: str):
        """Create main menu keyboard"""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        
        if lang == 'uk':
            joke_btn = types.InlineKeyboardButton("😄 Жарт", callback_data="joke")
            ball_btn = types.InlineKeyboardButton("🔮 Магічна куля", callback_data="8ball")
            role_btn = types.InlineKeyboardButton("🎭 Хто ти сьогодні", callback_data="whoami")
            lang_btn = types.InlineKeyboardButton("🌐 English", callback_data="lang_en")
        else:
            joke_btn = types.InlineKeyboardButton("😄 Joke", callback_data="joke")
            ball_btn = types.InlineKeyboardButton("🔮 Magic 8-Ball", callback_data="8ball")
            role_btn = types.InlineKeyboardButton("🎭 Who are you today", callback_data="whoami")
            lang_btn = types.InlineKeyboardButton("🌐 Українська", callback_data="lang_uk")
            
        keyboard.add(joke_btn, ball_btn)
        keyboard.add(role_btn)
        keyboard.add(lang_btn)
        return keyboard
    
    def get_random_joke(self, user_id: int, lang: str) -> str:
        """Get random joke avoiding repetition"""
        if user_id not in self.used_jokes_uk:
            self.used_jokes_uk[user_id] = set()
        if user_id not in self.used_jokes_en:
            self.used_jokes_en[user_id] = set()
            
        jokes_list = self.jokes_uk if lang == 'uk' else self.jokes_en
        used_set = self.used_jokes_uk[user_id] if lang == 'uk' else self.used_jokes_en[user_id]
        
        # Reset if all jokes used
        if len(used_set) >= len(jokes_list):
            used_set.clear()
            
        # Get unused jokes
        available_jokes = [joke for joke in jokes_list if joke not in used_set]
        
        if not available_jokes:
            available_jokes = jokes_list
            used_set.clear()
            
        joke = random.choice(available_jokes)
        used_set.add(joke)
        return joke
    
    def get_random_role(self, user_id: int, lang: str) -> str:
        """Get random role avoiding immediate repetition"""
        roles_list = self.roles_uk if lang == 'uk' else self.roles_en
        role = random.choice(roles_list)
        
        # Avoid immediate repetition
        if user_id in self.last_roles and role == self.last_roles[user_id]:
            # Try to get different role
            for _ in range(5):  # Max 5 attempts
                new_role = random.choice(roles_list)
                if new_role != role:
                    role = new_role
                    break
        
        self.last_roles[user_id] = role
        return role
    
    def setup_handlers(self):
        """Setup bot message handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def handle_start(message):
            self.start_command(message)
        
        @self.bot.message_handler(commands=['fun', 'joke'])
        def handle_fun(message):
            self.fun_command(message)
            
        @self.bot.message_handler(commands=['8ball', 'ball'])
        def handle_8ball(message):
            self.eight_ball_command(message)
            
        @self.bot.message_handler(commands=['whoami'])
        def handle_whoami(message):
            self.whoami_command(message)
        
        @self.bot.message_handler(commands=['help'])
        def handle_help(message):
            self.help_command(message)
            
        @self.bot.message_handler(commands=['lang', 'language'])
        def handle_language(message):
            self.language_command(message)
            
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            self.handle_button_callback(call)
            
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            self.handle_unknown_message(message)
    
    def start_command(self, message):
        """Handle /start command"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            if lang == 'uk':
                welcome_message = (
                    "🇺🇦 Привіт! Я твій український бот для приколів! 👋\n\n"
                    "🎭 Що тебе цікавить?"
                )
            else:
                welcome_message = (
                    "🇺🇸 Hello! I'm your Ukrainian joke bot! 👋\n\n"
                    "🎭 What interests you?"
                )
                
            keyboard = self.create_main_keyboard(lang)
            self.bot.send_message(message.chat.id, welcome_message, reply_markup=keyboard)
            
            logger.info(f"Start command handled for user {user_id}")
        except Exception as e:
            logger.error(f"Error in start command: {e}")
            self.send_error_message(message)
    
    def fun_command(self, message):
        """Handle /fun and /joke commands"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            # Get random joke without repetition
            joke = self.get_random_joke(user_id, lang)
            
            # Create keyboard for more actions
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            if lang == 'uk':
                new_joke_btn = types.InlineKeyboardButton("😄 Ще жарт", callback_data="joke")
                ball_btn = types.InlineKeyboardButton("🔮 Магічна куля", callback_data="8ball")
                role_btn = types.InlineKeyboardButton("🎭 Хто ти сьогодні", callback_data="whoami")
                menu_btn = types.InlineKeyboardButton("📱 Меню", callback_data="menu")
            else:
                new_joke_btn = types.InlineKeyboardButton("😄 Another joke", callback_data="joke")
                ball_btn = types.InlineKeyboardButton("🔮 Magic 8-Ball", callback_data="8ball")
                role_btn = types.InlineKeyboardButton("🎭 Who are you today", callback_data="whoami")
                menu_btn = types.InlineKeyboardButton("📱 Menu", callback_data="menu")
                
            keyboard.add(new_joke_btn, ball_btn)
            keyboard.add(role_btn)
            keyboard.add(menu_btn)
            
            # Send joke with emoji
            formatted_joke = f"😄 {joke}"
            self.bot.send_message(message.chat.id, formatted_joke, reply_markup=keyboard)
            
            logger.info(f"Joke sent to user {user_id}")
        except Exception as e:
            logger.error(f"Error in fun command: {e}")
            self.send_error_message(message)
    
    def eight_ball_command(self, message):
        """Handle /8ball and /ball commands"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            # Get random magic 8-ball answer
            answers = self.magic_answers_uk if lang == 'uk' else self.magic_answers_en
            answer = random.choice(answers)
            
            # Create keyboard for more actions
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            if lang == 'uk':
                again_btn = types.InlineKeyboardButton("🔮 Знову", callback_data="8ball")
                joke_btn = types.InlineKeyboardButton("😄 Жарт", callback_data="joke")
                role_btn = types.InlineKeyboardButton("🎭 Хто ти сьогодні", callback_data="whoami")
                menu_btn = types.InlineKeyboardButton("📱 Меню", callback_data="menu")
                response_text = f"🔮 Магічна куля каже:\n\n{answer}"
            else:
                again_btn = types.InlineKeyboardButton("🔮 Again", callback_data="8ball")
                joke_btn = types.InlineKeyboardButton("😄 Joke", callback_data="joke")
                role_btn = types.InlineKeyboardButton("🎭 Who are you today", callback_data="whoami")
                menu_btn = types.InlineKeyboardButton("📱 Menu", callback_data="menu")
                response_text = f"🔮 Magic 8-Ball says:\n\n{answer}"
                
            keyboard.add(again_btn, joke_btn)
            keyboard.add(role_btn)
            keyboard.add(menu_btn)
            
            self.bot.send_message(message.chat.id, response_text, reply_markup=keyboard)
            
            logger.info(f"8-ball answer sent to user {user_id}")
        except Exception as e:
            logger.error(f"Error in 8ball command: {e}")
            self.send_error_message(message)
    
    def whoami_command(self, message):
        """Handle /whoami command - Who are you today game"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            # Get random role
            role = self.get_random_role(user_id, lang)
            
            # Create keyboard for more actions
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            if lang == 'uk':
                again_btn = types.InlineKeyboardButton("🎭 Знову", callback_data="whoami")
                joke_btn = types.InlineKeyboardButton("😄 Жарт", callback_data="joke")
                ball_btn = types.InlineKeyboardButton("🔮 Магічна куля", callback_data="8ball")
                menu_btn = types.InlineKeyboardButton("📱 Меню", callback_data="menu")
            else:
                again_btn = types.InlineKeyboardButton("🎭 Again", callback_data="whoami")
                joke_btn = types.InlineKeyboardButton("😄 Joke", callback_data="joke")
                ball_btn = types.InlineKeyboardButton("🔮 Magic 8-Ball", callback_data="8ball")
                menu_btn = types.InlineKeyboardButton("📱 Menu", callback_data="menu")
                
            keyboard.add(again_btn, joke_btn)
            keyboard.add(ball_btn)
            keyboard.add(menu_btn)
            
            self.bot.send_message(message.chat.id, role, reply_markup=keyboard)
            
            logger.info(f"Role sent to user {user_id}")
        except Exception as e:
            logger.error(f"Error in whoami command: {e}")
            self.send_error_message(message)
    
    def help_command(self, message):
        """Handle /help command"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            if lang == 'uk':
                help_message = (
                    "🤖 Допомога по боту:\n\n"
                    "📋 Доступні команди:\n"
                    "/start - почати роботу з ботом\n"
                    "/fun або /joke - отримати випадковий жарт\n"
                    "/8ball або /ball - магічна куля (задай питання)\n"
                    "/whoami - хто ти сьогодні (весела гра)\n"
                    "/lang - змінити мову\n"
                    "/help - показати це повідомлення\n\n"
                    "💡 Використовуй кнопки для зручності! 😊"
                )
            else:
                help_message = (
                    "🤖 Bot help:\n\n"
                    "📋 Available commands:\n"
                    "/start - start working with bot\n"
                    "/fun or /joke - get random joke\n"
                    "/8ball or /ball - magic 8-ball (ask a question)\n"
                    "/whoami - who are you today (fun game)\n"
                    "/lang - change language\n"
                    "/help - show this message\n\n"
                    "💡 Use buttons for convenience! 😊"
                )
                
            keyboard = self.create_main_keyboard(lang)
            self.bot.send_message(message.chat.id, help_message, reply_markup=keyboard)
            
            logger.info(f"Help command handled for user {user_id}")
        except Exception as e:
            logger.error(f"Error in help command: {e}")
            self.send_error_message(message)
    
    def language_command(self, message):
        """Handle /lang command"""        
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            # Create language selection keyboard
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            uk_btn = types.InlineKeyboardButton("🇺🇦 Українська", callback_data="lang_uk")
            en_btn = types.InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            back_btn = types.InlineKeyboardButton("⬅️ Назад" if lang == 'uk' else "⬅️ Back", callback_data="menu")
            
            keyboard.add(uk_btn, en_btn)
            keyboard.add(back_btn)
            
            if lang == 'uk':
                text = "🌐 Оберіть мову:"
            else:
                text = "🌐 Choose language:"
                
            self.bot.send_message(message.chat.id, text, reply_markup=keyboard)
            
            logger.info(f"Language command handled for user {user_id}")
        except Exception as e:
            logger.error(f"Error in language command: {e}")
            self.send_error_message(message)
    
    def handle_button_callback(self, call):
        """Handle inline keyboard button callbacks"""        
        try:
            user_id = call.from_user.id
            chat_id = call.message.chat.id
            data = call.data
            
            if data == "joke":
                lang = self.get_user_language(user_id)
                joke = self.get_random_joke(user_id, lang)
                
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if lang == 'uk':
                    new_joke_btn = types.InlineKeyboardButton("😄 Ще жарт", callback_data="joke")
                    ball_btn = types.InlineKeyboardButton("🔮 Магічна куля", callback_data="8ball")
                    role_btn = types.InlineKeyboardButton("🎭 Хто ти сьогодні", callback_data="whoami")
                    menu_btn = types.InlineKeyboardButton("📱 Меню", callback_data="menu")
                else:
                    new_joke_btn = types.InlineKeyboardButton("😄 Another joke", callback_data="joke")
                    ball_btn = types.InlineKeyboardButton("🔮 Magic 8-Ball", callback_data="8ball")
                    role_btn = types.InlineKeyboardButton("🎭 Who are you today", callback_data="whoami")
                    menu_btn = types.InlineKeyboardButton("📱 Menu", callback_data="menu")
                    
                keyboard.add(new_joke_btn, ball_btn)
                keyboard.add(role_btn)
                keyboard.add(menu_btn)
                
                formatted_joke = f"😄 {joke}"
                self.bot.send_message(chat_id, formatted_joke, reply_markup=keyboard)
                
            elif data == "8ball":
                lang = self.get_user_language(user_id)
                answers = self.magic_answers_uk if lang == 'uk' else self.magic_answers_en
                answer = random.choice(answers)
                
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if lang == 'uk':
                    again_btn = types.InlineKeyboardButton("🔮 Знову", callback_data="8ball")
                    joke_btn = types.InlineKeyboardButton("😄 Жарт", callback_data="joke")
                    role_btn = types.InlineKeyboardButton("🎭 Хто ти сьогодні", callback_data="whoami")
                    menu_btn = types.InlineKeyboardButton("📱 Меню", callback_data="menu")
                    response_text = f"🔮 Магічна куля каже:\n\n{answer}"
                else:
                    again_btn = types.InlineKeyboardButton("🔮 Again", callback_data="8ball")
                    joke_btn = types.InlineKeyboardButton("😄 Joke", callback_data="joke")
                    role_btn = types.InlineKeyboardButton("🎭 Who are you today", callback_data="whoami")
                    menu_btn = types.InlineKeyboardButton("📱 Menu", callback_data="menu")
                    response_text = f"🔮 Magic 8-Ball says:\n\n{answer}"
                    
                keyboard.add(again_btn, joke_btn)
                keyboard.add(role_btn)
                keyboard.add(menu_btn)
                
                self.bot.send_message(chat_id, response_text, reply_markup=keyboard)
                
            elif data == "whoami":
                lang = self.get_user_language(user_id)
                role = self.get_random_role(user_id, lang)
                
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                if lang == 'uk':
                    again_btn = types.InlineKeyboardButton("🎭 Знову", callback_data="whoami")
                    joke_btn = types.InlineKeyboardButton("😄 Жарт", callback_data="joke")
                    ball_btn = types.InlineKeyboardButton("🔮 Магічна куля", callback_data="8ball")
                    menu_btn = types.InlineKeyboardButton("📱 Меню", callback_data="menu")
                else:
                    again_btn = types.InlineKeyboardButton("🎭 Again", callback_data="whoami")
                    joke_btn = types.InlineKeyboardButton("😄 Joke", callback_data="joke")
                    ball_btn = types.InlineKeyboardButton("🔮 Magic 8-Ball", callback_data="8ball")
                    menu_btn = types.InlineKeyboardButton("📱 Menu", callback_data="menu")
                    
                keyboard.add(again_btn, joke_btn)
                keyboard.add(ball_btn)
                keyboard.add(menu_btn)
                
                self.bot.send_message(chat_id, role, reply_markup=keyboard)
                
            elif data == "menu":
                lang = self.get_user_language(user_id)
                
                if lang == 'uk':
                    welcome_message = (
                        "🇺🇦 Привіт! Я твій український бот для приколів! 👋\n\n"
                        "🎭 Що тебе цікавить?"
                    )
                else:
                    welcome_message = (
                        "🇺🇸 Hello! I'm your Ukrainian joke bot! 👋\n\n"
                        "🎭 What interests you?"
                    )
                    
                keyboard = self.create_main_keyboard(lang)
                self.bot.send_message(chat_id, welcome_message, reply_markup=keyboard)
                
            elif data.startswith("lang_"):
                new_lang = data.split("_")[1]
                self.user_languages[user_id] = new_lang
                
                if new_lang == 'uk':
                    response = "🇺🇦 Мова змінена на українську!"
                else:
                    response = "🇺🇸 Language changed to English!"
                    
                keyboard = self.create_main_keyboard(new_lang)
                self.bot.send_message(chat_id, response, reply_markup=keyboard)
                
            # Answer callback to remove loading animation
            self.bot.answer_callback_query(call.id)
            
            logger.info(f"Button callback handled: {data} for user {user_id}")
        except Exception as e:
            logger.error(f"Error in button callback: {e}")
            try:
                self.bot.answer_callback_query(call.id, "Error occurred")
            except:
                pass

    def handle_unknown_message(self, message):
        """Handle unknown messages"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            if lang == 'uk':
                response = (
                    "🤔 Я не розумію цю команду.\n"
                    "Використовуй кнопки нижче! 😊"
                )
            else:
                response = (
                    "🤔 I don't understand this command.\n"
                    "Use the buttons below! 😊"
                )
                
            keyboard = self.create_main_keyboard(lang)
            self.bot.send_message(message.chat.id, response, reply_markup=keyboard)
            
            logger.info(f"Unknown message handled for user {user_id}")
        except Exception as e:
            logger.error(f"Error in unknown message handler: {e}")
            self.send_error_message(message)
    
    def send_error_message(self, message):
        """Send error message to user"""
        try:
            user_id = message.from_user.id
            lang = self.get_user_language(user_id)
            
            if lang == 'uk':
                error_msg = (
                    "😔 Вибачте, сталася помилка.\n"
                    "Спробуйте пізніше або натисніть кнопку нижче"
                )
            else:
                error_msg = (
                    "😔 Sorry, an error occurred.\n"
                    "Try again later or press the button below"
                )
                
            keyboard = self.create_main_keyboard(lang)
            self.bot.send_message(message.chat.id, error_msg, reply_markup=keyboard)
        except Exception as e:
            logger.error(f"Failed to send error message: {e}")
    
    def run(self):
        """Start bot polling"""
        logger.info("Starting bot...")
        
        while True:
            try:
                # Start polling with error handling
                self.bot.infinity_polling(
                    timeout=10,
                    long_polling_timeout=5,
                    none_stop=True,
                    interval=0
                )
            except Exception as e:
                logger.error(f"Bot polling error: {e}")
                logger.info("Restarting bot in 5 seconds...")
                time.sleep(5)

def main():
    """Main function to run the bot"""
    try:
        # Create and run bot
        bot = UkrainianJokeBot()
        print("🤖 Український бот приколів запущений!")
        print("💡 Натисніть Ctrl+C для зупинки")
        bot.run()
    except KeyboardInterrupt:
        print("\n👋 Бот зупинений користувачем")
        logger.info("Bot stopped by user")
    except Exception as e:
        print(f"❌ Критична помилка: {e}")
        logger.error(f"Critical error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
