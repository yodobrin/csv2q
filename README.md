# csv2q
Python function - insert large scale messages to queue

## Context
When a quick, cheap & robust solution is required to process large scale activities in parallel, one of the enablers for this would be a message queue. within the queue, the asingle activities would be represented as messages within a queue. each handling node would dequeue a message from the queue, process it, and in most cases would log the success activity in designated queue, and the failure within specific error queue.
<br>
The solution of leveraging Azure Storage Queue fits into this, having segnificant low costs.

### Architecture
![High Level Architecture](https://github.com/yodobrin/csv2q/issues/1#issue-444822459)
#### Function

#### Storage Blob

#### Requests Queue

#### Input Q

