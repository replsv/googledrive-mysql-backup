#!/usr/bin/env python

# Name     : googledrive-mysql-backup
# Author   : Gabriel C <shell.cooking@gmail.com>, cgFlamer @ github
# Requires : python
# Packages : gdata, atom, os, time

import atom
import os
import time
import gdata.client, gdata.docs.client, gdata.docs.data

def uploadToGoogleDrive(filename, username, password):
    print "Begining backup to Google Drive of file " + filename
    try:
        fh = open(filename)
    except IOError, e:
        sys.exit('ERROR: Unable to open ' + filename + ': ' + e[1])
    file_size = os.path.getsize(fh.name)
    file_type = 'application/zip'
    docsclient = gdata.docs.client.DocsClient(source='planzero-gupload-v0.1')
    print 'Auth on Google',
    try:
        docsclient.ClientLogin(username, password, docsclient.source);
    except (gdata.client.BadAuthentication, gdata.client.Error), e:
        sys.exit('ERROR: ' + str(e))
    except:
        sys.exit('ERROR: Unable to login')
    print '... successful!'

    # Prevent file conversion
    uri = 'https://docs.google.com/feeds/upload/create-session/default/private/full'
    uri += '?convert=false'

    # Upload the file
    t1 = time.time()
    print 'Uploading the file',
    uploader = gdata.client.ResumableUploader(docsclient, fh, file_type, file_size, chunk_size=1048576, desired_class=gdata.data.GDEntry)
    new_entry = uploader.UploadFile(uri, entry=gdata.data.GDEntry(title=atom.data.Title(text=os.path.basename(fh.name))))
    print '... successful!'
    print 'Uploaded', '{0:.2f}'.format(file_size / 1024 / 1024) + ' MB | Duration: ' + str(round(time.time() - t1, 2)) + ' seconds'