from loguru import logger


class UserLog:
    """
    Logging for user's actions
    """

    def __init__(self, user_id: int, **kwargs) -> None:
        """
        Initialization for user's log

        :param user_id: Telegram user ID
        :param kwargs: Additional data to display
        """

        self.user_id = user_id
        self.display_data = " ".join([
            f"({key}: {value})" for key, value in kwargs.items()
        ])

    def log(self, message: str) -> None:
        """
        Display user's info

        :param message: Message to display
        """

        logger.info(f"{message} {self.display_data}", source=self.user_id)
