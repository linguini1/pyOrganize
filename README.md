# PyOrganize
### Matteo Golin

A simple desktop organizer I developed to help get files out of my Downloads folder and into a proper filing system.

## Overview

PyOrganize contains an observer for file system events on Windows. When a file in the specified "watched directory" is
modified, created or saved, it is immediately moved to another directory based on its file name and extension.

This movement is decided by the number of tags that match the filename. Tags are associated with other directories on
the user's computer, and are stored in a configurations file. Once a matching directory is selected, the file is nested
there.

Files that contain a special user-defined character are ignored. By default, this character is `!`.

This program can be left running for the observer to run continuously, or can be run via the commandline periodically.
There is a dedicated command line interface, as well as a console interface.

## Requirements
Python 3.10.0 or greater is required.
- Watchdog
- Windows Operating System

## Features

### Active Sorting
PyOrganize can be left running to actively sort the watched directory, or it can be run periodically using the command
line argument `--initial-sort`. All files containing the ignore character (`!` by default) will be skipped.

### Adding Directories
A directory can be added by specifying its path and the tags the user wishes to be associated with it.
The subcommand is `add-directory`.

Tags can be added recursively, meaning they will be applied to directories nested below the given one.
The argument is `-recursive-tags`, or `-rt`.

The user may also select to have the tags of a previously added parent directory be attributed to the directory be 
adding, and/or its children.
The argument is `-parent-tags`, or `-pt`.

### Console Interface
The user may access the full functionality of the application through the console interface, which can be accessed on
run-time with the `console` subcommand.

### Configurations File
The configurations file can be set using the `config` subcommand. This overwrites any existing configurations file.
It can be modified with the `mod-config` subcommand.
The config contains the watched directory, ignore character and list of directory names that should be ignored when
adding directories automatically (for programmers, this may be especially useful for things like .git folders, or
dependencies that should not be listed as available directories).
