import logging
import os

from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from get_pretty import get_pretty
from transactions import transactions_with_status_generator

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

START, TRANSACTIONS = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""

    await update.message.reply_text(
        "Hi! Please send me message with the next values: address, api_key, start_block, end_block, page, offset, sort."
    )

    return TRANSACTIONS


async def transactions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    data = update.message.text.split(", ")
    transactions_generator = transactions_with_status_generator(*data)
    for transaction in transactions_generator:
        await update.message.reply_text(get_pretty(transaction))

    return START


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    application = (
        Application.builder()
        .token(os.getenv("BOT_TOKEN"))
        .build()
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TRANSACTIONS: [MessageHandler(filters.TEXT, transactions)],
            START: [
                CommandHandler("start", start),
                MessageHandler(filters.TEXT, transactions),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
