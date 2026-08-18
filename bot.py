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
        await update.message.reply_text("🔒 کانال قفل شد.\nهمه پست‌های جدید پاک می‌شوند.")


async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global locked

    if update.effective_user and update.effective_user.id == OWNER_ID:
        locked = False
        await update.message.reply_text("🔓 کانال آزاد شد.")


async def delete_channel_posts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not locked:
        return

    message = update.channel_post

    if message:
        try:
            await context.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message.message_id
            )
            print(f"Deleted message {message.message_id}")
        except Exception as e:
            print(f"Delete error: {e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # کنترل ربات فقط توسط صاحب ربات
    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))

    # دریافت پست‌های کانال
    app.add_handler(
        MessageHandler(filters.UpdateType.CHANNEL_POST, delete_channel_posts)
    )

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
