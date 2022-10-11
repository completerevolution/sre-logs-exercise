import json
import sys
import numpy as np
import pandas as pd


all_records = []


def open_file(filename):
    with open(filename, "r") as f:
        all_lines = []

        for newline in f:
            all_lines.append((json.loads(newline)))

    return all_lines


def calculate_mode_duration(records_to_calculate):

    record_frequency_count = {}

    for record in records_to_calculate:

        duration_value = record["Duration"]

        record_frequency_count[duration_value] = (
            record_frequency_count.get(duration_value, 0) + 1
        )

    most_frequent = max(record_frequency_count.values())

    modes = [
        key
        for key, duration_value in record_frequency_count.items()
        if duration_value == most_frequent
    ]

    print("Unique duration count: " + str(len(record_frequency_count.items())))
    print("")
    print(
        "Highest duration: "
        + str(sorted(record_frequency_count.keys(), reverse=True)[0])
        + " seconds"
    )
    print(
        "Highest frequency: "
        + str(
            record_frequency_count[
                sorted(record_frequency_count.keys(), reverse=True)[0]
            ]
        )
    )
    print("")
    print(
        "Lowest duration: "
        + str(sorted(record_frequency_count.keys())[0])
        + " milliseconds"
    )
    print(
        "Highest frequency: "
        + str(record_frequency_count[sorted(record_frequency_count.keys())[0]])
    )
    print("")
    print("Mode duration value: " + str(modes[0]) + " milliseconds")
    print("Mode duration frequency: " + str(record_frequency_count[modes[0]]))

    return modes


def calculate_mean_duration(records_to_calculate):
    record_frequency_count = len(records_to_calculate)
    record_total_value = 0

    for record in records_to_calculate:
        duration_value = record["Duration"]

        record_total_value = record_total_value + duration_value

    print("Total value: " + str(record_total_value))
    print("Total count: " + str(record_frequency_count))

    print("Mean value (int): " + str(int(record_total_value / record_frequency_count)))


def get_std_dev(ls):
    """
    Credit: https://datascienceparichay.com/article/calculate-standard-deviation-in-python/
    """
    n = len(ls)
    mean = sum(ls) / n
    var = sum((x - mean) ** 2 for x in ls) / n
    std_dev = var**0.5
    return std_dev


def create_list_of_duration_values(records_to_calculate):

    duration_list = []

    for record in records_to_calculate:
        duration_value = record["Duration"]

        duration_list.append(duration_value)

    return duration_list


def find_records_above_percentile(records_to_calculate, percentile_to_calculate):

    records_above_percentile = []

    for record in records_to_calculate:
        duration_value = record["Duration"]

        if duration_value > percentile_to_calculate:
            records_above_percentile.append(record)

    return records_above_percentile


def calculate_percentile(all_records, percentile_input):

    global percentile_value

    list_to_process = create_list_of_duration_values(all_records)
    percentile_value = int(np.percentile(list_to_process, percentile_input))

    list_of_records_above_percentile = find_records_above_percentile(
        all_records, percentile_value
    )

    print("========== Debug ==========")
    calculate_mean_duration(all_records)
    print("========== Debug ==========")
    calculate_mode_duration(all_records)
    print("========== Debug ==========")
    print("Total records count: " + str(len(all_records)))
    print(str(percentile_input) + " percentile value: " + str(percentile_value))
    print(
        "Number of records in "
        + str(percentile_input)
        + " percentile: "
        + str(len(list_of_records_above_percentile))
    )
    print("========== Debug ==========")

    return calculate_time_groups(list_of_records_above_percentile)


def calculate_time_groups(records_to_calculate):

    mode_duration_value = calculate_mode_duration(all_records)

    pd.set_option(
        "display.max_rows", None
    )  # Thanks Nick Kosmicki // Mews Data Team lead

    records = pd.DataFrame(records_to_calculate)

    records["TimeStamp"] = pd.to_datetime(
        records["TimeStamp"]
    )  # Thanks Nick Kosmicki // Mews Data Team lead

    export_list = records.groupby(pd.Grouper(key="TimeStamp", axis=0, freq="5min"))

    print("========== Debug ==========")
    print("Display count of records in dataframe")
    print(str(export_list.count()))
    print("========== End Debug ==========")
    print("\n\n\n\n\n\n")

    print("========= Start Results =====")
    for i in export_list:

        i_to_dict = i[1].to_dict("records")

        print("Window of 5 minutes: " + str(i[0]))
        print("Duration exceeded: " + str(percentile_value) + " milliseconds")
        print("Mode duration value: " + str(mode_duration_value[0]) + " milliseconds")
        print("Endpoint:" + i_to_dict[0]["Endpoint"])
        print("Failure count: " + str(len(i_to_dict)) + "\n")

    print("======== End of Results =====")


# Go! Go! Go!

# Basic sanitising
if len(sys.argv) == 1 or len(sys.argv) >= 3:
    print("Please only supply a percentile value.")
    print("Example: " + str(sys.argv[0]) + " 99.9")
    quit()
elif float(sys.argv[1]) >= 100:
    print("Please only supply a percentile value between 1-99")
    print("Example: " + str(sys.argv[0]) + " 99.9")
    quit()

percentile_input = float(sys.argv[1])

#  Debug - small test data // original data set
all_records = open_file("original-data/logs.txt")
# all_records = open_file("logs.json")
calculate_percentile(all_records, percentile_input)
