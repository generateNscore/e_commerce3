e_commerce3
![Preview](screen.jpg)


## ✨ Key Features

This GitHub repository is a **PyCharm** project developed to practice full-stack development. 
The core technologies and APIs used include:

* **Python**-based backend
* **FastAPI** framework
* **PostgreSQL** database
* **RESTful API** communication between Frontend and Backend

While it is not a commercial-grade application, it is highly complete and allows you to test the project using your own database consisting of 5 tables (See `e_commerce3_models.pptx` for a full description).

You can explore the detailed structures of the tables, columns, and relationships in the project files (see below to clone and set up the project).

## ⚙️ Installation and Configuration

If you need help cloning the repository into PyCharm, please refer to this guide:
[How to create a project folder in PyCharm with a GitHub repository](https://www.google.com/search?q=how+to+create+project+folder+in+pycharm+with+a+github+repository)

If you encounter any issues, feel free to contact me at smlee@inha.ac.kr.

### Prerequisites
Before proceeding, make sure you have **PyCharm** and **PostgreSQL** installed on your PC. Then, follow these two steps:

1. Open the Terminal in PyCharm and run the following command to install all required libraries:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a file named `.env` in the project root folder and paste the following line:
   ```env
   DATABASE_URL=postgresql+psycopg2://postgres:{your_password}@localhost:5432/e_commerce_db
   ```
   *Note: This file is required for the project to run. Replace `{your_password}` with the password you set during PostgreSQL installation.*

## 🧩 Running the Cloned Project

To start the backend server, open the Terminal and run:

```bash
uvicorn app.main:app --reload
```

Once you see `"Application startup complete."` at the end of the log, your backend server is ready. The server runs on the default port `8000`.

### Accessing the Project
You can access the project in your browser using two different URLs:

1. **Frontend / Main Interface**

```
http://127.0.0.1:8000
```

*The page will display the main dashboard screen, likely showing all 0s initially.*

2. **FastAPI Interactive Docs (API Endpoints)**

```
http://127.0.0.1:8000/docs
```

*This page is a swagger ui screens that displays the interactive FastAPI endpoints. The `POST /admin/generate_data` endpoint is the gateway to creating your initial database.*

---

### 🗄️ How to Generate Initial Data

By default, clicking **Try it out** -> **Execute** on the `POST /admin/generate_data` endpoint will only trigger a built-in `analyse(db)` function without populating the database. 

To populate and set up your own database, follow these steps:

1. Open `app/config.py` and change the value of `DEBUG_RESET_DB` from `False` to `True`:

```python
DEBUG_RESET_DB = True
```

2. Open `app/routers/admin.py` and locate the data generation code:

```python
world = generate_fake_data(customer_count = 567,
                           product_count = (5,6),
                           order_count = 8901,
                           city_count = 5)
```

*You can keep these default values or modify the numbers to adjust the amount of mock data generated.*
3. (Recommended) After generating the data, change `DEBUG_RESET_DB` in `app/config.py` back to `False`. Otherwise, your database will be deleted and recreated every time the endpoint is executed.
4. When `DEBUG_RESET_DB` is set to `True`, the console will output a series of analytical logs verifying the SQL queries used in the frontend dashboard.


## 📄 License
MIT License - free for personal and commercial use.
---
Made to be cloned and run instantly. If you get the same screen as `screen.jpg`, setup succeeded.
