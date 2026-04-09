# 1. Use an official Python runtime as the base image
FROM python:3.13-slim

# 2. Install System Dependencies (C++ Compiler, Go, Audio Libraries)
RUN apt-get update && apt-get install -y golang && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y cmake g++ && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y libsndfile1 ffmpeg lsof && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Copy the entire project into the container
COPY . .

# 5. Build the C++ DSP Engine
RUN cd cpp_dsp && mkdir -p build && cd build && cmake .. && make

# 6. Build the Go API Gateway
RUN cd go_gateway && go build -o main main.go

# 7. Install Python Dependencies
# (Make sure you have a requirements.txt in your python_ai folder)
RUN pip install --no-cache-dir -r python_ai/requirements.txt

# 8. Expose the ports for Go and Streamlit
EXPOSE 8080 7860

# 9. Make the startup script executable
RUN chmod +x start_docker.sh
# 8.5 Grant write permissions to the app directory for the Hugging Face user
RUN chmod -R 777 /app

# Ensure the python_ai folder specifically is writable
RUN chmod -R 777 /app/python_ai

# 10. Command to run when the container starts
CMD ["./start_docker.sh"]