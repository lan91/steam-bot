import Teleme
import Twitme 


if __name__ == '__main__':
	Twitme.get_all_tweets("steam_games")
	data = Twitme.import_data('steam_games_tweets.csv')
	Twitme.get_basic_statistics(data)


