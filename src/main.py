from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from game import Game

TOKEN = '6075437680:AAHOBKLBQY5l5fmnWYwafJNYN_SWFMew5Vk'
SEARCHING = []
GAMES = []
PLAYER_TO_GAME = dict()
GAME_COUNTER = 0


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Привет. Это бот для игры в "четыре в ряд". Чтобы найти соперника, введите '
                                    'команду /find_opponent')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Чтобы найти соперника, введите команду /find_opponent\nЧтобы играть, отправьте '
                                    'цифру от 1 до 7 после указания от бота.')


async def find_opponent_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global GAME_COUNTER
    player_id = update.message.chat_id
    if len(SEARCHING) != 0:
        if SEARCHING[0] == player_id:
            await update.message.reply_text('Вы уже начинали поиск соперника. Пожалуйста, подождите...')
        else:
            player_waiting_id = SEARCHING[0]
            GAME_COUNTER += 1
            new_game = Game(player_waiting_id, player_id, GAME_COUNTER)
            GAMES.append(new_game)
            SEARCHING.pop()
            PLAYER_TO_GAME.update({player_id: GAME_COUNTER, player_waiting_id: GAME_COUNTER})
            await context.bot.send_message(chat_id=player_waiting_id, text='Соперник найден. Игра начинается...\nВы '
                                                                           'ходите первым\n')
            await context.bot.send_message(chat_id=player_waiting_id, text="Ваш ход...")
            await update.message.reply_text('Соперник найден. Игра начинается...')
    else:
        SEARCHING.append(player_id)
        await update.message.reply_text('Поиск соперника начат. Пожалуйста, подождите...')


def get_game(game_id):
    for j in range(len(GAMES)):
        if GAMES[j].game_id == game_id:
            return j
    return -1


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flag = True
    text = update.message.text
    player_id = update.message.chat_id

    print(f'User ({player_id}): "{text}"')

    response = ""
    game_id = 0
    try:
        game_id = PLAYER_TO_GAME[player_id]
    except BaseException:
        response = 'Вы ещё не играете.'
        flag = False
        await update.message.reply_text(response)

    wanted_column = 0
    if flag:
        try:
            wanted_column = int(text) - 1
        except BaseException:
            response = 'Бот вас не понимает. Введите число от 1 до 7'
            flag = False
            await update.message.reply_text(response)

    if flag:
        j = get_game(game_id)
        response = GAMES[j].make_a_move(wanted_column, player_id)
        await update.message.reply_text(response)
        if response != 'Сейчас ход соперника...' and response != 'Невозможный ход. Попробуйте другой.':
            await context.bot.send_message(chat_id=GAMES[j].turn, text=response)
            if GAMES[j].game_over:
                PLAYER_TO_GAME.pop(GAMES[j].player_1_id)
                PLAYER_TO_GAME.pop(GAMES[j].player_2_id)
                GAMES.pop(j)
            else:
                await context.bot.send_message(chat_id=GAMES[j].turn, text="Ваш ход...")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('find_opponent', find_opponent_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=1)
