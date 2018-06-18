
import os

# The top argument for name in files
topdir = '.'

extens = ['xlsx', 'csv']  # the extensions to search for

found = {x: [] for x in extens} # lists of found files

# Directories to ignore
ignore = ['docs', 'doc']

logname = "findfiletypes.log"

print('Beginning search for files in %s' % os.path.realpath('/Users/Jens/Google Drive/self_learning/2018paper_spider/AI Handbook数据项目'))

# Walk the tree
for dirpath, dirnames, files in os.walk(topdir):
    # Remove directories in ignore
    # directory names must match exactly!
    for idir in ignore:
        if idir in dirnames:
            dirnames.remove(idir)

    # Loop through the file names for the current step
    for name in files:
        # Split the name by '.' & get the last element
        ext = name.lower().rsplit('.', 1)[-1]

        # Save the full name if ext matches
        if ext in extens:
            found[ext].append(os.path.join(dirpath, name))

# The header in our logfile
loghead = 'Search log from filefind for files in {}\n\n'.format(
              os.path.realpath(topdir)
          )
# The body of our log file
logbody = ''

# loop thru results
for search in found:
    # Concatenate the result from the found dict
    logbody += "<< Results with the extension '%s' >>" % search
    logbody += '\n\n%s\n\n' % '\n'.join(found[search])

# Write results to the logfile
with open(logname, 'w') as logfile:
    logfile.write('%s\n%s' % (loghead, logbody))
