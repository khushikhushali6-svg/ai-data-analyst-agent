## 🤖 AI-Powered Insights

The application uses a local Qwen3 model through Ollama to analyze the generated dataset summary and provide:

- Key Insights
- Business Interpretation
- Recommendations

## 📄 Automated Reports

Users can generate an automated text-based analysis report containing:

- Dataset overview
- Column information
- Statistical summary
- Product sales analysis

The generated report can be downloaded directly from the application.

## ⚙️ Installation

### 1. Clone the Repository

git clone https://github.com/khushikhushali6-svg/ai-data-analyst-agent.git

### 2. Open the Project

cd ai-data-analyst-agent

### 3. Create a Virtual Environment

python -m venv venv

### 4. Activate the Virtual Environment

Windows:

venv\Scripts\activate

### 5. Install Dependencies

pip install -r requirements.txt

## 🔐 Environment Variables

Create a `.env` file in the project root:

OPENAI_API_KEY=your_api_key_here

**Never upload your `.env` file or API keys to GitHub.**

The `.env` file is already included in `.gitignore`.

## 🤖 Ollama Setup

Install Ollama and download the Qwen3 model:

ollama pull qwen3:1.7b

Start Ollama if required:

ollama serve

The application uses the local Ollama API for AI-generated data insights.

## ▶️ Run the Application

Start the Streamlit application:

streamlit run app.py

The application will run locally at:

http://localhost:8501

## 📁 Project Structure

ai-data-analyst-agent/
│
├── app.py
├── test_api.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── analysis/
├── charts/
├── data/
└── reports/

## 🎯 Use Case

This project is designed to simplify exploratory data analysis by automating repetitive data-cleaning, statistical-analysis, visualization, and business-insight tasks.

It can be useful for students, analysts, developers, and businesses that need quick insights from structured datasets.

## 🔮 Future Improvements

- 📑 PDF report generation
- 📊 More advanced visualizations
- 📈 Sales forecasting
- 🤖 Natural-language data querying
- 🧠 Advanced AI-driven recommendations
- ☁️ Cloud deployment
- 👥 User authentication
- 📁 Support for larger datasets

## 👩‍💻 Author

**Khushi Vyas**

MCA — Full Stack Web Development