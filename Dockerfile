# Base Airflow image with Python and required Airflow environment
FROM apache/airflow:2.3.0

# Switch to root to install system-level dependencies (like Java)
USER root

# Update package list and install OpenJDK 11 for running PySpark
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk && \
    rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME so PySpark knows where to find Java
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Switch back to the airflow user (good security practice)
USER airflow

# Copy your Python dependencies list to the container
COPY requirements.txt .

# Install all Python dependencies (e.g. Faker, PySpark, Kafka libs, Snowflake connector)
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
