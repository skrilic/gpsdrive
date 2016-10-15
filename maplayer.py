# -*- coding: utf-8 -*-

__author__="slaven"
__date__ ="$28.05.2010. 10:51:58$"

import sys
import os
import ConfigParser
from string import Template

#User's Home folder ...
homedir = os.getenv("HOME")
tmplvar=""
tmplplacemark= "%s/gpspectrum/templates/kmlbody.xml" % homedir
config = ConfigParser.ConfigParser()
config.read("%s/gpspectrum/conf/kml.ini" % homedir)
ptcsv = config.get("webroot","csv")
ptimg = config.get("webroot","image")

def file2string(filein):
    """
    Function gets name of input file with complete path and returns string populated with
    content of the file.
    """
    stringout = ""
    stringin = open(filein,"r")
    for line in stringin:
        stringout = stringout + line
    return stringout

#for line in tmplplacemark:
#    tmplvar = tmplvar + line
#kmlplacemark=Template(tmplvar)

def kmlgenerator(measlogfile,kmlout):
    tmpldir = "%s/gpspectrum/templates" % homedir
    # First remove remaining KML file ...
    if os.path.isfile(kmlout) == True:
        os.remove(kmlout)
    kmlfile = open(kmlout,'a')
    logobject = open(measlogfile,"r")
    header = open("%s/kmlheader.xml" % tmpldir,"r")
    footer = open("%s/kmlfooter.xml" % tmpldir,"r")
    # Write header of KML file
    for line in header:
        kmlfile.write(line)
    # Now, it is time to add tessallation.
    #tsltbody=open("%s/kmltessellatebody.xml" % tmpldir,"r")
    tsltbody="%s/kmltessellatebody.xml" % tmpldir
    # Create coords_values
    cooval = ""
    for logrow in logobject:
      elm = logrow.split(',')
      # Skip line with table header (column name)
      if elm[0] != 'datetime':
          cooval = cooval + "%s,%s,%s\r\n" % (elm[2],elm[1],elm[3])
    kmlfile.write(Template(file2string(tsltbody)).substitute(style="redLineOrangePoly",coords_values=cooval)) # Style could be: yellowLineGreenPoly or redLineOrangePoly, for now.
    #
    #measlogfile must be opened again for Points definitions.
    logobject.close()
    logobject = open(measlogfile,"r")
    i = 1
    for logrow in logobject:
        elm = logrow.split(',')
        latit = elm[1]
        long = elm[2]
        coordinates = "%s,%s" %(long,latit)
        if elm[0] != 'datetime':
            description = elm[0] #Date and Time
            csvfile = elm[3]
            pngfile = elm[4]
            placemark = Template(file2string(tmplplacemark)).substitute(pathtocsv=ptcsv,pathtoimage=ptimg,name=i,coords=coordinates,desc=description,csv=csvfile,spectrum=pngfile)
            kmlfile.write(placemark)
            i=i+1
    #At last, write footer of KML file and then, close it.    
    for line in footer:
        kmlfile.write(line)
    kmlfile.close()
    logobject.close()
    return

def main():
    measlog = sys.argv[1]
    kmloutput = sys.argv[2]
    kmlgenerator(measlog,kmloutput)

if __name__ == "__main__":
    main()