 
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# === Token du bot ===
TOKEN = "8135360979:AAHptiw9OS5BHjrw57dKdw9kcgJe6IaKUf0"

# === Liste des produits ===
products = {
    "Cali Mac 1": {
        "description": "Top Shelf Premium Canadian Mac 1",
        "prix": "5g - 50€\n10g - 90€\n25g - 150€\n50g - 280€\n100g - 550€",
        "video": "https://example.com/video_cali_mac.mp4"
    },
    "Cali RS11": {
        "description": "Top Shelf Premium RS 11",
        "prix": "5g - 50€\n10g - 90€\n25g - 150€\n50g - 280€\n100g - 550€",
        "video": "https://example.com/video_cali_rs11.mp4"
    },
    "Amnesia Haze": {
        "description": "Amnesia qualité Boerenjongens",
        "prix": "5g - 40€\n10g - 80€\n25g - 140€\n50g - 260€\n100g - 520€",
        "video": "https://example.com/video_amnesia_haze.mp4"
    },
    "Hash Static Frozen": {
        "description": "Top Moroccans Premium Pollens",
        "prix": "5g - 40€\n10g - 80€\n25g - 140€\n50g - 260€\n100g - 480€",
        "video": "https://example.com/video_hash_static.mp4"
    }
}

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(prod, callback_data=prod)] for prod in products]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🐾 Bienvenue au Mini Zoo ! Choisis un produit :", reply_markup=reply_markup)

# === Gestion des clics sur les produits ===
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prod = query.data
    info = products[prod]

    text = f"🎬 {prod}\n\n{info['description']}\n\n💰 Tarifs :\n{info['prix']}"
    keyboard = [[InlineKeyboardButton("🛒 Commander", callback_data=f"order_{prod}")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.reply_text(text, reply_markup=reply_markup)
    # Si tu veux envoyer la vidéo, décommente la ligne suivante et mets le vrai lien
    # await query.message.reply_video(video=info['video'], caption=text, reply_markup=reply_markup)

# === Gestion des commandes ===
async def order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prod = query.data.replace("order_", "")
    await query.message.reply_text(f"✅ Vous avez choisi de commander : {prod}\nNous vous contacterons pour finaliser la commande !")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(order, pattern=r"^order_"))
    app.add_handler(CallbackQueryHandler(button))

    print("✅ Bot lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()
git status
git IndentationError
git add
git commit -m "version initiale du bot "
"" git remomte add origin https://github.com/haltoutlouay17-arch/projet-rtt.git
