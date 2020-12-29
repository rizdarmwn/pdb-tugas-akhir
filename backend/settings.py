DATABASE = {
    'keyspace': {
        'name': 'hotelbook',
        'replication_factor': 1,
    },
    'config': {
        'default_keyspace': 'hotelbook',
        'hosts': ['172.18.0.2', ],
        'retry_connect': True,
        'port': 9042
    }
}
