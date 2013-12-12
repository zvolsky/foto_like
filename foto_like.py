#!/usr/bin/env python
# coding: utf8
#-------------------------------------------------------------------------------
# Name:        foto_like
# Purpose:     retrieves URL's and count of "like" for photos at jozefsobin.cz
#
# Author:      Mirek Zvolsky
#
# Created:     12.12.2013
# Licence:     public domain
#-------------------------------------------------------------------------------

"""retrieves URL's and count of "like" for photos at jozefsobin.cz
"""

import vfp
import urllib2
from bs4 import BeautifulSoup, Tag

base = 'http://blog.jozefsebin.cz/page/'
outfile = 'fotky.csv'

def foto_like():
    """retrieves URL's and count of "like" for photos at jozefsobin.cz
    """
    fotky = []
    for i in xrange(1,100000):
        try:
            pg = urllib2.urlopen(base + '%s'%i).read()
            print i
        except:
            break
        soup = BeautifulSoup(pg)
        fotos = soup.find_all('div', 'copy')
        if not len(fotos):
            break
        for foto in fotos:
            for sibling in foto.next_siblings:
                if isinstance(sibling, Tag) and sibling.name=='a':
                    notes = sibling.find_all('div', 'notes')[0].text
                    try:
                        pocet = int(notes
                                .strip().rsplit(' ', 1)[0].replace(' ','')) 
                    except ValueError:
                        # print '???', notes
                        pocet = 0
                    fotky.append((sibling['href'], pocet))
    print 'stránek :', i-1
    print 'fotek   :', len(fotky)
    fotky.sort(key=lambda item:item[1], reverse=True)
    for fotka in fotky:
        vfp.strtofile('%s, %s\n' % (fotka[0], fotka[1]), outfile, 1)
      
if __name__=='__main__':
    foto_like()

'''
            		if isinstance(sibling, Tag) and sibling.name=='a':
                    notes = sibling.find_all('div', 'notes')[0].text
                    try:
                        pocet = int(notes
                                .strip().rsplit(' ', 1)[0].replace(' ','')) 
                    except ValueError:
                        print '???', notes
                        pocet = 0
              			fotky.append((sibling['href'], pocet))
'''