<!-- ABOUT THE PROJECT -->
## About The Project

UWC 2.0 :smile:

This project aims  to provide a Task Management System for Back Officer:
* View task of each Worker (Janitor, Collector)
* View information of Vehicle, Trolley, MCP, Area
* Assign task for each Worker (Janitor, Collector)
* Message each Worker (Janitor, Collector)


### Built With
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![Django][djangoproject.com]][Django-url]

## Getting Started

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/namkha1032/SoftwareEngineering-Assignment.git
   ```
2. Install packages
   ```sh
   pip install -r requirements.txt
   ```
3. Migrate database
   ```sh
   python manage.py migrate
   ```

## Usage

Run the website
   ```sh
   python manage.py runserver
   ```

The account for each Back Officer will be provided by the company, so Back Officer
can not register account, here the account that we provided to you to log in

Username: admin

Password: 12345

If you can not log in using the above account, create an account

   ```sh
   python manage.py createsuperuser
   ```
Then you proceed to create a Username and Password.


