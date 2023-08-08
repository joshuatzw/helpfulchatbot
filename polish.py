def polish_text(update):
     # raw text that was sent from user
    text = update.message.text

    # splitting the sentence into a list, and removing the first word e.g. "/ask", then join
    text_list = text.split()
    text_list.pop(0)
    text_to_ask = ' '.join(text_list)
    return text_to_ask