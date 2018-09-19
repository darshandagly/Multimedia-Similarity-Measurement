# Multimedia-Similarity-Measurement
-----------------------------------

Description
-----------
Given a dataset of locations, images, and users along with the textual and visual descriptors of each of the objects(location, image, user), the implemented programs aim to find the 'k' most similar locations, images and users based on the user input.

Programs 1, 2, and 3 compute the output from the data extracted from MongoDB database. 
Programs 4 and 5 directly parse the dataset files and generate the required output.


Getting Started
---------------
The below instructions will help you set the project up and running on your local Windows machine for development and testing purposes.

Prerequisites
-------------
Before running and testing the programs included in this project, follow the below steps to set up the environment.

**Installing MonogDB for Windows 10**
You can install using the Windows Installer wizard or from the command line. 
Below are the steps to install MongoDB Community Edition using the Windows Installer Wizard.
1. Open any Web Browser and visit https://www.mongodb.com/download-center#community page.
2. Download the latest stable version(v4.0.2 at the time of development) .msi installer file.
3. Run the .msi file once downloaded and follow the steps in the wizard to install MongoDB and MongoDB Compass.
4. For detailed installation instruction visit https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/ page.


**Installing Python v3.7 for Windows**
1. Open a web browser and visit https://www.python.org/downloads/
2. Download the latest stable version(v3.7.0 at the time of development) .exe file.
3. Run the .exe file once downloaded and follow the steps in the wizard to install.

**Python Libraries required to run the Programs**
1. pymongo
2. scipy
3. numpy
4. heapq
5. BeautifulSoup

Enter the below command in command prompt to install the libraries:
pip install <library_name>

Ex: pip install pymongo

Note: Open command prompt as administrator if you have troubles installing the libraries.

**Development/Test Datasets**
1. Open any Web Browser and visit http://skuld.cs.umass.edu/traces/mmsys/2015/paper-5/
2. Click on devset/testset link under Resources tab and download the following files required for testing and development purposes.
  a. desctxt.zip
  b. descvis.zip
  c. img.zip
  d. imgwiki.zip
  e. devset_topics.xml
3. Create a new directory named 'dataset' where you have saved the project programs and unzip the above files.

Note: Please go through the dataset readme file(Div150Cred readme file describing the data format) for understanding the structure of the data if you are using this project for development purposes.


Running the Tests
-----------------
Now that we have done the environment setup, refer to the below detailed program description along with the expected input and steps to execute the programs. 

1. user_similarity.py
This program is used to find the most similar 'k' users based on the input user_id, model and value of k. This program uses the textual features of the users to compare the users to each other and provide a list of k similar users as output. This program also lists the overall matching score along with the top 3 terms that have the highest similarity contribution.

Expected Input Format: <image_id> <model - TF/DF/TF-IDF> <k>
Example : 39052554@N00 TF 5


2. image_similarity.py
This program is used to find the most similar 'k' images based on the input image_id, model and value of k. This program uses the textual features of the images to compare the images to each other and provide a list of k similar images as output. This program also lists the overall matching score along with the top 3 terms that have the highest similarity contribution.

Expected Input Format: <image_id> <model - TF/DF/TF-IDF> <k>
Example : 288051306 TF-IDF 5


3. location_similarity.py
This program is used to find the most similar 'k' locations based on the input location_id, model and value of k. This program uses the textual features of the locations to compare the locations to each other and provide a list of k similar locations as output. This program also lists the overall matching score along with the top 3 terms that have the highest similarity contribution.

Expected Input Format: <location_id> <model - TF/DF/TF-IDF> <k>
Example : 6 DF 7


4.model_based_location_sim.py
This program is used to find the most similar 'k' locations based on input location_id, model and value of k. This program uses the visual descriptors of the images associated with locations for similarity comparisons. This program also list the overall matching score if the 'k' locations along with top 3 contributing pairs

Expected Input Format: <location_id> <model - CM, CM3x3, CN, CN3x3,CSD,GLRLM, GLRLM3x3,HOG,LBP, LBP3x3> <k>
Example : 10 CN3x3 7

5. location_visual_similarity.py
This program is used to find the most similar 'k' locations based on input location_id and value of k. This program uses all the visual descriptors of the images associated with locations for similarity comparisons. This program also list the overall matching score if the 'k' locations along with all the models and their contributing values.

Expected Input Format: <location_id> <k>
Example : 4 5

**Steps to Run the Programs**
1. Open Command Prompt
2. Enter Command python <dir>/<program_name>.py 

Example : python C:/Users/admin/Desktop/MWDB-Phase1/image_similarity.py


Release History
---------------
0.0.1 : Intial Development


Author
------
Darshan Dagly
