DATABASE = {
    'keyspace': {
        'name': 'hotelbook',
        'replication_factor': 2,
    },
    'config': {
        'default_keyspace': 'hotelbook',
        'hosts': ['172.18.0.2', '172.18.0.3'],
        'retry_connect': True,
        'port': 9042
    }
}
