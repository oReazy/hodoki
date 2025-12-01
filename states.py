# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

import asyncio, logging

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

from modules import database, registration, mainMenu, settings

# ———————————————————————————————————————————————————————————————————————————————————————————————————————————————

STATES = {
    'registration.registration_1': registration.registration_1,
    'registration.registration_1_check': registration.registration_1_check,
    'mainMenu.Show': mainMenu.Show,
    'settings.Show': settings.Show
}