def confirmTxMarkup(txId):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Confirm", callback_data = 'confirmed ' + str(txId)))
    return markup
