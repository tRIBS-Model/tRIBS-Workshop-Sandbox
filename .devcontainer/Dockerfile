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

# tRIBS is pinned by tag, and tags move. Docker keys a RUN layer on its own
# text plus its parent, so moving the tag upstream is completely invisible to
# the cache: the clone below would be restored from cache with the old source
# and the build would go green having changed nothing. This ADD fetches the
# tag's current SHA; the response body changes when the tag moves, which busts
# this layer and every layer after it. Do not remove it or rebuilds silently
# stop picking up upstream fixes.
ARG TRIBS_REF=v6.0.0
ADD https://api.github.com/repos/tRIBS-Model/tRIBS/git/refs/tags/${TRIBS_REF} /tmp/tribs-ref.json

# Clone the repository
RUN git clone -b ${TRIBS_REF} https://github.com/tRIBS-Model/tRIBS.git

WORKDIR /opt/tRIBS

# Run your specific CMake commands
# We configure it for serial execution (parallel=OFF) and optimization (-O2)
RUN cmake -S . -B build -Dparallel=OFF -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build --target all

# Add the tRIBS executable to the System PATH
ENV PATH="/opt/tRIBS/build:/opt/tRIBS/build/src:${PATH}"


# INSTALL pytRIBS
WORKDIR /opt

# Same cache-busting reason as TRIBS_REF above.
ARG PYTRIBS_REF=v1.0.0
ADD https://api.github.com/repos/tRIBS-Model/pytRIBS/git/refs/tags/${PYTRIBS_REF} /tmp/pytribs-ref.json

# Clone pytRIBS
RUN git clone -b ${PYTRIBS_REF} https://github.com/tRIBS-Model/pytRIBS.git

WORKDIR /opt/pytRIBS

# Install it using pip
# Use "--no-cache-dir" to keep the image small
RUN pip install --no-cache-dir .
# Additional packages: openpyxl for reading Excel files, explicitly install the
# Whitebox toolbox, and ipykernel.
RUN pip install --no-cache-dir openpyxl whitebox ipykernel \
    && python3 -c "import whitebox; whitebox.download_wbt(verbose=True)"

# Set the user back to the workspace directory
WORKDIR /workspaces
