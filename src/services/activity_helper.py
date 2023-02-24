from activity import detect_activity , read_input

def main():
    # Read the input file
    df = read_input('input.csv')
    # Detect the activity
    act , pred = detect_activity(df)
    print(act , pred) 

if __name__ == '__main__':
    main()