## Get IN or OUT traffic from Netflow
###### Get conversation IPs information in IPGroup of Netflow Analyzer with API
###### 1. Install Libraries
```
pip install requests
pip install pandas
pip install dicttoxml
pip install pprint
```
###### 2. Enter the requests URLs into clientAIPlists.txt (one line with comment, one line with URL, ans so on)
###### 3. Proceed getTopTenSourceIPInfo
###### 5. It will generate a document named CSVFILE, and it encompasses csv file for each customer
###### 6. All customer csv file will be combined in combined.xlsx

###### _Note:_ you can also convert the .py to .exe file by the following steps:
###### - `pip install pyinstaller`
###### - Open PowerShell and excute `pyinstaller --onefile -w 'getTopTenSourceIP_V1_2.py'`
