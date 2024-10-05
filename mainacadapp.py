
from flask import Flask
from flask import render_template
from flask import request, url_for, send_file, send_from_directory, redirect
from werkzeug.utils import secure_filename
import os
from funcsacadapp import annotation_report_master_function, document_comparison_master_function, convert_docx_to_pdf, convert_single_pdf_to_docx
import pypdf

"""

TODO :

- RECHECK THE REPORT MAKING FUNC FOR POTENTIAL FLAW (DISPLAYES TOO MANY PAGES)
- make error messages look nicer, appear on same page
- maybe change send_file to send_from_directory
    - fix the drag and drop
- maybe add sidebar menu on left side for guides and privacy policy and homebuttons to pages -> and some icons
- change the download hyperlinks to a nicer button
- add credits for icons
- make doccompare look nicer


- FIX COMMENTS BEING DELETING IN DOC COMPARE

- for future: add a dark mode, download button for app, guides, excel report generator (graph), text summary


"""




basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)




app.config.update(ANNOT_UPLOAD_FOLDER = os.path.join(basedir, "annotation_uploads"),
                  COMPARE_UPLOAD_FOLDER = os.path.join(basedir, "comparison_uploads"),
                  TOPDF_UPLOAD_FOLDER = os.path.join(basedir, "converttopdf_uploads"),
                  TOWORD_UPLOAD_FOLDER = os.path.join(basedir, "converttoword_uploads"),
                  APP_DOWNLOAD_FOLER = os.path.join(basedir, "app_download"))

# 50mb limit
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024


### for app icon
@app.route('/favicon.ico')
def favicon():
    return url_for('static', filename='/favicon.ico')


### ANNOTAION REPORT 

@app.route('/annotdownloads/<filename>', methods=['GET', 'POST'])       
def annotation_download_files(filename):

        
    file_path = os.path.join(app.config['ANNOT_UPLOAD_FOLDER'], filename)   

    return send_file(file_path, as_attachment=True)         


@app.route("/annotationreport/", methods=['POST', 'GET'])
def annotation_report_page():

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Please select a file first', 400
        
        file = request.files['file']

        if file.filename == '':
            return 'Please select a file with a valid name', 400
        

        # Save the uploaded file to a secure location
        filename_secure_file = secure_filename(file.filename)
        path_to_secure_file = os.path.join(app.config['ANNOT_UPLOAD_FOLDER'], filename_secure_file)
        file.save(path_to_secure_file)

        # Generate the report and get the path to the generated file
        wordDocpath = annotation_report_master_function(path_to_secure_file, os.path.abspath(os.path.dirname(__file__)))

        # this exception is for when a wrong filetype is entered, it is caught here
        try:
            # Extract the file name to be used for downloading
            docname = os.path.basename(wordDocpath)
        except TypeError:
            return 'The selected file contains no comments/annotations', 400

        # Generate the URL for the download link
        download_url = url_for('annotation_download_files', filename=docname)

        # Render the template with the generated download URL
        return render_template("annotationreporttemplate.html", docname=download_url, 
                                                                var_homepage = url_for('homepage'),
                                                                var_annotation_report = url_for("annotation_report_page"), 
                                                                var_document_comparison = url_for("doc_comparison_page"),
                                                                var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                                var_convert_to_word = url_for('convert_to_word_page'))
    

    # If the request method is GET, just render the template without docname
    return render_template("annotationreporttemplate.html", var_homepage = url_for('homepage'),
                                                            var_annotation_report = url_for("annotation_report_page"), 
                                                            var_document_comparison = url_for("doc_comparison_page"),
                                                            var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                            var_convert_to_word = url_for('convert_to_word_page'))

    

#-------------------------------------------------------------------------------------

### DOCUMENT COMPARISON


@app.route('/comparedownloads/<filename>', methods=['GET', 'POST'])
def comparison_download_files(filename):
    # Construct the full path to the file to be sent
    file_path = os.path.join(app.config['COMPARE_UPLOAD_FOLDER'], filename)
    
    return send_file(file_path, as_attachment=True)


