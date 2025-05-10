from aiogram import Router

from . import (
    menu,
    captcha
)


router = Router()
router.include_router(menu.router)
router.include_router(captcha.router)
