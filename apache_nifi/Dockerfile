FROM apache/nifi:latest

USER root

# Install docker.io inside the NiFi container
RUN apt-get update && \
    apt-get install -y docker.io && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


# Switch back to nifi user (recommended)
#USER nifi