## Usage

##### Localy
Install locally 

```bash
echo -e 'SECRET_KEY="<secretkey>"\nDEBUG=True' > .env
make migrate
make run-dev
```
Upload Sample DB from the task.

```bash
make user-create
curl -u <username>:<password> -X POST -d '"https://gist.githubusercontent.com/kotik/3baa5f53997cce85cc0336cb1256ba8b/raw/3c2a590b9fb3e9c415a99e56df3ddad5812b292f/dataset.csv"' --header 'Content-Type: application/json' http://<django-url>/upload
```

##### Heroku

**[Preview on Heroku](https://aht-linked.herokuapp.com/)**



##### CPI
```
https://<django-url>/data_api/?cpi"
```

##### GROUP_BY
```
https://<django-url>/data_api/?group_by=<key>
Keys:
    country
    date
    channel
    os
```