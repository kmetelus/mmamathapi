import json
import os
from dotenv import load_dotenv
from py2neo import Graph, Node, Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo
from py2neo.matching import *

# Example shortest path query
# MATCH(hc:Fighter{name: 'henry cejudo'}),(dc:Fighter{name: 'daniel cormier'}), p = shortestPath((hc)-[:HAS_BEATEN*]->(dc)) return p
def init_fighter(db, fighter_name):
    tx = db.begin()
    new_node = Node('Fighter', name=fighter_name, nickname='')
    tx.create(new_node)
    tx.commit()
    tx.finished()
    return new_node

def get_or_create_fighter(db, nm, fighter_name):
    fighter = nm.match('Fighter', name=fighter_name)
    if fighter.exists():
        return fighter.first()
    else:
        return init_fighter(db, fighter_name)

def update_fighter(db, fighter, nickname):
    tx = db.begin()
    fighter.nickname = nickname
    db.push(fighter)
    tx.commit()
    tx.finished()

def create_relationship(db, winner, loser):
    HAS_BEATEN = Relationship.type("HAS_BEATEN")
    db.merge(HAS_BEATEN(winner, loser))

def establish_wins(db, nm, fighter, wins):
    for loser_name in wins:
        loser = get_or_create_fighter(db, nm, loser_name.lower())
        create_relationship(db, fighter, loser)

def create_database_node(db, nm, block):

    name = block['name'].lower()
    nickname = block['nickname'].lower()
    wins = block['wins']
    fighter = get_or_create_fighter(db, nm, name)
    if nickname:
        update_fighter(db, fighter, nickname)
    establish_wins(db, nm, fighter, wins)


def initialize_neo4j_database():
    load_dotenv()
    db = Graph(os.getenv('DB_ACCESS_STRING'), auth=(os.getenv('DB_USERNAME'), os.getenv('DB_PASSWORD')))
    nm = NodeMatcher(db)
    with open('mmamathapi\\fighterData.txt') as json_file:
        fighter_data = json.load(json_file)
        for section in fighter_data['data']:
            for block in section:
                create_database_node(db, nm, block)


def main():
    initialize_neo4j_database()

if __name__ == "__main__":
  main()