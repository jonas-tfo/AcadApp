  const dropArea = document.getElementById('drop-area');
  const fileElem = document.getElementById('fileElem');
  const fileList = document.getElementById('file-list');
  const startUploadBtn = document.getElementById('start-upload');  // The upload button
  let selectedFiles = [];  // To store files from drag-and-drop or file selection

  // Prevent default behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  // Highlight the drop area on drag over
  ['dragenter', 'dragover'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.add('highlight'), false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropArea.addEventListener(eventName, () => dropArea.classList.remove('highlight'), false);
  });

  // Handle files dropped or selected
  dropArea.addEventListener('drop', handleDrop, false);

  // Event listener for the "start-upload" button
  startUploadBtn.addEventListener('click', () => {
    if (selectedFiles.length > 0) {
      selectedFiles.forEach(uploadFile);
    } else {
      console.error('No files selected for upload');
    }
  });

  function handleDrop(e) {
    let dt = e.dataTransfer;
    let files = dt.files;
    handleFiles(files);
  }

  function handleFiles(files) {
    selectedFiles = [...files];  // Store the files in the array for later upload
    previewFiles(selectedFiles);  // Display file preview
  }

  function previewFiles(files) {
    fileList.innerHTML = '';  // Clear previous file list
    files.forEach(file => {
      let div = document.createElement('div');
      div.textContent = `File: ${file.name}`;
      fileList.appendChild(div);
    });
  }

  function uploadFile(file) {
    let url = '/annotationreport';
    let formData = new FormData();
    formData.append('file', file);

    fetch(url, {
      method: 'POST',
      body: formData
    })
    .then(response => {
      if (response.ok) {
        return response.text();  // Ensure HTML is returned
      } else {
        console.error(`Failed to upload file: ${file.name}`);
      }
    })
    .then(htmlContent => {
      document.body.innerHTML = htmlContent;  // Dynamically update the page
    })
    .catch(error => {
      console.error(`Error uploading file: ${file.name}`, error);
    });
  }

  // Handle manual file selection through the file input
  fileElem.addEventListener('change', (e) => {
    handleFiles(fileElem.files);
  });

 