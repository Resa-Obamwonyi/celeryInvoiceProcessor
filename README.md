## Task Description
A celery task that fetches the invoice data from a FTP Server (similar to Client 3) once per day and uploads it to the existing API.

## Tools
- Django
- Celery
- Redis

## Needed Setup Tools
- Virtual environment for installing requirements
- An .env file for storing secrets

## Testing
- All tasks in the project are run once the app, celery and the redis worker are up and running
- To start the app, `python manage.py runserver`
- To run the redis worker: `redis server`
- To run celery and see a list of available tasks, activate the venv, then run 
    - `python3 -m celery -A invoice_scheduler worker -l info`
- To run the Celery worker as a background process
    - `celery -A invoice_scheduler --workdir=. beat -l info --logfile=celery.beat.log --detach`
    - `celery -A invoice_scheduler --workdir=. worker -l info --logfile=celery.log --detach`
- To view the status and logs of the background tasks
    - `cat celery.beat.log`
    - `cat celery.log`

- To kill all worker processes
    - `pkill -f "celery worker"`

