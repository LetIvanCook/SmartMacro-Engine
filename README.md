# SmartMacro Engine: Constraint-Based Nutritional Optimization

## 📌 Project Overview
**SmartMacro Engine** is a high-performance web application designed to solve a complex constraint optimization problem in fitness and nutrition. Unlike standard calorie-tracking apps, this engine dynamically calculates the exact gram-level measurements of available ingredients to meet precise macronutrient targets. The calculations automatically adjust based on the user's specific training cycle, such as the Push-Pull-Legs (PPL) split, ensuring optimal physical recovery and performance.

## 🚀 Core Features
* **Algorithmic Meal Generation:** Implements Linear Programming and Backtracking algorithms to compute the optimal combination of raw ingredients, minimizing food waste while hitting daily macro targets with zero-to-minimal deviation.
* **Dynamic Workload Adaptation:** Automatically shifts carbohydrate and protein requirements based on the intensity of the workout day (e.g., maximizing carbs for 'Legs' day, prioritizing protein for 'Push/Pull' days).
* **Inventory & Concurrency Management:** Tracks real-time ingredient inventory. Utilizes robust transaction locks and database triggers to ensure data integrity during simultaneous inventory updates.
* **Automated Software Testing:** Core algorithms are heavily tested using structured methodologies, including Equivalence Partitioning and Boundary Value Analysis, ensuring the system handles edge cases (e.g., zero inventory, mathematically impossible macro targets) without crashing.

## 💻 Tech Stack & Architecture
This project strictly follows a **3-tier architecture** (Presentation, Business Logic, and Data Access layers) to ensure scalability and maintainability.

* **Frontend (Presentation Layer):**
  * UI/UX designed entirely from scratch using **Figma**.
  * Developed using responsive **HTML, CSS, and vanilla JavaScript** for a lightweight and lightning-fast user experience.
* **Backend & Core Engine (Business Logic Layer):**
  * Built with **Java**, serving as the mathematical core for processing optimization algorithms and discrete values.
* **Database (Data Access Layer):**
  * Managed via **SQL Server Management Studio 20**.
  * Advanced database logic implemented through **T-SQL** (Stored Procedures and Triggers) to optimize query speed and enforce strict data constraints at the database level.

## 🧠 Why This Project?
This system was developed to bridge the gap between abstract mathematical algorithms and real-world fitness challenges. It serves as a comprehensive showcase of algorithmic problem-solving, clean code principles, database optimization, and end-to-end software engineering capabilities.
