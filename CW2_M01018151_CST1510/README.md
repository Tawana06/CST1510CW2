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