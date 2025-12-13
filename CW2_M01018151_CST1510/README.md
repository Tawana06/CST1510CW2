# Week 7: Secure Authentication System
Student Name: [Tawana I Gwatidzo] \
Student ID: [M010118151] \
Course: CST1510 -CW2 - Multi-Domain Intelligence Platform

## Project Description
A command-line authentication system implementing secure password hashing
This system allows users to register accounts and log in with proper pass

## Features
- Secure password hashing using bcrypt with automatic salt generation
- User registration with duplicate username prevention
- User login with password verification
- Input validation for usernames and passwords
- File-based user data persistence

## Technical Implementation
- Hashing Algorithm: bcrypt with automatic salting
- Data Storage: Plain text file (`users.txt`) with comma-separated values
- Password Security: One-way hashing, no plaintext storage
- Validation: Username (3-20 alphanumeric characters), Password (6-50 cha


# Intelligence Platform - Week 8 Database Implementation

## Project Structure


## Features
- SQLite database with 4 tables
- User authentication with bcrypt
- CRUD operations for all domains
- CSV data loading
- Analytical queries

## Setup
1. Run `pip install -r requirements.txt`
2. Run `python main.py` to initialize database
3. Add your CSV files to the DATA folder

## Database Schema
- users: User authentication
- cyber_incidents: Security incidents  
- datasets_metadata: Dataset information
- it_tickets: IT support ticketss

# Week 9 Intelligence Platform

## Web Interface, MVC and Visualisation

## Features
- login
- register user
- session managment
- cybersecurity dashboard
- data science dashboard
- it dashboard
- bar charts
- line graphs
- datatables

# Implementations
- no domain or dashboard can be accessed without logging in first
- all dashboards are session controlled
- all dashboards contain charts displaying their data
- all dashboards have filters on the sidebar
- all dashboards can be accessed from the main dashboard

# Week 10 Intelligence Platform

## AI Integration

# Features
- gemini AI
- api key managment
- AI assistant on the dashboard

# Implementation
- any user can access the AI Assistant and ask it questions
- AI Assistant can reply user
- AI assistant can store history for the session only

# Week 11 Intelligence Platform

## OOP Refactoring

# Features
- rewriting the code in OOP (Object Oriented Programming)

# Implementation
- created a new folder called multi_domain_platform
- rewrote every code necessary using OOP
- created a new 00P_home,py to run the OOP code domain

# Notes
- inside the folder there are now two intelligence_platform.db
- one is accessed through home.py and it is the one made with the original code without OOP
- the other one is in the multi_domain_platform folder and can be accessed through OOP_home.py and it is OOP code
- both of them work on streamlit, its just the coding foundation that is different
- OOP_home,py was made using the tutorial and the original home.py code files however there are some slight differences in the dashboard display.
- regardless of these slight differences, both dashboard work the same way

# Requirements

## Requirements to run the domains
- the main folder 'CW2_MO1018151_CST1510' is marked as a sources root
- the folder 'multi_domain_intelligence' inside the main folder is also marked as a source root
- when running streamlit in the terminal one has to put the whole full path for example streamlit run C:\Users\gwati\PycharmProjects\newproject\CW2_M01018151_CST1510\home.py for it to work. I have attached the examples and the full path as comments at the top of the home codes.
- once on the domain if registers a new account, they then have to login to be able to access the dashboards

- to run the codes, make sure you have the following libraries installed
* bcrypt
* streamlit
* pandas
* os
* sqlite3
* re
* google genai

