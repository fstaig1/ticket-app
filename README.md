# Ticket Finder

Ticket purchasing app I have created for my dissertation.
___

## How to run

1. Open project file in VSCode or IDE of your choice.
2. Create a new venv and install `requirements.txt`
    -   `python -m venv /venv`
    -   `pip install -r requirements.txt`
3. Run `main.py`
4. Open <http://127.0.0.1:38255>

___

## Default User Details

| Email            | Password     | Role    |
| ---------------- | ------------ | ------- |
| `admin@test.com` | `Password1!` | `user`  |
| `user@test.com`  | `Password1!` | `admin` |
| `venue@test.com` | `Password1!` | `venue` |
| `david@test.com` | `Password1!` | `user`  |
| `eric@test.com`  | `Password1!` | `user`  |
| `frank@test.com` | `Password1!` | `user`  |


___

## What the User Roles Mean

- `user`
  - default user role, has no special permissions
- `admin`
  - can access the admin dashboard
  - can view all tables in database
  - can remove rows from database
  - can create new users and venues

- `venue`
  - each venue manager is assigned a venue to manage on creation
  - can access the venue dashboard
  - can view details about the venue including:
    - Name, capacity, location, list of all concerts
  - can create new concerts at their venue

___

## Important

- This is only deployed on a localhost as a proof of concept.
- If the database must be initialised, remove the quote marks from lines 59-62 in `main.py`

    ``` Python
    59.  # uncomment this to re initialise the database
    60.  """
    61.  with app.app_context():
    62.      init_db()
    63.  """
    ```
