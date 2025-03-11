
# StockTalk API

## 📌 Overview

StockTalk is a robust API designed to facilitate discussions on stock market trends, investment strategies, and financial topics. Users can create posts, categorize them, engage in discussions through comments, and create watchlists to manage bullish stocks.

## 🔗 Live Project & Resources

[GitHub Project Board](https://github.com/orgs/e27-BE-Capstone/projects/1)

Postman Documentation: https://documenter.getpostman.com/view/33996164/2sAYk7S4V5

ERD: https://dbdiagram.io/d/BE-Capstone-StockTalk-67b96fb0263d6cf9a010a217 

FIGMA: https://www.figma.com/board/QyMBqD3u8E6gXNocy04zrl/BE-Capstone---StockTalk?node-id=0-1&t=foasqyfHGmyWz1mw-1

Loom Video Demo: 

## 👥 Target User

StockTalk is designed for:

- Investors looking for a platform to discuss market trends.

- Financial analysts sharing insights.

- Casual users tracking stocks and engaging in discussions.

## 🚀 Features

User Authentication: Sign up and log in with Firebase authentication.

FULL CRUD Operations for User, Post, Categories, Watchlists, and Comments 

Post Management: Users can create, read, update, and delete posts.

Categorization: Posts can be categorized for easy filtering.

Watchlists: Track stocks with personalized notes.

Comment System: Engage in discussions under posts.

RESTful API: Fully structured API following best RESTful practices.

## 🛠️ Tech Stack

- Django Rest Framework (DRF)
- Firebase Authentication
- Next.js

## 👨‍💻 Contributors

Andre Phosarath - [GitHub Profile](https://github.com/AVP4000)

## 📜 Installation & Setup

#### Clone the repository:

git clone https://github.com/e27-BE-Capstone/BE-Capstone-StockTalk

#### Navigate to the project folder:

cd stocktalk-api

#### Create and activate a virtual environment:

Back-End Start-Up
Pipenv shell <<------Only have to do once


#### Install dependencies:

Pipenv install <<---Only have to do once


#### Apply migrations:

Python manage.py makemigrations <<---Creates a migrations file (django database business)
Python manage.py migrate <<---- updates the database from that file


#### Start the development server:

python manage.py runserver

#### 🛠️ Running Tests

#### To run the test suite:

python manage.py test stocktalkapi.tests

## 📩 Contact

For inquiries or collaboration, reach out to andrepho22@gmail.com or [GitHub Profile](https://github.com/AVP4000)