# Transaction Format
```Transaction_Name/16 digit read address/16 digit write address/16 characters input```    
     
ex) A00000000000000010000000000000001Hellow    
Write User table 'Hellow' to 1st index
-----------------------

# East/West Server
Receives transactions and determines, whether the first hop can be executed here or not
If it is not possible, it will send the transaction to the center server or waiting queue (Due to conflict)
If it is possible, it will execute and update values
-----------------------

# Center Server
Executing first or second hops and sending a response to the east or west server     

-----------------------
The details are described in the paper
