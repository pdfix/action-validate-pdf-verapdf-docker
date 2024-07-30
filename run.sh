#!/bin/bash

# init
pushd "$(dirname $0)" > /dev/null

IMAGE_NAME="pdfix-verapdf-validation"
IMAGE_TAG="latest"
IMAGE="$IMAGE_NAME:$IMAGE_TAG"

# Initialize variables for arguments
FORCE_REBUILD=false
INPUT_PDF=""
OUTPUT_PDF=""
PROFILE=""
MAX_FAILS=""
FORMAT=""

# Function to print help message
print_help() {
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  --input <input.pdf>     Path to the input PDF file"
    echo "  --output <output>       Path the output file"
    echo "  --profile <profile>     Validation profile"
    echo "  --maxfailuresdisplayed <max> Max failures displayed"
    echo "  --format <format>       Output format (xml, json, html, text, raw)"
    echo "  --build                 Force rebuild of the Docker image"
    echo "  --help                  Display this help message"
}

# Parse script arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --build) FORCE_REBUILD=true ;;
        --profile) PROFILE="$2"; shift ;;
        --input) INPUT_PDF="$2"; shift ;;
        --output) OUTPUT_PDF="$2"; shift ;;
        --maxfailuresdisplayed) MAX_FAILS="$2"; shift ;;
        --format) FORMAT="$2"; shift ;;
        --help) print_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; print_help; exit 1 ;;
    esac
    shift
done

# Check required arguments
if [ -z "$INPUT_PDF" ]; then
    echo "Error: --input argument is required."
    print_help
    exit 1
fi

# Extract directory paths and file names
INPUT_DIR=$(dirname "$INPUT_PDF")
INPUT_FILE=$(basename "$INPUT_PDF")
OUTPUT_DIR=$(dirname "$OUTPUT_PDF")
OUTPUT_FILE=$(basename "$OUTPUT_PDF")
PROFILE_DIR=$(dirname "$PROFILE")
PROFILE_FILE=$(basename "$PROFILE")

# Check if Docker is installed
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed on this system."
    exit 1
else
    echo "Docker is installed."
fi

# Function to build Dockerfile
build_dockerfile() {
    echo "Building Dockerfile..."
    if docker build -t $IMAGE .
    then
        echo "Dockerfile built successfully and image $IMAGE created."
    else
        echo "Error: Failed to build Dockerfile."
        exit 1
    fi
}

# Check if the Docker image is already present
if docker image inspect $IMAGE > /dev/null 2>&1
then
    if [ "$FORCE_REBUILD" = true ]; then
        echo "Force rebuild flag is set. Rebuilding Docker image $IMAGE..."
        build_dockerfile
    else
        echo "Docker image $IMAGE already exists."
    fi
else
    echo "Docker image $IMAGE does not exist. Building Dockerfile..."
    build_dockerfile
fi

DATA_IN="/data_in"
DATA_OUT="/data_out"
DATA_PROFILE="/data_profile"

# Run the Docker container with the specified arguments
docker_cmd="docker run --rm -v \"$INPUT_DIR\":\"$DATA_IN\""

if [ -n "$OUTPUT_DIR" ]; then
    docker_cmd+=" -v \"$OUTPUT_DIR\":\"$DATA_OUT\""
fi

if [ -n "$PROFILE_DIR" ]; then
    docker_cmd+=" -v \"$PROFILE_DIR\":\"$DATA_PROFILE\""
fi

docker_cmd+=" -it $IMAGE -i \"$DATA_IN/$INPUT_FILE\" "


if [ -n "$OUTPUT_FILE" ]; then
    docker_cmd+=" -o \"$DATA_OUT/$OUTPUT_FILE\""
fi
if [ -n "$PROFILE" ]; then
    docker_cmd+=" --profile \"$DATA_PROFILE/$PROFILE_FILE\""
fi
if [ -n "$MAX_FAILS" ]; then
    docker_cmd+=" --maxfailuresdisplayed \"$MAX_FAILS\""
fi
if [ -n "$FORMAT" ]; then
    docker_cmd+=" --format \"$FORMAT\""
fi

eval $docker_cmd

popd > /dev/null
