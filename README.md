Distributed Password Cracker

# Running the code
1. Set up the environment: ```conda create -f environment.yaml```
2. Activate the conda environment ```conda activate dpc```
3. Run ```python hash_gen.py``` to generate a hash for your password
	3.1 Enter a password
	3.2 Enter the hashtype ('sha' or 'md5')
	3.3 THe generated has will be printed
4. Run the server file: ```python server.py localhost 11111```
5. Copy the password generated from the ```hash_gen.py``` file and use it as input to the ```server.py``` file
6. Open a new terminal or a new tab on the terminal and run the client(s), keeping the <ip address> and <port number> same as that used for the server: ```python3 client.py localhost 11111```
