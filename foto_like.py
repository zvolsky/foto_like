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
from bs4 import BeautifulSoup

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
            print 'stránek :', i-1
            break
        soup = BeautifulSoup(pg)
        fotos = soup.find_all('div', 'copy')
        for foto in fotos:
            for sibling in foto.next_siblings:
            		if isinstance(sibling, Tag) and sibling.name=='a':
              			fotky.append((
                        sibling['href'],
                        int(sibling.find_all('div', 'notes')[0].text.strip()
                                    .rsplit(' ', 1)[0].replace(' ',''))
                        ))
    print 'fotek   :', len(fotky)
    for fotka in fotky.sort(key=lambda item:item[1], reverse=True):
        vfp.strtofile('%s, %s\n' % (fotka[0], fotka[1]), outfile, 1)
      
if __name__=='__main__':
    foto_like()