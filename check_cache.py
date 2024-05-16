import json
import sys
import argparse

def print_latest(filename, latest=None):
    try:
        with open(filename, 'r') as f:
            d = json.load(f)

        if latest is not None and latest > 0:
            d = d[-latest:]

        for obj in d:
            print (obj)
            print ()

    except FileNotFoundError:
        print (f"Error: File {filename} not found.")
    except json.JSONDecodeError:
        print (f"Error: File {filename} is not a valid JSON")
    except ValueError as e:
        print (f"Error {e}")
    except Exception as e:
        print (f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print elements from a JSON file")
    parser.add_argument('filename', help="The JSON file containing list of dictionary objects")
    parser.add_argument('-latest', type=int, help="Number of latest elements to print")

    args = parser.parse_args()

    filename = args.filename
    latest = args.latest

    print_latest(filename, latest)
