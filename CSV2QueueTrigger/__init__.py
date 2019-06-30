import logging

import azure.functions as func
from azure.storage.queue import QueueService,QueueMessageFormat
from azure.storage.blob import BlockBlobService
import csv
from io import StringIO

def create_queues(queue_service,input_queue,success_queue,fail_queue):
    """Create all queues required based on the names passed.
    in case the queues already exist, nothing would be created
    Keyword arguments:
    queue_service -- a handle to create and push messages to queues
    input_queue,success_queue,fail_queue -- queues to be created
    """   
    createq(queue_service,input_queue)
    createq(queue_service,success_queue)
    createq(queue_service,fail_queue)

def createq(queue_service, queue):
    """create a queue.
    Keyword arguments:    
    queue_name -- a queue which will be created
    queue_service -- a handle to create and push messages to queues    
    """    
    queue_service.create_queue(queue)

def del_blobs(blob_service,container_name,csv_to_load):
        # blob_list=[]
        blob_service.delete_blob(container_name,csv_to_load,snapshot=None)

    

def main(msg: func.QueueMessage) -> None:
    """
    Triggered by a new message in the defined queue. based on the message, queues would be created
    and all the lines in the specified csv files would be inserted to the queue
    best performed with <500 or less lines in csv.
    The csv file is assume to have no header line
    """
    incoming_msg = msg.get_body().decode('utf-8')
    logging.info('Python queue trigger function processed a queue item: %s', incoming_msg)
    
    msg_attributes = incoming_msg.strip().split(',')
    # #assuming
    # # [0] - name of the input queue to send messages to
    # # [1] - storage account name
    # # [2] - storage account key
    # # [3] - container name for csv files
    # # [4] - csv file to use
    input_queue = msg_attributes[0]
    success_queue = '{0}-success'.format(input_queue)
    fail_queue = '{0}-fail'.format(input_queue)
    sa_name = msg_attributes[1]
    sa_key = msg_attributes[2]
    queue_service = QueueService(account_name=sa_name, account_key=sa_key) 
    queue_service.encode_function = QueueMessageFormat.text_base64encode
    create_queues(queue_service,input_queue,success_queue,fail_queue)  
    
    container_name = msg_attributes[3]
    csv_to_load = msg_attributes[4]
    blob_service = BlockBlobService(account_name=sa_name, account_key=sa_key)
    
    blobstring = blob_service.get_blob_to_text(container_name,csv_to_load).content
    f = StringIO(blobstring)
    reader = csv.reader(f, delimiter=',')
    for row in reader:
        row_line = '\t'.join(row)
        queue_service.put_message(input_queue,row_line)
    del_blobs(blob_service,container_name,csv_to_load)
