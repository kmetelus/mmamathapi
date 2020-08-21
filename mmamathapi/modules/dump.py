import ujson

from scraper import try_get_all_fighters

def main():
    fighter_data = open('../fighterData.txt', 'w')
    json = { 'data' : try_get_all_fighters() }
    fighter_data.write(ujson.dumps(json, indent = 4))
    fighter_data.close()

if __name__ == "__main__":
    main()