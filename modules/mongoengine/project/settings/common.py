#!chuck_extends project/settings/common.py

#!chuck_appends AUTHENTICATION_BACKENDS
    # In case you want to use Mongoengine to handle auth operations
    # uncomment the following:
#   'mongoengine.django.auth.MongoEngineBackend',

#!chuck_appends SETTINGS

import mongoengine
mongoengine.connect('db_$PROJECT_NAME')

# In case you want to use Mongoengine to handle sessions
# uncomment the following:
#   SESSION_ENGINE = 'mongoengine.django.sessions'

# In case you want to use the MongoDB's GridFS feature for storage
# purposes uncomment the following 2 lines:
#   from mongoengine.django.storage import GridFSStorage
#   fs = GridFSStorage()

#!end

