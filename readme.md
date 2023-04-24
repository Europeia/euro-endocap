Usage Instructions:

1. (First time only): Install required dependencies using `pip install -r requirements.txt`.
2. Create a file called start.bat in the same folder as this script's main.py file.
3. Configure the following command with your credentials and put it in start.bat:
   - `python3 main.py -h DB_HOST -u DB_USER -p DB_PWD -x EXCLUDED_NATION -x ANOTHER_EXCLUDED_NATION -x ETC`
   - you can add an optional -e ENDOCAP parameter to the above, the default is 25.
4. Save and run that file. Once the script terminates, you should see a file called 'output.txt' in the same directory as main.py.
   - This file contains a list of nations and the nations that they are endorsing that are over the cap.
