# Castellana Due Diligence Service

## Overview

**Castellana** Due Diligence Service is an Agentic tool that converts startups documentation and notes into a first-draft investment memo tailored to VC. Built to reflect how I personally assess companies, Castellana is open source with the goal of improving automatise my investment process.

## Getting Started

### Prerequisites

Before installing, make sure the following are installed:

- Node.js version 16 or later  
- Python version 3.8 or later  
- npm and pip  
- Google Cloud SDK

You will also need these API keys set up as environment variables:

- OpenAI API Key  
- Portkey API Key  
- EXA AI API Key  
- Proxycurl API Key  
- Google Cloud Vision API credentials in JSON format

## Installation

1. Clone the repository

```bash
git clone https://github.com/your-username/castellana-memo.git
cd castellana-memo
```

2. Install Node.js dependencies

```bash
npm install
```

3. Install Python dependencies

```bash
pip install -r requirements.txt
pip install 'crewai[tools]'
```

4. Build the project

```bash
npm run build
```

## Environment Variables

Create a `.env` file in the root directory with the following content:

```env
OPENAI_API_KEY=your-openai-api-key
EXA_API_KEY=your-exa-api-key
PROXYCURL_API_KEY=your-proxycurl-api-key
GOOGLE_APPLICATION_CREDENTIALS=./cloud-credentials.json
PORTKEY_API_KEY=your-portkey-api-key
PORT=3002
GOOGLE_CLOUD_PROJECT_ID=castellana-due-diligence
```

## Google Cloud Vision Setup

1. Create a Google Cloud project  
2. Enable the Cloud Vision API in the API Library  
3. Create a Cloud Storage bucket  
4. Assign IAM roles to your service account:  
   - Storage Object Admin  
   - Storage Object Creator  
   - Storage Object Viewer  
   - Cloud Vision AI Service Agent  
5. Download the credentials JSON file and place it in the project root as `cloud-credentials.json`

## Usage

### Development

To run the development server with backend and frontend:

```bash
npm run dev
```

### Production

To build and run the production server:

```bash
npm run build
npm start
```

## Project Structure

- `index.js` – Main backend server  
- `main.py` – Market analysis logic  
- `agents.py` – Automated research agents  
- `tasks.py` – Supporting Python logic  
- `.env` – Configuration file  
- `package.json` – Node.js settings  
- `requirements.txt` – Python packages

## License

This project is released under the GNU Affero General Public License v3.0. See the LICENSE file for details.

## Disclosure

Castellana Due Diligence Service is meant to support the diligence process, not to serve as a final decision-maker.
