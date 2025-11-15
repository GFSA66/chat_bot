from telebot import types

# Список вопросов, включая *Секретка* для форматирования
question_list = ['*Секретка*', 'привет', 'как дела', 'проверка', 'хз']

# Создание стандартной клавиатуры для обычных кнопок (ReplyKeyboardMarkup)
questions = types.ReplyKeyboardMarkup(resize_keyboard=True)

# Создание клавиатуры для inline кнопок, где row_width=2 (для двух кнопок в одном ряду)
InLineQuestions = types.InlineKeyboardMarkup(row_width=2)  # Устанавливаем 2 кнопки на одну строку

# Проходим по списку вопросов и добавляем кнопки в обе клавиатуры
for question in question_list:
    ################ Стандартная клавиатура #################
    # Добавляем обычную кнопку на стандартную клавиатуру
    questions.add(types.KeyboardButton(question))
    
    ################ Inline клавиатура ################
    # Добавляем inline кнопку на inline клавиатуру с соответствующим callback_data
    InLineQuestions.add(types.InlineKeyboardButton(text=question, callback_data=question))

# Теперь, клавиатура `questions` будет вертикальной, а клавиатура `InLineQuestions` будет иметь две кнопки в строке
