# EmpathZ AI Coordinator

A Streamlit demo application for analyzing and assessing crisis calls in real time.

## Features

- **Real-time Call Analysis**: AI-powered summarization and risk assessment
- **Interactive Dashboard**: View call transcripts, risk scores, and analytics
- **Risk Evaluation**: Four-dimensional risk assessment (Suicide, Homicide, Self-harm, Harm-others)
- **PDF Reports**: Generate and download comprehensive call analysis reports
- **Analytics**: Track total calls, risk distribution, and response times

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Select a call from the "Recent Calls" list
2. View the conversation transcript and AI analysis
3. Review risk assessment scores and reasoning
4. Download PDF reports for individual calls
5. Monitor overall analytics and trends

## Technology Stack

- **Streamlit**: Web application framework
- **Python**: Backend logic and data processing
- **ReportLab**: PDF report generation
- **Custom CSS**: Styling and theming

## Demo Data

This application includes 10 simulated crisis calls with pre-computed analysis results for demonstration purposes.