@app.route("/doccompare/", methods=['POST', 'GET'])
def doc_comparison_page():

    if request.method == 'POST':
        if 'file1' not in request.files or 'file2' not in request.files:
            return 'Please select two files first', 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']

        if file1.filename == '' or file2.filename == '':
            return 'Please select a file with a valid name', 400
        

        # Save the uploaded file to a secure location
        filename_secure_file1 = secure_filename(file1.filename)
        path_to_secure_file1 = os.path.join(app.config['COMPARE_UPLOAD_FOLDER'], filename_secure_file1)
        file1.save(path_to_secure_file1)

        filename_secure_file2 = secure_filename(file2.filename)
        path_to_secure_file2 = os.path.join(app.config['COMPARE_UPLOAD_FOLDER'], filename_secure_file2)
        file2.save(path_to_secure_file2)
        
        # Generate the report and get the path to the generated file
        wordDocpath = document_comparison_master_function(app.config['COMPARE_UPLOAD_FOLDER'], path_to_secure_file1, path_to_secure_file2)

        # this exception is for when a wrong filetype is entered, it is caught here
        try:
            # Extract the file name to be used for downloading
            docname = os.path.basename(wordDocpath)
        except TypeError:
            return 'Please select a valid filetype, either a PDF (.pdf) or a Word document (.docx)', 400

        

        # Generate the URL for the download link
        download_url = url_for('comparison_download_files', filename=docname, var_homepage = url_for('homepage'),
                                                                var_annotation_report = url_for("annotation_report_page"), 
                                                                var_document_comparison = url_for("doc_comparison_page"),
                                                                var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                                var_convert_to_word = url_for('convert_to_word_page'))

    
        # Render the template with the generated download URL
        # thisis just not registering at all
        return render_template("doccomparisontemplate.html", docname=download_url, var_homepage = url_for('homepage'),
                                                                var_annotation_report = url_for("annotation_report_page"), 
                                                                var_document_comparison = url_for("doc_comparison_page"),
                                                                var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                                var_convert_to_word = url_for('convert_to_word_page'))


    # If the request method is GET, just render the template without docname
    return render_template("doccomparisontemplate.html", var_homepage = url_for('homepage'),
                                                         var_annotation_report = url_for("annotation_report_page"), 
                                                         var_document_comparison = url_for("doc_comparison_page"),
                                                         var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                         var_convert_to_word = url_for('convert_to_word_page'))



#------------------------------------------------------------------------------------

### FILE CONVERTION

@app.route('/converttopdfdownloads/<filename>', methods=['GET', 'POST'])
def converttopdf_download_files(filename):
    # Construct the full path to the file to be sent
    file_path = os.path.join(app.config['TOPDF_UPLOAD_FOLDER'], filename)
    
    return send_file(file_path, as_attachment=True)



@app.route("/converttopdf/", methods=['POST', 'GET'])
def convert_to_pdf_page():

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Please select a file first', 400
        
        file = request.files['file']

        if file.filename == '':
            return 'Please select a file with a valid name', 400
            
        filename_secure_file = secure_filename(file.filename)
        path_to_secure_file = os.path.join(app.config['TOPDF_UPLOAD_FOLDER'], filename_secure_file)
        file.save(path_to_secure_file)

        pdfPath = convert_docx_to_pdf(path_to_secure_file)

        try:
            # Extract the file name to be used for downloading
            docname = os.path.basename(pdfPath)
        except TypeError:
            return 'Please select a valid filetype, either a PDF (.pdf) or a Word document (.docx)', 400

            # Generate the URL for the download link
        download_url = url_for('converttopdf_download_files', filename=docname)

        print(download_url)

        return render_template("converttopdftemplate.html", docname=download_url, var_homepage = url_for('homepage'),
                                                                var_annotation_report = url_for("annotation_report_page"), 
                                                                var_document_comparison = url_for("doc_comparison_page"),
                                                                var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                                var_convert_to_word = url_for('convert_to_word_page'))


    return render_template("converttopdftemplate.html", var_homepage = url_for('homepage'),
                                                        var_annotation_report = url_for("annotation_report_page"), 
                                                        var_document_comparison = url_for("doc_comparison_page"),
                                                        var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                        var_convert_to_word = url_for('convert_to_word_page'))




