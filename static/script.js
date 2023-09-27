function exportToTxt() {
  const textareaContent = document.getElementById('textareaContent').value;

  const blob = new Blob([textareaContent], { type: 'text/plain' });
  const anchor = document.createElement('a');
  anchor.download = 'exported.txt';
  anchor.href = window.URL.createObjectURL(blob);
  anchor.target = '_blank';
  anchor.click();
}