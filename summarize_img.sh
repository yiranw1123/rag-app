#!/bin/bash

# Define the directory containing the images
IMG_DIR="./figures/"

# Loop through each image in the directory
for img in "${IMG_DIR}"*.jpg; do
    # Extract the base name of the image without extension
    base_name=$(basename "$img" .jpg)

    # Define the output file name based on the image name
    output_file="${IMG_DIR}${base_name}.txt"

    # Execute the command and save the output to the defined output file
    /Users/yiranw/llama.cpp/llava-cli -m /Users/yiranw/llama.cpp/models/llava/ggml-model-q4_k.gguf --mmproj /Users/yiranw/llama.cpp/models/llava/mmproj-model-f16.gguf --temp 0.1 -p "Describe the image in detail. Be specific about graphs, such as bar plots." --image "$img" > "$output_file"

done