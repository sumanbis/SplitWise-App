# Expense Sharing System

## Table of Contents
- [Introduction](#introduction)
- [API Contracts](#api-contracts)
- [Class Structure](#class-structure)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
This document provides an overview of the Expense Sharing System, API contracts, and the structure of its classes. The system is designed to facilitate expense management and sharing among a group of users.

## API Contracts
### Expense Creation API
- **Endpoint:** `/api/record_expense`
- **Method:** POST
- **Request Payload:**
  - `amount` (decimal)
  - `expense_type` (string)
  - `participants` (list of user IDs)
  - `payer` (user ID)
- **Response:**
  - 201 Created: Expense recorded and balances updated
  - 400 Bad Request: Invalid input data

### Balance List API
- **Endpoint:** `/api/balance`
- **Method:** GET
- **Response:**
  - 200 OK: 
    - `user` (json)
    - `owed_to` (json)
    - `amount` (ddecimal)
  - 404 Not Found

### Views
- `ExpenseCreateView`: Add Expense, Split amount, save and update in database.
- `BalanceListView`: List all the expenses.

### Models
- `UserProfile`: Represents user information, including name, email, and mobile number.
- `Expense`: Represents an expense with fields such as amount, expense type, participants, and payer.
- `Balance`: Represents balances between users, including the owed amount.

### Serializers
- `UserProfileSerializer`: Serializes user data.
- `ExpenseSerializer`: Serializes expense data.
- `BalanceSerializer`: Serializes balance data.

## Installation
- Clone repository 
- pip install requirements.txt
- python manage.py runserver

## Usage
- python manage.py runserver
- Use postman
- To add expense: 
- `POST Api`: http://127.0.0.1:8000/app/record_expense/
- `Body`: 
    - expense type = equal:    
        {
            "payer": 1,
            "participants": ["1", "2", "3"],
            "amount":1000,
            "expense_type": "EQUAL"
        }
        
    - expense type = exact:
        {
            "payer": 1,
            "participants": [2, 3],
            "amount": 1250,
            "expense_type": "EXACT",
            "owed_amounts": {
                "2": 370,
                "3": 880
            }
        }
    - expense type = percentage:
        {
            "payer": 4,
            "participants": [1, 2, 3, 4],
            "amount": 1200,
            "expense_type": "PERCENT",
            "percentages": [40, 20, 20, 20]
        }

- `GET API`: http://127.0.0.1:8000/app/balances/
- `Admin Url`: http://127.0.0.1:8000/admin
      - User: admin
      - password: 123456
