# CanyonDB
Free time optimizer for canyonners.

When you have only X hours and a cord of length Y and you want to go out for a canyon, this tool allow you to select the better rated canyon for the time and the cord you have.

## How to use me

1. Screen-scrap the database from //descente-canyon.com//
`scrapy runspider canyon-scrap.py -o canyons.json --logfile=canyons.log`

### MongoDB version

*Prerequisites:* python + pymongo + flask + MongoDB server + MongoDB mongoimport client utility

2. Insert this database into MongoDB
`remove '[' and ']' from canyons.json
mongoimport --db canyons --collection canyons --file canyons.json`
3. Get driving times from google maps server
`driving_compute-mongo.py`
4. Do a little bit of denormalization and formatting on the database
`denorm_and_format-mongo.py`
5. Launch the web server
`server-mongo.py`
6. Browse `http://localhost:30000/static/index.html`

### Text version

*Prerequisites:* python + flask

2. Get driving times from google maps server
`driving_compute-text.py`
3. Do a little bit of denormalization and formatting on the database
`denorm_and_format-text.py`
3. Launch the web server
`server-text.py`
4. Browse `http://localhost:30000/static/index.html`
