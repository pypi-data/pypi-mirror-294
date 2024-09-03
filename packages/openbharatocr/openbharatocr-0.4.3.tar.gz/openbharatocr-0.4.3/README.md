# openbharatocr
[![Build status](https://github.com/essentiasoftserv/openbharatocr/actions/workflows/main.yml/badge.svg)](https://github.com/essentiasoftserv/openbharatocr/actions/workflows/main.yml)

openbharatocr is a Python library developed as open-source, designed specifically for optical character recognition (OCR) of Indian government documents.

The features of this package:
- It offers comprehensive support for the majority of Indian government documents, covering a wide range of document types. 

### Setting Up a Development Environment for OpenBharatOCR
This guide details how to establish a development environment for OpenBharatOCR on a Linux system (Ubuntu/Debian preferred). If you're using Windows or macOS, consider using a virtual machine or a Linux subsystem (WSL2 on Windows, Docker on macOS).

**Prerequisites:**

- Operating System: Linux (Ubuntu/Debian preferred)
- Python 3.6 or later: Check the version with `python3 --version` or `python --version` in your terminal. Download the latest installer from https://www.python.org/downloads/ if needed.

**Installation:**

- Clone the openbharatocr repository:

``` 
git clone https://github.com/essentiasoftserv/openbharatocr.git
``` 

- Create a virtual environment (recommended):

    This isolates project dependencies and avoids conflicts with system-wide packages. Use venv or virtualenv (if venv is not available):

``` 
    python3 -m venv openbharatocr_env  # Using venv
    # OR
    virtualenv openbharatocr_env      # Using virtualenv
``` 

- Activate the virtual environment:

```
source openbharatocr_env/bin/activate  # For venv
# OR
source openbharatocr_env/bin/activate  # For virtualenv
``` 


- Install dependencies:
Navigate to the cloned repository directory and install required packages using pip:
```
    cd openbharatocr
    pip install -r requirements.txt
   ``` 

#### Installation


```
    pip install openbharatocr
```


**Pan Card**

This function takes the path of a PAN card image as input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.pan(image_path)
```


**Aadhaar Card**

The two functions accepts the file paths of the front and back images of an Aadhaar card as input and returns their corresponding information encapsulated in a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.front_aadhaar(image_path)
    dict_output = openbharatocr.back_aadhaar(image_path)
```

**Driving Licence**

This function takes the path of a Driving Licence card image as input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.driving_licence(image_path)
```

**Passport**

This function takes the path of a Passport image as input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.passport(image_path)
```

**VoterID**

The two functions accepts the file paths of the front and back images of a voterID as input and returns their corresponding information encapsulated in a dictionary.

```
    import openbharatocr 
    # Download YOLOv3 models from links(added below) and set local downloaded path to YOLO_CFG, YOLO_WEIGHT env variables
    dict_output = openbharatocr.voter_id_front(image_path)
    dict_output = openbharatocr.voter_id_back(image_path)
```


### Download Resources
Some resources need to be downloaded and set the path in the variables.
- YOLO_CFG = https://drive.google.com/file/d/1SEst2lVoFDOgUVLZ5kje9GTb2tHRA8U-/view?usp=sharing
- YOLO_WEIGHT = https://drive.google.com/file/d/1cGGstycfogmO6O7ToB2DAEXOgTWVgINh/view?usp=drive_link


**Vehicle Registration Card/Certificate**

This function takes the path of a Vehicle Registration Card/Certificate image as an input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.vehicle_registration(image_path)
```


**Water Bill**

This function takes the path of a Water Bill image as an input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.water_bill(image_path)
```

**Birth Certificate**

This function takes the path of a Birth Certificate image as an input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.birth_certificate(image_path)
```


**Degree**

This function takes the path of a Degree image as an input and returns its information in the form of a dictionary.

```
    import openbharatocr 
    dict_output = openbharatocr.degree(image_path)
```

### Contribute & support
We are so pleased to your help and help you. If you wanna develop openbharatocr, Congrats! If you have problem, don't worry, create an issue here:

```
    https://github.com/essentiasoftserv/openbharatocr/issues
```

### Pre Commit
Note: Before committing your changes, run pre-commits 

```
    pre-commit run --all
```

