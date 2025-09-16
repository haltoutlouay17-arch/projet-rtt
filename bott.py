
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

TOKEN = "8135360979:AAHptiw9OS5BHjrw57dKdw9kcgJe6IaKUf0"
ADMIN_ID = 8437400033  # Ton vrai ID Telegram
SIGNAL_LINK = "https://signal.me/#p/+scarface.60"  # Lien vers ton Signal

# Produits avec prix par quantité
products = {
    "Cali Mac 1": {"description": "Top Shelf Premium Canadian Mac 1", "prix": {"5g": "50€", "10g": "90€", "25g": "150€", "50g": "280€", "100g": "550€"}},
    "Cali RS11": {"description": "Top Shelf Premium RS 11", "prix": {"5g": "50€", "10g": "90€", "25g": "150€", "50g": "280€", "100g": "550€"}},
    "Amnesia Haze": {"description": "Amnesia qualité Boerenjongens", "prix": {"5g": "40€", "10g": "80€", "25g": "140€", "50g": "260€", "100g": "520€"}},
    "Hash Static Frozen": {"description": "Top Moroccans Premium Pollens", "prix": {"5g": "40€", "10g": "80€", "25g": "140€", "50g": "260€", "100g": "480€"}}
}

# États ConversationHandler
QUANTITY, ADDRESS, PHONE = range(3)
user_order = {}

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(prod, callback_data=prod)] for prod in products]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🐾 Bienvenue au Mini Zoo ! Choisis un produit :", reply_markup=reply_markup)

# Cliquer sur produit → proposer quantités
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    prod = query.data
    user_order[query.from_user.id] = {"produit": prod}
    keyboard = [[InlineKeyboardButton(f"{q} - {products[prod]['prix'][q]}", callback_data=q)] for q in products[prod]['prix']]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(f"Choisissez la quantité pour {prod} :", reply_markup=reply_markup)
    return QUANTITY

# Choisir quantité
async def choose_quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    quantity = query.data
    user_order[query.from_user.id]["quantité"] = quantity
    await query.message.reply_text("📍 Veuillez entrer votre adresse complète :")
    return ADDRESS

# Récupérer l'adresse
async def get_address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_order[update.message.from_user.id]["adresse"] = update.message.text
    await update.message.reply_text("📞 Veuillez entrer votre numéro de téléphone (10 chiffres) :")
    return PHONE

# Récupérer le téléphone et envoyer à l'admin
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone = update.message.text
    if not phone.isdigit() or len(phone) < 10:
        await update.message.reply_text("❌ Numéro invalide. Veuillez entrer un numéro valide de 10 chiffres :")
        return PHONE
    
    user_order[update.message.from_user.id]["phone"] = phone
    order_info = user_order[update.message.from_user.id]
    
    # Message à l'admin
    msg = (
        f"📦 Nouvelle commande !\n\n"
        f"Produit : {order_info['produit']}\n"
        f"Quantité : {order_info['quantité']}\n"
        f"Adresse : {order_info['adresse']}\n"
        f"Téléphone : {order_info['phone']}\n"
        f"Client : {update.message.from_user.first_name} ({update.message.from_user.id})\n\n"
        f"📲 Contact Signal : {SIGNAL_LINK}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg)
    
    await update.message.reply_text("✅ Votre commande a été reçue ! Nous vous contacterons bientôt.")
    user_order.pop(update.message.from_user.id)
    return ConversationHandler.END

# Annuler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Commande annulée.")
    user_order.pop(update.message.from_user.id, None)
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button, pattern="^.*$")],
        states={
            QUANTITY: [CallbackQueryHandler(choose_quantity)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    print("✅ Bot lancé...")
    app.run_polling()

if __name__ == "__main__":
    main()