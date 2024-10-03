## RAG Generic solution

This is a generic full-stack solution for running RAG (Retrieval Augmented Generation) systems.

## Features

- Generic solution for running RAG systems
- Supports both file uploads and YouTube links
- Supports both CSV and PDF files
- Supports both GPT-4 and Qwen-7B models
- Supports both single-document and multi-document retrieval
- Supports both single-query and multi-query retrieval
- Supports both single-answer and multi-answer retrieval

## Architecture

The architecture of the solution is as follows:

![Architecture](https://github.com/sayjeyhi/Generic-RAG/blob/main/architecture.png)

## Usage

To use the solution, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/sayjeyhi/Generic-RAG.git
```

2. Install the required dependencies:

```bash
cd Generic-RAG/backend
pip install -r requirements.txt
```

3. Run the backend server:

```bash
uvicorn main:app --reload
```

4. Run the frontend:

```bash
cd ../frontend
npm install
npm run dev
```

5. Open your browser and navigate to http://localhost:3000

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
