from flask import Flask, render_template, request
from base64 import b64encode
from api import get_tag, get_barcode

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['SECRET_KEY'] = 'ie7yyyeyehysyheir'

#function to check if the uploaded image is valid or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

#main route (Home Page)
@app.route('/')
def main():
    if request.method=='GET':
        return render_template('index.html')

#route for image classifier
@app.route('/image-classifier')
def image_classifier():
    return render_template('image.html')

#result route for image classifier        
@app.route('/image-classifier-result', methods=['POST'])
def result():
    #getting the image
    uploaded_image = request.files['image']
    
    #checking for allowed_file
    if allowed_file(uploaded_image.filename):
        #calling the api function
        result = get_tag(uploaded_image)
        
        if type(result) != str:
            #extracting and parsing tags
            tag = result['tag']
            ftags = []
            
            for tags in tag:
                ftags.append({tags['tag']['en']:str(int(tags['confidence']))})
            uploaded_image.seek(0)
            image_string = b64encode(uploaded_image.read())
            image_string = image_string.decode('utf-8')
        
            return render_template('image-result.html', tag=ftags, image=image_string)
            
        else:
            result = result
            button ='''<button class="project-button">
        <a class="project-button-link" href="/image-classifier">Go to Image Classifier</a></button>'''
        
            error = result+button
            return render_template('error.html', error=error)
            
        
    else: 
        error = '''<H1>Something Went Wrong!  Either an image is not uploaded or an unsupported format has been uploaded.  Please try again</H1>
            <button class="project-button">
        <a class="project-button-link" href="/image-classifier">Go to Image Classifier</a></button>
        '''
        
        return render_template('error.html', error=error)

#route for barcode reader
@app.route('/barcode-reader')
def barcode_reader():
    return render_template('barcode.html')

#route for barcode reader result    
@app.route('/barcode-result', methods=['POST'])
def barcode_result():
    #getting the image
    image = request.files['image']
    
    #checking for allowed_file
    if allowed_file(image.filename):
        
        #calling the api function to analyse the barcode
        result = get_barcode(image)
        
        if type(result)==str:
            result = result
            button ='''<button class="project-button">
    <a class="project-button-link" href="/barcode-reader">Go to Barcode Reader</a></button>'''
            error = result + button
            return render_template('error.html', error=error)
        
        image.seek(0)
        image_string = b64encode(image.read())
          
        image_string = image_string.decode('utf-8')
            
        #extracting and examining the data
        barcodes = []
    
        
        for barcode in result:
            barcodes.append({'data':str(barcode['data']), 'type':str(barcode['type'])})
        
        return render_template('barcode-result.html', barcode=barcodes, image=image_string)
            
    else: 
        error = '''<H1>Something Went Wrong! Either an image is not uploaded or an unsupported format has been uploaded.
            Please try again</H1>
            <button class="project-button">
        <a class="project-button-link" href="/barcode-reader">Go to Barcode Reader</a></button>
        '''
        
        return render_template('error.html', error=error)
    


if __name__=="__main__":
    app.run(debug=True, host='0.0.0.0')
    
