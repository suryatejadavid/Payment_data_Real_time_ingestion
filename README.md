# E-commerce Data Pipeline

## Overview

This project implements a data pipeline for processing e-commerce order and payment data using Google Cloud Pub/Sub, Apache Cassandra, and Python. The system is designed to process both real-time and batch data, handle deduplication, and store the processed data in Cassandra. The infrastructure is containerized using Docker, which makes it easy to deploy and manage.

## Features

- **Real-time Data Ingestion:** Utilizes Google Cloud Pub/Sub to ingest and process order and payment data in real-time.
- **Data Deduplication:** Ensures data integrity by handling duplicate records before writing to the database.
- **Batch Processing:** Supports batch data processing with the ability to scale easily.
- **Cassandra Database:** Apache Cassandra is used for scalable, high-performance data storage.
- **Dockerized Environment:** Easy deployment of the entire pipeline using Docker.

## Architecture

The architecture consists of the following components:

1. **Google Cloud Pub/Sub:** Manages the streaming of order and payment data in real-time.
2. **Python Scripts:** Several Python scripts handle the production, consumption, and deduplication of order and payment data.
3. **Apache Cassandra:** A NoSQL database used to store order and payment data.
4. **Docker:** A containerized setup for Apache Cassandra.
5. **Deduplication Process:** Python scripts handle deduplication to ensure that no duplicate records are stored in Cassandra.

## Project Structure
ecommerce-data-pipeline/
│
├── docker-compose-cassandra.yml               # Docker Compose file for Cassandra setup
├── ingest_in_fact_table.py                    # Python script for ingesting data into Cassandra
├── order_data_producer.py                     # Python script for producing order data
├── order_data_consumer.py                     # Python script for consuming order data
├── order_data_consumer_dedup.py               # Python script for consuming and deduplicating order data
├── payments_data_producer.py                  # Python script for producing payment data
└── README.md                                  # Project documentation (this file)

## Prerequisites

1. **Google Cloud SDK:** Ensure Google Cloud SDK is installed and authenticated to use `gcloud` CLI commands.
2. **Python 3.8+:** The scripts require Python 3.8+.
3. **Docker:** Make sure Docker is installed for running the Cassandra container.

## Setup and Deployment

### 1. Google Cloud Setup

- **Create Pub/Sub Topics:**
    - Create the following Pub/Sub topics:
        - `orders_data`
        - `payments_data`
        - `dlq_payments_data`
    
- **Authentication:**
    - Authenticate your GCP account using:
      ```bash
      gcloud auth application-default login
      ```
    - Ensure that the service account has Pub/Sub producer and subscriber roles.

### 2. Docker Setup for Cassandra

- Start the Cassandra container using Docker:
  ```bash
  docker compose -f docker-compose-cassandra.yml up -d
