from collections import Counter

def rowCounter(input_data):
    header = input_data[0]
    # A Counter használata az elemek számolásához
    counter = Counter([item[0] for item in input_data[1:]])

    # Átalakítás a kívánt kimenetre
    output_data = [[elem, count] for elem, count in counter.items()]

    return [header] + output_data
