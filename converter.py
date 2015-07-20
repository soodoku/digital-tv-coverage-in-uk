'''

 Parse coverage checker html files. 
 Write out data to a csv. 
 
 INPUT: html files in MY_DATA_FOLDERS
 OUTPUT: csv file called OUTPUT_FILE

'''

from os import walk
import re

MY_DATA_FOLDERS = ["cov_checker"]   # Folder to be processed
OUTPUT_FILE = "output.csv"  # csv output result

DIGITAL_SEVICES = set()
CHANNELS = set()
MYDATABASE = []


def findWithPattern(mystr, startPattern, endPattern):
    """
    Find the string that starts with <startPattern> and ends with <endPattern> in the orginal string <mystr>.
    Args:
        mystr: orginal string.
        startPattern: 
        endPattern: 
    Returns:
        The found string,
        and the remained part of the orginal string.
    """
    x = mystr.find(startPattern)
    if x==-1:
        return "",mystr
    mystr = mystr[x + len(startPattern):]
    y = mystr.find(endPattern)
    if y==-1:
        return "",mystr
    return mystr[:y], mystr[y+len(endPattern):]


# ------------FIRST PHASE----------------
# 1. Read through all the data files
# 2. Generate list of DIGITAL_SEVICES and CHANNELS
# 3. Log all the data into MYDATABASE

my_output_file = open (OUTPUT_FILE, "ab+")

def scan_all_files(log_data):
    global DIGITAL_SEVICES
    global CHANNELS
    global MYDATABASE

    DIGITAL_SEVICES = set()
    CHANNELS = set()
    MYDATABASE = []
    
    for mypath in MY_DATA_FOLDERS:
        # Process each folder
        print "Reading folder " + mypath

        # Retrieve all file in the folder
        flist = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            flist.extend(filenames)
            break

        # Process each file in the folder
        count = 0
        for filename in flist:
            count = count + 1
            if (count%1000==0):
                print ("Processing file %s000th"%(count/1000,))

            with open (mypath + "/" + filename, "r") as myfile:
                # Read the file
                data=myfile.read()

                # Extract signalQuality
                signalQuality,data = findWithPattern(data,"This address","signal");
                for signalType in ["good","variable","poor",""]:
                    if (signalQuality.find(signalType)>-1):
                        signalQuality = signalType
                        break;
                    
                # Extract transmitterName
                transmitterName,data = findWithPattern(data,"<strong>","</strong> transmitter");
                transmitterName = transmitterName

                # Extract transmitterRegion
                transmitterRegion,data = findWithPattern(data,">"," region</a>");
                if (transmitterRegion=="Detailed view"):
                    transmitterRegion=""

                # Extract list of available digitalServices
                digitalServices=set()
                digitalService,data = findWithPattern(data,"<li class=\"reception_option ","\">")
                while len(digitalService)>0:
                    digitalServices.add(digitalService)
                    digitalService,data = findWithPattern(data,"<li class=\"reception_option ","\">")
                DIGITAL_SEVICES = DIGITAL_SEVICES.union(set(digitalServices))

                # Extract list of available channels
                channels=set()
                channel,data = findWithPattern(data,"<span class=\"alt\">","</span>")
                while len(channel)>0:
                    channels.add(channel)
                    channel,data = findWithPattern(data,"<span class=\"alt\">","</span>")
                CHANNELS = CHANNELS.union(set(channels))

                # Store the record into database
                if log_data:
                    row = {'code':filename.split(".")[0],
                               'signalQuality':signalQuality,
                               'transmitterName':transmitterName,
                               'transmitterRegion':transmitterRegion,
                               'digitalServices':digitalServices,
                               'channels':channels}
                    rowStr = "%s,%s,%s,%s"%(row['code'],row['signalQuality'],row['transmitterName'],row['transmitterRegion'],)
                    for service in DIGITAL_SEVICES:
                        rowStr =rowStr + ',%d' % (int(service in row['digitalServices']),)
                    for channel in CHANNELS:
                        rowStr =rowStr + ',%d' % (int(channel in row['channels']),)
                    my_output_file.write(rowStr + "\n")

print "------------FIRST PHASE----------------"
# 1. get the DIGITAL_SEVICES and CHANNELS
scan_all_files(False)
# Set the order of DIGITAL_SEVICES and CHANNELS in the csv file
DIGITAL_SEVICES = sorted(DIGITAL_SEVICES)
CHANNELS = sorted(CHANNELS)

# Genearate the column name list
headerStr = "%s,%s,%s,%s"%('postal.code','quality.terrestrial.tv.signal','transmitter.name','transmitter.region',)
for service in DIGITAL_SEVICES:
    headerStr =headerStr + ',service.%s' % (service,)
for channel in CHANNELS:
    headerStr =headerStr + ',channel.%s' % (channel,)
my_output_file.write(headerStr + "\n")


print "------------SECOND PHASE----------------"
# 2. ouput into csv file for each row in MYDATABASE
scan_all_files(True)

my_output_file.close()

# ------------FINISH----------------
print "DONE"

            
            
