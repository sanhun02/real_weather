# Real Weather

An application that fetches real-time weather of any city using Django and [OpenWeatherMap API] (https://openweathermap.org/api). Features the ability to add and delete from a user's watchlist.

![real_weather](https://user-images.githubusercontent.com/113066180/220251572-e065d19d-11f5-4d7b-897e-a1e495f79169.gif)

## Setup

First clone the repository:

```bash
$ git clone https://github.com/sanhun02/real_weather.git
$ cd weatherProject
```

Install project dependencies:

```bash
$ pip install -r requirements.txt
```

Create database tables and a superuser account:
```bash
$ py manage.py migrate
$ py manage.py createsuperuser
```

Now you can run the development server:
```bash
$ py manage.py runserver
```
