import datetime
import json
import numpy as np
import pandas as pd
from IPython.display import display
from dateutil import parser


all_records = []

def open_file(filename):
    with open(filename, "r") as f:
        all_lines = []
        
        for newline in f:
            all_lines.append((json.loads(newline)))
        
    return all_lines


# def calculate_maximum_duration_diff(records_to_calculate):
#     """
#     Function to calculate the largest diff between two Duration values.
#     Input: new record
#     """

#     previous_record = None
#     master_list_of_pairs = []
#     highest_diff_pair = None
#     highest_diff = 0

#     for record in records_to_calculate:
        
#         # Initial run only
#         if previous_record == None:
#             previous_record = record

#         diff_between_previous_current = record["Duration"] - previous_record["Duration"]
#         if diff_between_previous_current > 0:

#             temp_tuple = (previous_record, record, diff_between_previous_current)
            
#             if diff_between_previous_current > highest_diff:
#                 highest_diff = diff_between_previous_current
#                 highest_diff_pair = (previous_record, record, highest_diff)
            
#             master_list_of_pairs.append(temp_tuple)
#             previous_record = record
            

#     print("List of pairs: " + str(master_list_of_pairs))
#     print("")
#     print("Highest diff pair: " + str(highest_diff_pair[0]) + " and " + str(highest_diff_pair[1]))

# def convert_timestamp_to_epoch(records_to_convert):
    
#     list_of_conveted_timestamps = []

#     for record in records_to_convert:
#         new_datetime_timestamp = parser.isoparse(record["TimeStamp"])

#         # {"TimeStamp":"2021-08-26T13:00:00","Endpoint":"/api/reservations/add","StatusCode":200,"Duration":500}
#         # {"TimeStamp":"2021-08-26T13:00:00.064","Endpoint":"/api/reservations/add","StatusCode":200,"Duration":511}
#         try:
#             new_format = datetime.datetime.strptime(str(new_datetime_timestamp), "%Y-%m-%d %H:%M:%S.%f")
#         except:
#             new_format = datetime.datetime.strptime(str(new_datetime_timestamp), "%Y-%m-%d %H:%M:%S")
        
#         unix_time = datetime.datetime.timestamp(new_format) * 1000
#         new_format_record = {"TimeStamp":int(unix_time),
#                             "Endpoint":record["Endpoint"],
#                             "StatusCode":record["StatusCode"],
#                             "Duration":record["Duration"]
#                             }
#         list_of_conveted_timestamps.append(new_format_record)

#     list_of_conveted_timestamps.sort(key=lambda item: item.get("TimeStamp"))
    
#     return list_of_conveted_timestamps

def calculate_mode_duration(records_to_calculate):
    
    record_frequency_count = {}
    
    for record in records_to_calculate:
        
        duration_value = record["Duration"]
        
        record_frequency_count[duration_value] = record_frequency_count.get(duration_value, 0) + 1

    most_frequent = max(record_frequency_count.values())

    modes = [key for key, duration_value in record_frequency_count.items()
                      if duration_value == most_frequent]



    print("")
    print("Unique duration count: " + str(len(record_frequency_count.items())))
    print("")
    print("Highest duration (seconds): " + str(sorted(record_frequency_count.keys(), reverse=True)[0]))
    print("Highest frequency: " + str(record_frequency_count[sorted(record_frequency_count.keys(), reverse=True)[0]] ))
    print("")
    print("Lowest duration (seconds): " + str(sorted(record_frequency_count.keys())[0]))
    print("Highest frequency: " + str( record_frequency_count[sorted(record_frequency_count.keys())[0]] ))
    print("")
    print("Mode duration value (seconds): " + str(modes[0]))
    print("Mode duration frequency: " + str(record_frequency_count[modes[0]]))


    return modes

def calculate_mean_duration(records_to_calculate):
    # (6 + 8 + 12 + 14) ÷ 4 = 10
    
    record_frequency_count = len(records_to_calculate)
    record_total_value = 0

    for record in records_to_calculate:
        duration_value = record["Duration"]

        record_total_value = record_total_value + duration_value

    print("Total value: " + str(record_total_value))
    print("Total count: " + str(record_frequency_count))
    
    print("Mean value (int): " + str(int(record_total_value / record_frequency_count)))

def get_std_dev(ls):
    n = len(ls)
    mean = sum(ls) / n
    var = sum((x - mean)**2 for x in ls) / n
    std_dev = var ** 0.5
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

def return_timestamps_endpoints(records_to_calculate):

    return_list = []

    for record in records_to_calculate:

        timestamp_within_five_mins = []

        print("Timestamp: " + record["TimeStamp"] )
        print("Endpoint: " + record["Endpoint"])
        print("")


def calculate_time_groups(records_to_calculate):

    records = pd.DataFrame(records_to_calculate)

    data = records.set_index(['TimeStamp'])
    data.index = pd.to_datetime(data.index)
    
    #print(records.info())
    #print(data.info())

    #records.DatetimeIndex.groupby()
    #records.groupby('TimeStamp')
    
    
    #===========  problem code =========
    #
    # How do I display both timestamp API endpoint string, in 5min groups?  (as per Readme)
    #

    display(data.groupby(pd.Grouper(freq="5m", label='right')))
    

    
    
    


all_records = open_file("original-data/logs.txt")

#all_records = open_file("logs.json")


#===========
list_to_process = create_list_of_duration_values(all_records)

percentile_value = int(np.percentile(list_to_process, 99.9))
list_of_records_above_percentile = find_records_above_percentile(all_records, percentile_value)

list_of_unique_endpoints = set([i["Endpoint"] for i in list_of_records_above_percentile])

time_list_of_unique_endpoints = [i["TimeStamp"] for i in list_of_records_above_percentile]

#final_list_of_timestamps_endpoints = return_timestamps_endpoints(list_of_records_above_percentile)

print("======================")
calculate_mean_duration(all_records)
print("======================")
calculate_mode_duration(all_records)
print("======================")
print("99.9th percentile value: " + str(percentile_value))
print("Number of records in 99.9th percentile: " + str(len(list_of_records_above_percentile)))
print("======================")

#print(str(list_of_records_above_percentile))

calculate_time_groups(list_of_records_above_percentile)

