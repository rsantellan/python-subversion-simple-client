#! /usr/bin/python

from svnLogic import SvnLogic

aux = SvnLogic()

path = "/media/olddisk/home/rodrigo/proyectos/webUtils/web_rca"
path = "/media/olddisk/home/rodrigo/proyectos/www/web/bomitcpr/branches/1.1.2"
#path = "/media/olddisk/home/rodrigo/proyectos/www/web/bomitcpr/branches"

return_aux = aux.svnStatus(path)

#print return_aux

aux1 = aux.svnLog(path, False)

for a in aux1:
    print "=========================================="
    print "Revision: {0!r}".format(a.revision_number)
    print "Author: {0!r}".format(a.author)
    print "Time: {0!r}".format(a.time)
    print "Message: {0!s}".format(a.message)
    print "Files: {0!s}".format(a.files)
    if 'deleted' in a.files:
        print "Files deleted:"
        for auxFile in a.files['deleted']:
            print "\t {0}".format(auxFile)
    if 'added' in a.files:
        print "Files added:"
        for auxFile in a.files['added']:
            print "\t {0}".format(auxFile)
    if 'nothing' in a.files:
        print "Files nothing:"
        for auxFile in a.files['nothing']:
            print "\t {0}".format(auxFile)
    if 'modified' in a.files:
        print "Files modified:"
        for auxFile in a.files['modified']:
            print "\t {0}".format(auxFile)
    if 'prop_changed' in a.files:
        print "Files prop_changed:"
        for auxFile in a.files['prop_changed']:
            print "\t {0}".format(auxFile)
    print "Paths: {0!s}".format(a.changed_paths)
    
    
    #print a.files
    
