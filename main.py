from neo4j import GraphDatabase
from connection import Connection, get_connection 
import seed_data


def main():
    seed_data.interactive_menu()

if __name__ == "__main__":
    main()