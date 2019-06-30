# csv2q
Python function - insert large scale messages to queue

## Context
When a quick, cheap & robust solution is required to process large scale activities in parallel, one of the enablers for this would be a message queue. within the queue, the asingle activities would be represented as messages within a queue. each handling node would dequeue a message from the queue, process it, and in most cases would log the success activity in designated queue, and the failure within specific error queue.
<br>
The solution of leveraging Azure Storage Queue fits into this, having segnificant low costs.

### Architecture
![High Level Architecture](https://user-images.githubusercontent.com/37622785/57838832-22a94e00-77ce-11e9-8098-ef06d3042967.png)
#### Function
The function is triggered by messages inserted to the request queue.
it assume the message is constructed of the required information to process single csv file and insert each line as message to provided queue. the function would create the queue in case it does not exist.
#### Storage Blob
the storage blob, is the location in which the function would load the csv file from. the details of the storage are part of the message.
#### Requests Queue
the request queue is where all requests for process should arrive to. it is expected a message has the following attributes in the following order, with comma (,)
 [0] - name of the input queue to send messages to
 [1] - storage account name
 [2] - storage account key
 [3] - container name for csv files
 [4] - csv file to use

#### Input Q
all the lines form the loaded csv would be inserted as seperated messages to the queue

## provided handler
The provided handler is simple way to utilize the function

## Build & Deploy
Update settings (queue names etc) and then run this from a command line

* func azure functionapp publish <function app name> --build-native-deps

