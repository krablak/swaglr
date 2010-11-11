'''
Created on Nov 9, 2010

@author: michalracek
'''

import csv


def load_data(filename):
    """
     Loads data for posting from csv file. 
     Attributes are in the following order:
     0: type
     1: page
     2: text
     3: link
     4: src
     5: comment
     6: title
    """
    result = []
    ifile  = open(filename, "rb")
    reader = csv.reader(ifile)
    rownum = 0
    for row in reader:
        # Save header row.
        if rownum == 0:
            header = row
        else:
            colnum = 0
            row_data = {}
            for col in row:
                if colnum==0:
                    row_data['type'] =  col
                if colnum==1:
                    row_data['page'] =  col 
                if colnum==2:
                    row_data['link'] =  col
                if colnum==3:
                    row_data['src'] =  col
                if colnum==4:
                    row_data['text'] =  col
                if colnum==5:
                    row_data['comment'] =  col
                if colnum==6:
                    row_data['title'] =  col
                colnum += 1
            result.append(row_data)           
        rownum += 1
    ifile.close()
    return result
