# BITS WILP Smart AI Assistant

This project is a smart assistant designed to process PDF documents, extract their content, and store the extracted data in a FAISS (Facebook AI Similarity Search) vector store. The project also includes functionality for interacting with AWS S3 for downloading and uploading files.

## Table of Contents

- [Project Structure](#project-structure)
- [Setup](#setup)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Docker](#docker)
- [AWS Lambda](#aws-lambda)
- [Contributing](#contributing)
- [License](#license)


## Setup

### Prerequisites

- Python 3.11
- Docker
- AWS CLI configured with appropriate credentials

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/bits_chatbot_cc.git
    cd bits_chatbot_cc
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Set up environment variables:

    Create a `.env` file in the root directory and add the following variables:

    ```env
    GOOGLE_API_KEY=your_gemini_api_key 
    AWS_ACCESS_KEY_ID=your_aws_access_key_id
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
    ```

## Usage

### Local Execution

1. Process the PDFs and update the FAISS vector store (Downloads PDFs from S3 and also updates the vector files over S3):

    ```sh
    python src/pdf_loader.py
    ```

2. To have the chatbot running in your machine, use:

    ```sh
    streamlit run src/bits_chatbot.py
    ```

### Docker

1. Build the Docker image:

    ```sh
    docker build -t bits_chatbot_cc .
    ```

2. Run the Docker container:

    ```sh
    docker-compose up
    ```

## Docker

The project includes a `Dockerfile` and `docker-compose.yml` for containerized deployment.

### Dockerfile

The `Dockerfile` sets up the environment with necessary dependencies and installs the required Python packages.

### docker-compose.yml

The `docker-compose.yml` file defines the services and their configurations.

## AWS Lambda

The project includes an AWS Lambda function in `improvements/LambdaFunction.py` to automate the process of downloading files from S3, processing PDFs, and uploading the updated vector store back to S3.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
