Import data
Split data into training and testing set
Train model on training set
Evaluate model on testing set


Hide data from cuttle:
```py
#cuttle-environment-disable sailor-api
```

API Route config:
```py
#cuttle-environment-set-config sailor-api route=/api/predict method=POST
# (Flask Transformer)

file = open("./images/mnist3.png", "rb") #cuttle-environment-get-config sailor-apiu request.files['files']

# Return variable as api response
c = str(digit) # cuttle-environment-set-config sailor-api response
```

Transform notebook:
```bash
cuttle transform sailor-api
```
Note: make sure to comment out `%matplotlib inline` / `matplotlib notebook`

# Flask configuration
Users will import TIC data into flask using the POST method
This will then be processed by the notebook function and passed into the other blueprints inside Flask