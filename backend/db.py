from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.management import create_keyspace_simple

import models
import settings


def build():
    # Setup a the driver connection used by the mapper
    connection.setup(**settings.DATABASE['config'])

    # Creates a keyspace with SimpleStrategy for replica placement
    # If the keyspace already exists, it will not be modified
    create_keyspace_simple(**settings.DATABASE['keyspace'])

    # Inspects the model and creates / updates the corresponding table and columns.
    # If keyspaces is specified, the table will be synched for all specified keyspaces.
    sync_table(models.Room)
    sync_table(models.Book)
    sync_table(models.BookCancelPredictionHistory)
    sync_table(models.User)


build()
