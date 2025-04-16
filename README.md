# AutoHaggle

## Overview
**AutoHaggle** is an AI-powered car pricing and negotiation platform designed to help users predict fair prices, compare dealer quotes, and secure the best deals. By leveraging historical data, regional market trends, and community-shared quotes, AutoHaggle provides accurate price estimates and negotiation insights.

---

## Structure of this project

### Data Processing, Model Exploration and Final Model development
- **./scripts**

### Frontend
- **./app**
- **./components**
- **./lib**
- **./public**

### Backend
- **./server**

## How AutoHaggle Works

### 1. Create a New Deal with Dream Car Parameters
Users start by entering details about their desired car, including:
- **Make, model, and year**
- **Mileage and condition**
- **Location**  

Our system analyzes historical sales data and regional market trends to generate a fair price estimate.

### 2. Get AI-Powered Price Predictions
AutoHaggle uses a **hybrid machine learning approach** to deliver highly accurate price predictions:
- **Clustering**: Users are assigned to a data cluster with similar and relevant listings.
- **Model Selection**: Based on the identified cluster, the best-performing model is applied to predict the car’s price.

Key factors considered:
- **Historical transaction data** – Identifying price patterns based on past sales.
- **Regional supply and demand trends** – Adjusting prices based on local market conditions.

### 3. Compare Dealer Quotes with Community-Shared Data
Once users receive a quote from a dealer, they can compare it with similar quotes in the **community-driven quote database**. This helps users determine if their offer is fair or if better deals are available.

### 4. Beat Dealer Quotes & Negotiate a Better Price
AutoHaggle provides **LLM-based negotiation strategies** *(Coming Soon)* to help users identify leverage points in their dealer quotes. The AI-powered suggestions will analyze:
- **Hidden fees and financing terms**
- **Regional market trends**
- **Alternative pricing options**  

These insights guide users on how to negotiate lower costs and maximize savings.

### 5. Secure the Best Deal & Share Final Quote
After purchasing a car, users can **share their final dealer quote** with the community. This strengthens AutoHaggle’s machine learning models, improves pricing accuracy, and helps others make informed decisions. Every shared deal contributes to a more **transparent and fair** car-buying ecosystem.

---

## Technology Stack

### **Machine Learning & AI Models**
- **Price Prediction** – Hybrid model using clustering and model selection.
- **Quote Matching** – Clustering algorithms to group similar dealer offers.

### **Backend & Data Processing**
- **Python & TensorFlow** – Powering price predictions and negotiation analysis.
- **PostgreSQL** – Storing user data, dealer quotes, and transaction history.

### **Frontend & User Interface**
- **React.js & Next.js** – Providing a fast, dynamic, and user-friendly experience.
- **Node.js & Express** – Handling API interactions and data processing.

---

## Getting Started

### **Clone the Repository**
```sh
git clone https://github.com/your-repo/AutoHaggle.git
cd AutoHaggle
```

### **Install Dependencies**
Ensure you have Python and Node.js installed, then install the required dependencies:

#### **Backend (Python)**
```sh
pip install -r requirements.txt
```

#### **Frontend (Node.js)**
```sh
npm install
```

### **Run the Application**
#### **Start the Backend**
```sh
python app.py
```

#### **Start the Frontend**
```sh
npm run dev
```

---

## Future Plans
- **Expand dealer partnerships** to incorporate real-time pricing data.
- **Enhance negotiation AI models** for personalized recommendations.
- **Implement predictive price forecasting** to help users time purchases effectively.
- **Develop a real-time negotiation chatbot** for dealer interactions.

---


For discussions or issues, please open an issue on GitHub.

---

## License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## Dataset Information
We are getting our data from a kaggle dataset. It represents a collection of used car transactions with details about the car. The purpose of collecting this data is to build a database and predictive model that users can interact with to get an accurate price for a used car. The data is publicly available and there are no restrictions on its use that we have found.
https://www.kaggle.com/datasets/syedanwarafridi/vehicle-sales-data