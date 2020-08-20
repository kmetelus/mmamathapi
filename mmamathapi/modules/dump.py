import simplejson

from scraper import get_all_fighters

def main():
    fighter_data = open('../fighterData.json', 'w')
    json = { 'data' : get_all_fighters() }
    fighter_data.write(simplejson.dumps(json, indent = 4, sort_keys=True ))
    fighter_data.close()

if __name__ == "__main__":
    main()