# Bloom Filter

# Bloom Filter - Part - 1  

### Article link  
substack.com - https://sunilkathuria.substack.com/p/bloom-filter-part-1  
Medium.com - https://medium.com/incomputingworld/bloom-filter-part-1-21d6257c8c8d  

### For Article/Bloom Filter - Part 1/simple_bloom_filter.py  
This file explains the basic implementation of a bloom filter. It covers insertion and search operations and demonstrates an example of a "False-Positive."  


# Bloom Filter - Part - 2   

### Article link  
substack.com - https://sunilkathuria.substack.com/p/bloom-filter-part-2    
Medium.com - https://medium.com/incomputingworld/bloom-filter-part-2-1921e4958a12    

### For Article/Bloom Filter - Part 2/bloom_filter.py  
This file contains the implementation of the class BloomFilter.  

### For Article/Bloom Filter - Part 2/hashes.py  
This file imports all the hash functions that the class BloomFilter uses.  

### For Article/Bloom Filter - Part 2/input_data.py  
This file contains two lists. The data from these lists is added and searched for while implementing a Bloom filter.    

### For Article/Bloom Filter - Part 2/measurements.py  
This file contains the implementation of mathematical functions that help decide the size of a bloom filter array, suggests the count hash functions to use, and a function that calculates the "False-positive" rate of a bloom filter based on the number of entries added.  

### For Article/Bloom Filter - Part 2/test_bloom_filter.py  
This file contains the sample implementation of the class BloomFilter.   


# Bloom Filter - Part - 3  

### Article link  
Substack - https://sunilkathuria.substack.com/p/bloom-filter-part-3  
Medium - https://medium.com/incomputingworld/bloom-filter-part-3-77a44aa4dea5   

### For Article/Bloom Filter - Part 3  
This is the main folder for this article.  

### For Article/Bloom Filter - Part 3/Database/schema.sql   
This file contains the schema definition we must create before running the application.  

### For Article/Bloom Filter - Part 3/Database/test_data.sql  
This file contains many insert statements that act as base data for this application.  

### For Article/Bloom Filter - Part 3/main_server  
This folder contains the files to run the main_server application.   

### For Article/Bloom Filter - Part 3/main_server/config.py  
This file contains the configuration details required for the main server application.   

### For Article/Bloom Filter - Part 3/main_server/main_server.py  
This file implements the main_server application. Written in flask. It primarily contains the initialization and route setting code.  

### For Article/Bloom Filter - Part 3/main_server/operations.py   
This file contains all the business logic, written in various functions, to run the server.   

### For Article/Bloom Filter - Part 3/node_server  
This folder contains the files to run the application's node server. I have tested the code by running three separate instances of this application.  

### For Article/Bloom Filter - Part 3/node_server/config.py  
This file contains the configuration details required for the node server application. Change the NODE_NAME and NODE_URL before you start another application instance. All the instances should have a different port number.  

### For Article/Bloom Filter - Part 3/node_server/node_server.py    
This file implements the node_server application. Written in flask. It primarily contains the initialization and route setting code.   

### For Article/Bloom Filter - Part 3/node_server/operations.py   
This file contains all the business logic, written in various functions, to run the node server.   

### For Article/requirements.txt  
Create a virtual environment on your machine and use this requirements file to set the environment.  


# Bloom Filter - Part - 4   

### Article link  
Substack - https://sunilkathuria.substack.com/p/bloom-filter-part-4  
Medium - https://medium.com/incomputingworld/bloom-filter-part-4-482d826db4f0  

### For Article/Bloom Filter - Part 4  
This is the main folder for this article.   

### For Article/Bloom Filter - Part 4/hashes.py  
This file imports all the hash functions that the class BloomFilter uses.  

### For Article/Bloom Filter - Part 4/input_data.py  
This file contains four lists. The data from these lists is added and searched for while implementing a Bloom filter.  

### For Article/Bloom Filter - Part 4/measurements.py  
This file contains the implementation of mathematical functions that help decide the size of a bloom filter array, suggests the count hash functions to use, and a function that calculates the "False-positive" rate of a bloom filter based on the number of entries added.  

### For Article/Bloom Filter - Part 4/scalable_bloom_filter.py  
This file contains the implementation of two classes. First is the BlooFilter. This class implements a bloom filter similar to the one we used in the previous articles. However, there is one additional parameter, "load_threshold." This is used to check the load (whether the number of bits set to 1 exceeds this threshold or not).  
The second class is ScalableBloomFilter. This class uses BloomFilter to implement a scalable bloom filter in a list. It provides the functionality to request a new bloom filter when the load threshold of the current bloom filter exceeds the limit. It also modifies the search functionality, checking all the bloom filters.  

### For Article/Bloom Filter - Part 4/test_scalable_bloom_filter.py  
This file contains the sample implementation of the class BloomFilter.  

### For Article/requirements.txt  
Create a virtual environment on your machine and use this requirements file to set the environment.  
