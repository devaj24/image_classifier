import requests
import os

api_key = os.environ.get('APIKEY')
api_secret = os.environ.get('APISECRET')

def get_tag(img):
    try:
        #upload the image to server
        upload = requests.post('https://api.imagga.com/v2/uploads',
        auth=(api_key, api_secret), files={'image':img})
    
        upload_id =upload.json()['result']['upload_id']
    
        #get the tag at /tag
        t = requests.get(f'https://api.imagga.com/v2/tags?image_upload_id={upload_id}',auth=(api_key, api_secret))
        tag = t.json()['result']['tags'][:9]
    
    
        return {'tag':tag}
        
    except:
        return 'something went wrong.Please try again'
       

def get_barcode(img):
    try:
        #upload the image to server
        upload = requests.post('https://api.imagga.com/v2/uploads',
        auth=(api_key, api_secret), files={'image':img})
    
        upload_id =upload.json()['result']['upload_id']
        response = requests.get(f'https://api.imagga.com/v2/barcodes?image_upload_id={upload_id}',auth=(api_key, api_secret))
        
        if response.json()['result']['barcodes']==[]:
            return "No Barcode Detected"
            
        else:
            return response.json()['result']['barcodes']
        
    except:
        return '''Something Went Wrong. Please Try Again.'''