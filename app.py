import modules.init_database as db_init
import bot.bot as bot

def main():
    db_init.main()
    bot.start_bot()    
    
if __name__ == '__main__':
    main()