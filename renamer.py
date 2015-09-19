#!/usr/bin/python
import os
import sys
import argparse

DEBUG = False
args = []

class log:
    def _cerr( msg ):
        print( msg, file=sys.stderr )

    def warn( msg ):
        log._cerr( '[WARN] ' + msg )
    def info( msg ):
        if( args.verbose ):
           log. _cerr( '[INFO] ' + msg )
    def debug( msg ):
        if( DEBUG ):
            log._cerr( '[DEBG] ' + msg )
    def fatal( msg, code=-1 ):
        log._cerr( '[FATL] ' + msg )
        exit( code )

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--start_numeration', default=0,
            help='Change the start numeration number for --numerate.')
    parser.add_argument('-t', '--step', default=1,
            help='Increment number for --numerate.')
    parser.add_argument('-v', '--verbose', action='store_const', const=True,
            help='Verbose information output.')
    parser.add_argument('-n', '--numerate', action='store_const', const=True,
            help='Autonumerate files, and save extention.')
    parser.add_argument('-b', '--prefix',
            help='Prefix for file name.')
    parser.add_argument('-e', '--postfix',
            help='Postfix for file name.')
    parser.add_argument('-x', '--extention',
            help='Add extention for file name.')
    #parser.add_argument('-f', '--force', action='store_const', const=True)
    return parser

def getFileExt( fileName  ):
    ext = os.path.splitext( fileName )[1]
    if( args.extention ):
        ext = args.extention
    return ext

def makeNewName( i, oldName ):
    newFileName = oldName
    if( args.numerate ):
        newFileName = str(i)
    newFileName += getFileExt( oldName )

    if( args.prefix ):
        newFileName = args.prefix + newFileName
    if( args.postfix ):
        newFileName = newFileName + args.postfix
    return newFileName

def testFilesExists( filesList ):
    "Return False if files is not exists"
    i = int( args.start_numeration )
    isExistsFiles = False
    for fileName in filesList:
        newFileName = makeNewName( i, fileName )
        i += int( args.step )
        if os.path.exists( newFileName ):
            log.warn( "File '" + newFileName + "' is exists." )
            isExistsFiles = True
    return isExistsFiles

def renameFiles( filesList ):
    "Rename all files in current directory"
    i = int( args.start_numeration )
    for fileName in filesList:
        newFileName = makeNewName( i, fileName )
        log.info("Rename '" + fileName + "' to '" + newFileName + "'")
        os.rename( fileName, newFileName )
        i += int( args.step )

if __name__ == '__main__':
    parser = createParser()
    args = parser.parse_args( sys.argv[1:] )

    filesList = os.listdir('./');

    renameDefence = testFilesExists( filesList )
    #if( args.force ):
    #    renameDefence = False
    if( renameDefence ):
        log.fatal( "One or more files is exists." )

    renameFiles( filesList )
    exit(0)
