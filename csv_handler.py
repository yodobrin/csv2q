import csv
import os
from azure.storage.queue import QueueService,QueueMessageFormat
from azure.storage.blob import BlockBlobService

file2read = 'your_csv_file.csv'
dest_folder = 'split'
split_file_prefix = 'split_'
records_per_file = 300
csvfile = open(file2read, 'r').readlines()
filename = 1
sa_name = '<>'
sa_key = '<storage account key>'
queue_2_use = '<your pre created request q>'
main_q = '<queue to insert into>'
container_2_use = '<container in which to upload split csv to>'


queue_service = QueueService(account_name=sa_name, account_key=sa_key) 
queue_service.encode_function = QueueMessageFormat.text_base64encode

blob_service = BlockBlobService(account_name=sa_name, account_key=sa_key)

for i in range(len(csvfile)):
    target_filename = f'{split_file_prefix}_{filename}.csv'
    target_filepath = os.path.join(dest_folder, target_filename)
    if i % records_per_file == 0:
        open(target_filepath, 'w+').writelines(csvfile[i:i+records_per_file])
        messages.append(f'{main_q},{sa_name},{sa_key},{container_2_use},{target_filename}')
        blob_service.create_blob_from_path(container_2_use,target_filename,target_filepath)
        filename += 1

for msg in messages:
    queue_service.put_message(queue_2_use,msg)
   
