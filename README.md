# sheetgo

To run this application you must have python >=3.6.

## How to run

### Using venv
1. Create a virtual environment: `python3 -m venv venv`
2. Activate the venv: `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Set the following environment variable to use Dropbox: `DROPBOX_ACCESS_TOKEN`
5. Run it: `python sheetgo.py`

#### Examples:
```bash
# firstly, create venv and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# set DROPBOX_ACCESS_TOKEN
export DROPBOX_ACCESS_TOKEN=73a90acaae2b1ccc0e969709665bc62f  # this is not a valid Dropbox access token

# runt it
python sheetgo.py
```
Output:
```
 * Serving Flask app "sheetgo" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### Tests

Open a new terminal on the project root path.

#### To run the unit tests:

```bash
source venv/bin/activate
python -m unittest
```

#### To test the entrypoints:

Entrypoint /excel/info:
```bash
# first, activate the venv
source venv/bin/activate
bash tests/entrypoint_excel_info_test.sh tests/sheetgo_tabs_sample.xlsx
```

Entrypoint /image/convert:
```bash
source venv/bin/activate

# from jpeg to png
bash tests/entrypoint_image_convert_test.sh tests/street-lights.jpg png /tmp/sl.png
# where:
# tests/street-lights.jpg = input image
# png = output format
# /tmp/sl.png = output image

# from png to jpeg
bash tests/entrypoint_image_convert_test.sh  tests/street-lights.png  jpeg  /tmp/sl.jpg
```


Entrypoint /image/convert/fromdropbox:
```bash
source venv/bin/activate

export DROPBOX_ACCESS_TOKEN=73a90acaae2b1ccc0e969709665bc62f  # this is not a valid Dropbox access token

# from jpeg to png
bash tests/entrypoint_image_convert_fromdropbox_test.sh  /Photos/street-lights.jpg  png /tmp/sl.png
# where:
# /Photos/street-lights.jpg = input image path on Dropbox
# png = output format
# /tmp/sl.png = output image

# from png to jpeg
bash tests/entrypoint_image_convert_fromdropbox_test.sh  /Photos/street-lights.png  jpeg  /tmp/sl.jpg
```


