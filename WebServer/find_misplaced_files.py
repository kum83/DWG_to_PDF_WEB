import subprocess
import json
import time
import datetime

find_files_cmd = 'find_misplaced_files.cmd '

sPath = ' L:\\Drawings '
sTypes = ' ".dwg .wdp " '

search_folders = {'L:\\Checker': ' ".dwg " ',
                  'L:\\Drawings': ' ".dwg .wdp .wdt .wdl .wda " ',
                  'L:\\Layouts': ' ".dwg .slddrw .sldasm .sldprt " ',
                  'L:\\MBDrawings': ' ".pdf " ',
                  'L:\\PDFDrawings': ' ".pdf .tif " ',
                  'L:\\SW Commercial': ' ".sldprt .sldasm "',
                  'L:\\SW Drawings': ' ".slddrw "',
                  'L:\\SW Models & Parts': ' ".sldprt .sldasm "',
                  'L:\\SW Reference files': ' ".sldprt .sldasm .slddrw .swb .pdf .xls "'}
misplaced_files = {}

for sPath in search_folders.keys():
    # print '\t' + find_files_cmd + '"' + sPath + '"' + search_folders[sPath]
    try:
        sOutput = subprocess.check_output(
            find_files_cmd + '"' + sPath + '"' + search_folders[sPath])
        sOutput = sOutput[sOutput.rfind('"') + 1:].strip()

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        misplaced_files[sPath[sPath.rfind('\\') + 1:]] = {'allowed': search_folders[sPath].translate(None, '"'),
                                                          'misplaced_files': sOutput.split('\r\n'),
                                                          'updated': st}
    except:
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

        misplaced_files[sPath[sPath.rfind('\\') + 1:]] = {'allowed': search_folders[sPath].translate(None, '"'),
                                                          'misplaced_files': ['no misplaced files'],
                                                          'updated': st}


# print json.dumps(misplaced_files, sort_keys=True, indent=2,
# separators=(',', ': '))

fJSON = open('misplaced_files.json', 'w')
fJSON.write(json.dumps(misplaced_files, sort_keys=True,
                       indent=2, separators=(',', ': ')))
fJSON.close()
