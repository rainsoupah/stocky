# Stocky

### Initial Setup

    cd stocky   # you should be in the root directory of the repo
    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt
    
    cd app/static
    bower install
    cd ../..
    
    
### Run
    . env/bin/activate      # if environment is not started
    python __init__.py      
