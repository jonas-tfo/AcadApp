// elements in first box
const dropArea1 = document.getElementById('drop-area1');
const fileElem1 = document.getElementById('file-elem1');
const fileList1 = document.getElementById('file-list1');
// elements in second box
const dropArea2 = document.getElementById('drop-area2');
const fileElem2 = document.getElementById('file-elem2');
const fileList2 = document.getElementById('file-list2');

const startUploadBtn = document.getElementById('start-upload');  // The upload button

let selectedFiles1 = [];  // To store files from drag-and-drop or file selection for area 1
let selectedFiles2 = [];  // To store files from drag-and-drop or file selection for area 2

// Prevent default behaviors for drag-and-drop events
function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

// Handle drag-and-drop events for both drop areas
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  dropArea1.addEventListener(eventName, preventDefaults, false);
  dropArea2.addEventListener(eventName, preventDefaults, false);
});

// Handle highlighting of drop areas when dragging files
['dragenter', 'dragover'].forEach(eventName => {
  dropArea1.addEventListener(eventName, () => dropArea1.classList.add('highlight'), false);
  dropArea2.addEventListener(eventName, () => dropArea2.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
  dropArea1.addEventListener(eventName, () => dropArea1.classList.remove('highlight'), false);
  dropArea2.addEventListener(eventName, () => dropArea2.classList.remove('highlight'), false);
});

// Handle file drop for first drop area
dropArea1.addEventListener('drop', handleDrop1, false);
function handleDrop1(e) {
  let dt = e.dataTransfer;
  let files = dt.files;
  handleFiles1(files);
}

function handleFiles1(files) {
  selectedFiles1 = [...files];  // Store the files in the array for later upload
  previewFiles1(selectedFiles1);  // Display file preview
}

function previewFiles1(files) {
  fileList1.innerHTML = '';  // Clear previous file list
  files.forEach(file => {
    let div = document.createElement('div');
    div.textContent = `File: ${file.name}`;
    fileList1.appendChild(div);
  });
}

// Handle manual file selection for first file area
fileElem1.addEventListener('change', (e) => {
  handleFiles1(fileElem1.files);
});

// Handle file drop for second drop area
dropArea2.addEventListener('drop', handleDrop2, false);
function handleDrop2(e) {
  let dt = e.dataTransfer;
  let files = dt.files;
  handleFiles2(files);
}

function handleFiles2(files) {
  selectedFiles2 = [...files];  // Store the files in the array for later upload
  previewFiles2(selectedFiles2);  // Display file preview
}

function previewFiles2(files) {
  fileList2.innerHTML = '';  // Clear previous file list
  files.forEach(file => {
    let div = document.createElement('div');
    div.textContent = `File: ${file.name}`;
    fileList2.appendChild(div);
  });
}

// Handle manual file selection for second file area
fileElem2.addEventListener('change', (e) => {
  handleFiles2(fileElem2.files);
});

// Event listener for the "start-upload" button
startUploadBtn.addEventListener('click', () => {
  if (selectedFiles1.length > 0 && selectedFiles2.length > 0) {
    uploadFiles(selectedFiles1[0], selectedFiles2[0]);  // Upload the first file from each area
  } else {
    console.error('Two files must be selected for upload');
  }
});

// Upload both files using FormData
function uploadFiles(file1, file2) {
  let url = '/doccompare';  // Your server endpoint
  let formData = new FormData();
  formData.append('file1', file1);
  formData.append('file2', file2);

  fetch(url, {
    method: 'POST',
    body: formData
  })
  .then(response => {
    if (response.ok) {
      return response.text();  // Ensure HTML is returned
    } else {
      console.error('Failed to upload files');
    }
  })
  .then(htmlContent => {
    document.body.innerHTML = htmlContent;  // Dynamically update the page
  })
  .catch(error => {
    console.error('Error uploading files', error);
  });
}