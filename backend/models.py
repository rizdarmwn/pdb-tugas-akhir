from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Item(Model):
    id = columns.UUID(primary_key=True)
    name = columns.Text()
    desc = columns.Text()
