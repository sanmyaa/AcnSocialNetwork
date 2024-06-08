# Project Installation Guide

## Step 1: Clone this Repository

First, clone this repository to your local machine using the following command:

```bash
git clone https://github.com/sanmyaa/AcnSocialNetwork.git
```

## Step 2: Run Docker Engine

Make sure Docker Engine is running on your local system. You can download and install Docker from [here](https://www.docker.com/products/docker-desktop).

## Step 3: Build and Run the Docker Containers

Navigate into the project folder and build the Docker containers with the following commands:

```bash
docker-compose build --no-cache
docker-compose up
```

## Accessing the Application

Once the server is live on your local machine, you can access the APIs and the admin panel:

- **APIs**: [http://localhost:8000/api](http://localhost:8000/api)
- **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)

## Step 4: Quit the Server

After quitting the server, bring down the Docker containers and networks with:

```bash
docker-compose down
```

## Note

**The database (Postgres) is running on a t3 micro instance, which will cause significant slowdown. This is done for cost optimization.**

## API COllection

A collection containing all the APIs can be accessed here [https://elements.getpostman.com/redirect?entityId=36159222-411e1419-f39b-4381-9fdc-b04ed2c469fe&entityType=collection](Postman Collection)

(For ease of understanding, the sample bearer tokens were kept exposed in all requests)