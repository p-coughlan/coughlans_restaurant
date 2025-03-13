# Project Overview

**Coughlan's Restaurant** is a web application for a fictional restaurant that enables users to make and manage table bookings, submit reviews, and view current menus. The application is built using **Django**, **Python**, and **PostgreSQL**, with a responsive front-end styled using **Bootstrap** and custom CSS.

## Features

- **Booking System:**
  - Users can easily book a table through an intuitive form.
  - A custom confirmation page is displayed upon successful booking.
  - Staff can manage bookings using dedicated views, including daily, weekly, and monthly calendar displays.

- **Review Submission:**
  - Customers can submit reviews using a star-based rating system.
  - Reviews are stored as numerical values and are displayed on the homepage once approved by an admin.

- **Menu Display:**
  - Static pages present the restaurant’s lunch and dinner menus.
  - Menus can be updated seasonally to reflect available dishes.

- **Admin & Staff Functionality:**
  - Staff have access to custom booking management interfaces directly from the website.
  - The application also leverages Django's admin panel for advanced management tasks.

*Screenshots and additional images can be added later to visually illustrate these features.*

## Technologies Used

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Django](https://img.shields.io/badge/Django-4.2-blue?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Heroku](https://img.shields.io/badge/Heroku-Deploy-purple?style=for-the-badge&logo=heroku&logoColor=white)](https://www.heroku.com/)
[![Adobe Photoshop](https://img.shields.io/badge/Adobe-Photoshop-blue?style=for-the-badge&logo=adobe-photoshop&logoColor=white)](https://www.adobe.com/products/photoshop.html)
[![Git](https://img.shields.io/badge/Git-2.34-orange?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)  
[![GitHub](https://img.shields.io/badge/GitHub-202?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)  
[![VS Code](https://img.shields.io/badge/VS%20Code-1.62-blue?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)


## Technologies Used (Without verion numbers)

[![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)  
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)  
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)  
[![Django](https://img.shields.io/badge/Django-blue?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)  
[![Python](https://img.shields.io/badge/Python-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)  
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)  
[![Heroku](https://img.shields.io/badge/Heroku-purple?style=for-the-badge&logo=heroku&logoColor=white)](https://www.heroku.com/)  
[![Adobe Photoshop](https://img.shields.io/badge/Adobe%20Photoshop-blue?style=for-the-badge&logo=adobe-photoshop&logoColor=white)](https://www.adobe.com/products/photoshop.html)  
[![Git](https://img.shields.io/badge/Git-orange?style=for-the-badge&logo=git&logoColor=white)](https://git-scm.com/)  
[![GitHub](https://img.shields.io/badge/GitHub-blue?style=for-the-badge&logo=github&logoColor=white)](https://github.com/)  
[![VS Code](https://img.shields.io/badge/VS%20Code-blue?style=for-the-badge&logo=visual-studio-code&logoColor=white)](https://code.visualstudio.com/)

## Setup and Installation

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
2. **Create and Activate a Virtual Environment:**
- On macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
- On Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
3. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
4. **Configure Environment Variables:**
- Create a .env file in the project root and add:
    ```env
    SECRET_KEY=<your_secret_key>
    DATABASE_URL=<your_postgresql_database_url>
5. **Run Migrations**
    ```bash
    python manage.py migrate
6. **Collect Static Files** (Optional, for production deployments)
    ```bash
    python manage.py collectstatic --noinput
7. **Start the Development Server**
    ```bash
    python manage.py runserver
