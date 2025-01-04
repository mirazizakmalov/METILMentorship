# Virtual Mentorship System

The **Virtual Mentorship System** is a web application designed to provide mentorship and learning resources for employees. The system enables users to ask questions, access recommended resources, take tests to evaluate their knowledge, and review questions and answers.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Features
1. **Ask a Question**: Users can ask questions and receive answers based on a preloaded knowledge base.
2. **Recommend Resources**: Suggests relevant resources and documents for learning based on a given topic.
3. **Take a Test**: Users can take a test to assess their knowledge and receive feedback.
4. **Review Questions**: Browse previously asked questions and answers for reference.
5. **User-Friendly Interface**: A clean and intuitive user interface for seamless interaction.

---

## Tech Stack
### Frontend
- **Vue.js**: For building the user interface.
- **Axios**: For making API requests.
- **HTML/CSS**: For structuring and styling the UI.

### Backend
- **Flask**: As the backend framework.
- **SQLite**: For storing questions, answers, and resources.
- **PyTorch**: For implementing AI models.
- **Hugging Face Transformers**: For question-answering and semantic similarity tasks.

---

## Installation

### Prerequisites
- **Python 3.8+**
- **Node.js 14+**
- **npm or Yarn**

### Backend Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. Create a virtual environment
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies

4. Run Flask Server
    python app.py

5. Navigate to front end folder
    cd mentorship-Frontend

6. Donwload dependencies
    npm install

7. Run development server
    npm run serve
