# First initialization

from loader import connect
from loader import updateConfig
from loader import popTags
from loader import loadFile

# # Connect with a dynamic IP using the min. config file
connect()

# # Update the config file with online info
updateConfig()

# # Populate the tags file with online info
popTags()

# # Load the production boot.py and main.py files
print('Downloading production files...')
loadFile('boot.py')
loadFile('main.py')
