h1. Events 

Each event is modelled as having two main parts - the data and the meta-data. The data is the minimal viable information that this event contains for its consumers, such as the advertiser id and for example revenue value for a conversion event or a product id for a product event. The meta data contains the event id itself, the time it was produced, its source and the actor (event generator).
This is shown in the diagram below :

<add diagram>


The two parts are making the event global message, simply called event.proto 

The meta-data contains the the source and the actor messages defined in corresponding proto files. 
The actor defines the generaor of the message whereas the source the method it was delivered (such as HTTP) and the machine it took place on. 
The data events correspond to the service that generated them such as pixels / impressions / clicks . 


python - compile protos 
First you need to install protobuf with protoc and make sure that protobuf is installed. Make sure that all are version 3.x 
When writing this, the google protobuf version version 3.0.0a4 did not link some of the extra google messages. Therefoe, two of the ones that are used (Any and Timestamp) are copied manually into google_messages directory. 

When calling the protoc compiler, you will need to provide the path to the source files, and the path to the output files. For example, assuming that you are on the protobuf directory of this project, and you would like your output files to be in <dest>, the command will look like :
protoc --python_out=<dest> --proto_path=protobuf protobuf/messages/event.proto 
