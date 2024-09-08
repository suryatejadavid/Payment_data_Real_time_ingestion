# E-commerce Data Pipeline

## Overview

This project implements a scalable and efficient data pipeline for processing e-commerce order and payment data using Google Cloud Pub/Sub, Apache Cassandra, and Python. The system is designed to handle both real-time and batch data processing, while managing deduplication and storing the processed data in Cassandra. The infrastructure is containerized using Docker, simplifying deployment and management.

## Features

- **Real-time Data Ingestion:** Utilizes Google Cloud Pub/Sub for real-time ingestion and processing of order and payment data.
- **Data Deduplication:** Ensures data integrity by handling duplicate records before writing to the database.
- **Batch Processing:** Supports batch processing of e-commerce data with the ability to scale.
- **Cassandra Database:** Apache Cassandra is used as a NoSQL database for scalable, high-performance data storage.
- **Dockerized Environment:** The entire pipeline is containerized using Docker, making it easy to deploy and manage.

## Architecture

The architecture consists of the following components:

1. **Google Cloud Pub/Sub:** Streams e-commerce order and payment data in real-time.
2. **Python Scripts:** Handle the production, consumption, and deduplication of order and payment data.
3. **Apache Cassandra:** A highly scalable NoSQL database used to store order and payment data.
4. **Docker:** Containerized environment for Apache Cassandra, enabling ease of deployment.
5. **Deduplication Process:** Python scripts handle deduplication to ensure no duplicate records are stored in Cassandra.

## Project Structure
ecommerce-data-pipeline/
│
├── docker-compose-cassandra.yml                # Docker Compose file for Cassandra setup
├── ingest_in_fact_table.py                     # Python script for ingesting data into Cassandra
├── order_data_producer.py                      # Python script for producing order data
├── order_data_consumer.py                      # Python script for consuming order data
├── order_data_consumer_dedup.py                # Python script for consuming and deduplicating order data
├── payments_data_producer.py                   # Python script for producing payment data
├── setup_and_requirement_readme.txt            # Instructions for setting up the environment
└── README.md                                   # Project documentation (this file)

## Prerequisites

1. **Google Cloud SDK:** Ensure that Google Cloud SDK is installed and authenticated to use `gcloud` CLI commands.
2. **Python 3.8+:** The scripts are written in Python 3.8+.
3. **Docker:** Docker must be installed to run the Cassandra container.

## Required Python Packages,IAM, Cassandra:
```bash
pip3 install google-cloud-pubsub
pip3 install cassandra-driver

IAM Setup

	•	IAM Service Account Setup:
	•	Open the IAM & Admin service on Google Cloud.
	•	Create a new service account and assign the Pub/Sub Producer and Pub/Sub Subscriber roles.
	•	Download the JSON key for the service account and place it in your local configuration directory.

## Docker setup for Cassandra
docker compose -f docker-compose-cassandra.yml up -d
docker exec -it cassandra-container cqlsh

### Cassandra Table Creation
CREATE KEYSPACE IF NOT EXISTS ecom_store WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

CREATE TABLE ecom_store.orders_payments_facts (
    order_id BIGINT PRIMARY KEY,
    customer_id BIGINT,
    item TEXT,
    quantity BIGINT,
    price DOUBLE,
    shipping_address TEXT,
    order_status TEXT,
    creation_date TEXT,
    payment_id BIGINT,
    payment_method TEXT,
    card_last_four TEXT,
    payment_status TEXT,
    payment_datetime TEXT
);


