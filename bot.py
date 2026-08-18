import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = 5049250693

locked = False


async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global locked

    if update.effective_user and update.effective_user.id == OWNER_ID:
        locked = True
        await update.message.reply_text("🔒 Lock فعال شد.")


async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global locked

    if update.effective_user and update.effective_user.id == OWNER_ID:
        locked = False
        await update.message.reply_text("🔓 Unlock فعال شد.")


async def inspect_channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.channel_post

    if not message:
        return

    # اطلاعاتی که تلگرام برای نویسنده پست به ربات داده
    print("========== CHANNEL POST ==========")
    print("Message ID:", message.message_id)
    print("Author signature:", repr(message.author_signature))
    print("Sender chat:", message.sender_chat)
    print("==================================")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))

    app.add_handler(
        MessageHandler(
            filters.UpdateType.CHANNEL_POST,
            inspect_channel_post
        )
    )

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
