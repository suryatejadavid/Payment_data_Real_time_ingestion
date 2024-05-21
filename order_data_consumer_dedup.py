import json
from google.cloud import pubsub_v1
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

# Initialize the Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient()
publisher = pubsub_v1.PublisherClient()

# Project and Topic details
project_id = "ecommercedataingestion"
subscription_name = "orders_data-sub"
subscription_path = subscriber.subscription_path(project_id, subscription_name)
duplicate_topic_path = publisher.topic_path(project_id, "duplicate_orders")

def cassandra_connection():
    # Configuration
    CASSANDRA_NODES = ['127.0.0.1']  # Adjust if your Cassandra is hosted elsewhere or in a cluster
    CASSANDRA_PORT = 9042  # Default Cassandra port, adjust if needed
    KEYSPACE = 'ecom_store'
    
    # Connection setup (without authentication)
    cluster = Cluster(contact_points=CASSANDRA_NODES, port=CASSANDRA_PORT)
    
    # Uncomment below lines and adjust USERNAME and PASSWORD if your Cassandra setup requires authentication.
    USERNAME = 'admin'
    PASSWORD = 'admin'
    auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
    cluster = Cluster(contact_points=CASSANDRA_NODES, port=CASSANDRA_PORT, auth_provider=auth_provider)
    
    session = cluster.connect(KEYSPACE)

    return cluster,session

# Setup Cassandra connection

cluster,session = cassandra_connection()

# Prepare the Cassandra insertion statement
insert_stmt = session.prepare("""
    INSERT INTO orders_payments_facts (order_id, customer_id, item, quantity, price, shipping_address, order_status, creation_date, payment_id, payment_method, card_last_four, payment_status, payment_datetime)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""")

# Pull and process messages
def pull_messages():
    while True:
        response = subscriber.pull(request={"subscription": subscription_path, "max_messages": 10})
        ack_ids = []

        for received_message in response.received_messages:
            # Extract JSON data
            json_data = received_message.message.data.decode('utf-8')
            
            # Deserialize the JSON data
            deserialized_data = json.loads(json_data)

            print(deserialized_data)
            
            # Checking if the duplicate order ID's are present de-dup
            query = f"SELECT order_id FROM orders_payments_facts WHERE order_id = {deserialized_data.get('order_id')}"
            rows = session.execute(query)
            if rows.one():  
                # if order_id found
                # Assuming you have a orderid matching already, you can send the data to duplicate topic:
                publisher.publish(duplicate_topic_path, data=json_data.encode('utf-8'))
                print("Data thrown in duplicate topic because order_id found -> ", deserialized_data)
            else:
                # Prepare data for Cassandra insertion
                cassandra_data = (
                    deserialized_data.get("order_id"),
                    deserialized_data.get("customer_id"),
                    deserialized_data.get("item"),
                    deserialized_data.get("quantity"),
                    deserialized_data.get("price"),
                    deserialized_data.get("shipping_address"),
                    deserialized_data.get("order_status"),
                    deserialized_data.get("creation_date"),
                    None,
                    None,
                    None,
                    None,
                    None
                )
                session.execute(insert_stmt, cassandra_data)
                print("Data inserted in cassandra !!", deserialized_data)
            
            # Collect ack ID for acknowledgment
            ack_ids.append(received_message.ack_id)

        # Acknowledge the messages so they won't be sent again
        if ack_ids:
            subscriber.acknowledge(request={"subscription": subscription_path, "ack_ids": ack_ids})

# Run the consumer
if __name__ == "__main__":
    try:
        pull_messages()
    except KeyboardInterrupt:
        pass
    finally:
        # Clean up any resources
        cluster.shutdown()