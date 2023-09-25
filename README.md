# Google Maps Converter

Google Maps Converter is a web application built with Flask that allows you to perform various conversions related to Google Maps, such as converting addresses to latitude and longitude coordinates, converting latitude and longitude coordinates to addresses, and obtaining the bounding box coordinates of a city.

## Features

- **Address to Lat-Lng Conversion**: Enter an address, and the app will provide you with its corresponding latitude and longitude coordinates.

- **Lat-Lng to Address Conversion**: Provide latitude and longitude coordinates separated by a comma, and the app will return the associated address.

- **City Bounding Box**: Get the bounding box coordinates (NORTHEAST_LAT, NORTHEAST_LNG, SOUTHWEST_LAT, SOUTHWEST_LNG) of a city by specifying its name.

## Getting Started

To run this application locally, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/google-maps-converter.git
   cd google-maps-converter
   ```

2. Set up your Google Maps API Key by exporting it as an environment variable:
   
   ```bash
   export GOOGLE_MAPS_API_KEY="your-api-key"
   ```

3. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
   
4. Run the Flask application:

   ```bash
   python run.py
   ```
5. Access the app in your web browser at http://localhost:5000.

## Usage

1. Choose the conversion type from the dropdown menu.

2. Enter the input data based on the selected conversion type.

3. Click the "Execute" button to perform the conversion.

4. View the result in the designated area. Any errors will be displayed in case of issues.

## Contributions

Contributions are welcome! If you'd like to add new features, fix bugs, or improve the project in any way, please feel free to open issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- This app is built using the Flask web framework.
- We rely on the Google Maps Geocoding API for address and coordinate conversions.

