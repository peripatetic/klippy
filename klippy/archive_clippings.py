import datetime, time, zipfile, os


def print_info(archive_name):
    zf = zipfile.ZipFile(archive_name)
    print '=============='
    print "Printing contents of %s:" % archive_name
    print '=============='
    for info in zf.infolist():
        print
        print info.filename
        print '\tComment:\t', info.comment
        print '\tModified:\t', datetime.datetime(*info.date_time)
        print '\tSystem:\t\t', info.create_system, '(0 = Windows, 3 = Unix)'
        print '\tZIP version:\t', info.create_version
        print '\tCompressed:\t', info.compress_size, 'bytes'
        print '\tUncompressed:\t', info.file_size, 'bytes'
        print

def archive_clippings(backup_zip, textfile):
    basename = 'Kindle clippings'
    timestr = time.strftime("%Y-%m-%d-%H:%M:%S")
    
    try:
        import zlib
        compression = zipfile.ZIP_DEFLATED
    except:
        compression = zipfile.ZIP_STORED

    modes = {
        zipfile.ZIP_DEFLATED: 'deflated',
        zipfile.ZIP_STORED:   'stored',
    }

    print '=============='
    print 'Appending to the archive:'
    print '=============='
    zf = zipfile.ZipFile(backup_zip, mode='a')
    try:
        print
        print '1. Adding My Clippings.txt with compression mode', modes[compression]
        zf.write(textfile, arcname='%s - Imported to DevonThink on %s.txt' % (basename, timestr), compress_type=compression)
    finally:
        print '2. Closing'
        zf.close()

def remove_clippings(textfile):
    print '3. Removing ', textfile
    print
    os.remove(textfile)

