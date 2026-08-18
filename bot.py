import os
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, CommandHandler, filters

BOT_TOKEN = os.environ["BOT_TOKEN"]

# شناسه عددی ادمینی که اجازه کنترل ربات را دارد
OWNER_ID = int(os.environ["OWNER_ID"])

locked = False


async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global locked

    if update.effective_user and update.effective_user.id == OWNER_ID:
        locked = True
        await update.message.reply_text("🔒 حالت قفل فعال شد.")


async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global locked

    if update.effective_user and update.effective_user.id == OWNER_ID:
        locked = False
        await update.message.reply_text("🔓 حالت قفل غیرفعال شد.")


async def channel_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not locked:
        return

    message = update.channel_post

    if message:
        try:
            await context.bot.delete_message(
                chat_id=message.chat_id,
                message_id=message.message_id
            )
        except Exception as e:
            print("Delete error:", e)


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("lock", lock))
    app.add_handler(CommandHandler("unlock", unlock))

    app.add_handler(
        MessageHandler(filters.ALL, channel_post)
    )

    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
