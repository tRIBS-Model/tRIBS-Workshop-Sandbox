# Base Image: Python 3.11 on Debian
FROM mcr.microsoft.com/devcontainers/python:3.11

# Install System Dependencies (CMake, Compilers)
# We update apt and install the tools tRIBS needs to build
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    && rm -rf /var/lib/apt/lists/*


    # BUILD tRIBS
WORKDIR /opt

# Clone the repository
RUN git clone https://github.com/tRIBS-Model/tRIBS.git

WORKDIR /opt/tRIBS

# Run your specific CMake commands
# We configure it for serial execution (parallel=OFF) and optimization (-O2)
RUN cmake -S . -B build -Dparallel=OFF -DCMAKE_CXX_FLAGS="-O2" \
    && cmake --build build --target all

# Add the tRIBS executable to the System PATH
ENV PATH="/opt/tRIBS/build:/opt/tRIBS/build/src:${PATH}"


# INSTALL pytRIBS
WORKDIR /opt

# Clone pytRIBS
RUN git clone https://github.com/tRIBS-Model/pytRIBS.git

WORKDIR /opt/pytRIBS

# Install it using pip
# Use "--no-cache-dir" to keep the image small
RUN pip install --no-cache-dir .
# Additional packages: openpyxl for reading Excel files and explicitly install Whitebox toolbox
RUN pip install --no-cache-dir openpyxl whitebox \
    && python3 -c "import whitebox; whitebox.download_wbt(linux=True, verbose=True)"

# Set the user back to the workspace directory
WORKDIR /workspaces