@app.route('/converttoworddownloads/<filename>', methods=['GET', 'POST'])
def converttoword_download_files(filename):
    # Construct the full path to the file to be sent
    file_path = os.path.join(app.config['TOWORD_UPLOAD_FOLDER'], filename)
    
    return send_file(file_path, as_attachment=True)



@app.route("/converttoword/", methods=['POST', 'GET'])
def convert_to_word_page():

    if request.method == 'POST':
        if 'file' not in request.files:
            return 'Please select a file first', 400
        
        file = request.files['file']

        if file.filename == '':
            return 'Please select a file with a valid name', 400
            
        filename_secure_file = secure_filename(file.filename)
        path_to_secure_file = os.path.join(app.config['TOWORD_UPLOAD_FOLDER'], filename_secure_file)
        file.save(path_to_secure_file)

        wordPath = convert_single_pdf_to_docx(path_to_secure_file)

        try:
            # Extract the file name to be used for downloading
            docname = os.path.basename(wordPath)
        except TypeError:
            return 'Please select a PDF (.pdf)', 400

            # Generate the URL for the download link
        download_url = url_for('converttoword_download_files', filename=docname)


        return render_template("converttodocxtemplate.html", docname=download_url, var_homepage = url_for('homepage'),
                                                                var_annotation_report = url_for("annotation_report_page"), 
                                                                var_document_comparison = url_for("doc_comparison_page"),
                                                                var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                                var_convert_to_word = url_for('convert_to_word_page'))


    return render_template("converttodocxtemplate.html", var_homepage = url_for('homepage'),
                                                         var_annotation_report = url_for("annotation_report_page"), 
                                                         var_document_comparison = url_for("doc_comparison_page"),
                                                         var_convert_to_pdf = url_for('convert_to_pdf_page'),
                                                         var_convert_to_word = url_for('convert_to_word_page'))


### HOMEPAGE

@app.route("/", methods=['POST', 'GET'])
@app.route("/home/")
def homepage():
    return render_template("homepagetemplate.html", 
                           var_annotation_report = url_for("annotation_report_page"), 
                           var_document_comparison = url_for("doc_comparison_page"),
                           var_convert_to_pdf = url_for('convert_to_pdf_page'),
                           var_convert_to_word = url_for('convert_to_word_page'))



### MENU ITEMS

@app.route("/about/")
def about():
    return render_template("abouttemplate.html", var_homepage=url_for('homepage'))

@app.route("/privacypolicy/")
def privacy():
    return render_template("privacytemplate.html", var_homepage=url_for('homepage'))


@app.route("/acknowledgements/")
def acknowledgements():
    return render_template("acknowledgementstemplate.html", var_homepage=url_for('homepage'))

@app.route("/support/")
def support():
    return render_template("supporttemplate.html", var_homepage=url_for('homepage'))


### ERROR HANDLING


@app.errorhandler(413)
def error413(e):
    return "A file is too large, please try again with a smaller file", 413


@app.errorhandler(pypdf.errors.PdfReadError)
def handle_corrupted(e):
 
    return 'File cannot be read and is potentially corrupted '

# maybe make this give feedback to me
@app.errorhandler(500)
def error413(e):
    return "An internal error has occured", 500



### APP 


@app.route('/downloadapp/', methods=['GET', 'POST'])       
def download_app():

    path = 'AcadApp.zip'
    return send_file(path, as_attachment=True)



# Route with button to initiate download
@app.route("/appdownloadpage/", methods=['POST', 'GET'])
def app_download_page():

    if request.method == 'POST':

        download_url = url_for('download_app')

        return render_template("apptemplate.html", var_homepage=url_for('homepage'),
                                                   var_downloadapp=download_url)
    
    download_url = url_for('download_app')

    return render_template("apptemplate.html", var_homepage=url_for('homepage'),
                                                var_downloadapp=download_url)


                                        
    

               




"""
upload_folders = [app.config["ANNOT_UPLOAD_FOLDER"], app.config["COMPARE_UPLOAD_FOLDER"], app.config["TOPDF_UPLOAD_FOLDER"], app.config["TOWORD_UPLOAD_FOLDER"]]

def file_age_in_seconds(pathname):
    return time.time() - os.stat(pathname)[stat.ST_MTIME]
"""




if __name__ == "__main__":
    app.run(port=8000, debug=False, host="0.0.0.0")




 