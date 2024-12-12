import argparse
import subprocess
import json

def main():
    parser = argparse.ArgumentParser(description='Script to execute a query with given arguments.')
    parser.add_argument('--city', required=True, help='City name')
    parser.add_argument('--commit', action='store_true', help='Commit flag')
    parser.add_argument('--incorrectOrder', action='store_true', help='Incorrect order flag')
    
    try:
        args = parser.parse_args()
    except SystemExit:
        parser.print_help()
        print("\nError: Invalid arguments provided.")
        exit(1)
    
    data = {
        "city": args.city,
        "ordenincorrecto": args.incorrectOrder,
        "commitintermedio": args.commit
    }
    
    response = subprocess.run(
        ['curl', '-X', 'POST', 'http://127.0.0.1:5000/borraCiudad', '-H', 'Content-Type: application/json', '-d', json.dumps(data)],
        capture_output=True,
        text=True
    )
    
    print(response.stdout)

if __name__ == '__main__':
    main()