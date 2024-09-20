# Remote Monitoring and Management

#Description
An advanced monitoring solution designed to track CPU utilization, disk usage, and device status. The application leverages Python, FastAPI, MongoDB, Docker, and Nginx to ensure reliable, real-time monitoring and enhanced system performance.

## Features

- **Real-time Monitoring**: Tracks CPU utilization, disk usage, and device status.
- **Data Storage**: Utilizes MongoDB for efficient data storage and retrieval.
- **Containerization**: Uses Docker to containerize the application, facilitating easy deployment and scalability.
- **Deployment**: Deployed on Azure Virtual Machine for reliable performance.
- **Edge Device Code**: Collects and transmits system metrics to the server.
- **Reverse Proxy**: Configured with Nginx for routing and load balancing.

## Technologies Used

- **Python**
- **FastAPI**
- **MongoDB**
- **Docker**
- **Azure**
- **Nginx**

## Installation and Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/your-username/remote-monitoring-and-management.git
    cd remote-monitoring-and-management
    ```

2. **Set up a virtual environment and install dependencies**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Run the application**:
    ```sh
    uvicorn app.main:app --reload
    ```

4. **Containerize the application with Docker**:
    ```sh
    docker build -t remote-monitoring .
    docker run -d -p 80:80 remote-monitoring
    ```

5. **Deploy on Azure Virtual Machine**:
    - Follow Azure's documentation to set up a VM and deploy the Docker container.

6. **Set up Nginx**:
    - Configure Nginx as a reverse proxy for routing and load balancing.

## Usage

- **API Endpoints**:
    - `/metrics/cpu` - Get CPU utilization.
    - `/metrics/disk` - Get disk usage.
    - `/metrics/status` - Get device status.

## Contact

- **Author**: [Shriram Narayana](https://github.com/Shr1ramN)
- **Email**: shriramnarayanabhat@gmail.com

