# SnowFort UI

SnowFort is an open source data analytics system for wireless sensor network. It uses previously available open source
hardware with a new open source communication scheme to allow for simple, reliable, and flexible wireless sensor
networks. SnowFort is developed by the faculties and students at Stanford University. The goal of this project is
helping developers and researchers to rapidly develop a network for sensing without the time or background to develop
the entire system from scratch.

## Requirements

See `requirements.txt` for required packages. These are python packages that should be installed using `pip`.

## Build Database

In the top directory of this project run the following:

```python
python shell.py
>>> from snowfort import db
>>> db.create_all()
>>> exit()
```

## Run Application

In the top directory of this project run the following:

```python
python run.py
```

You should then be able to access from the browser at `<ip-address>:5000` or possibly `localhost:5000`.

## Demo Application and Real-Time Graph

Delete the `development.db` database in the `snowfort` folder if you've made one before.

```python
python demo.py
```

This will set up the demo with some test data in the system. There will be a default user of: `richardhsu.cs@gmail.com`
and password `mypasswordcool`.

From there you can run the application.

### Real-Time Graphs

You can start up the real-time graph demo by going to a station view for example `<ip-address>:5000/stations/view/1` and
enabling the real-time graph. Then you'll want to set up the data generator which is also at the top level directory
and can be run by typing:

```python
python realtimedemo.py
```

You can kill this when you'd like but it'll will run forever and update the database every second.
