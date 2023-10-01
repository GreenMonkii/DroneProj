# Drone Application README.md

## Description

This is a Django application that demonstrates how to get the battery level of a drone.

## Installation

To install the application, clone the repository and run the following command:

```
pip install -r requirements.txt
```

## Usage

To start the development server, run the following command:

```
python manage.py runserver
```

The development server will be available at `http://localhost:8000/` in your web browser.

## Tests

To run the tests, run the following command:

```
python manage.py test
```

The tests will be run and the results will be displayed in the console.

## Build

To build the project for production, run the following command:

```
python manage.py collectstatic


This will collect all of the static files into the `static/` directory.

## Deployment

To deploy the application to production, you can copy the contents of the project directory to your production server.

## Getting the battery level

To get the battery level of a drone, run the following command:


python manage.py get_battery_level <drone_id>
```

This will return the battery level of the drone with the specified ID.

## Example

The following example shows how to get the battery level of the drone with the ID 1:

```
python manage.py get_battery_level 1
```

This will return the battery level of the drone as a percentage.

## License

This application is licensed under the MIT License.