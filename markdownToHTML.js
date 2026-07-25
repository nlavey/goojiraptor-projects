const markdownInput = document.getElementById("markdown-input");
const htmlOutput = document.getElementById("html-output");
const preview = document.getElementById("preview");

function convertMarkdown() {
  let html = markdownInput.value;
  html = html.replace(/^# (.*?)$/gim, '<h1>$1</h1>');
  html = html.replace(/^## (.*?)$/gim, '<h2>$1</h2>');
  html = html.replace(/^### (.*?)$/gim, '<h3>$1</h3>');
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  html = html.replace(/__(.*?)__/g, '<strong>$1</strong>');
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  html = html.replace(/_(.*?)_/g, '<em>$1</em>');
  html = html.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" />');
  html = html.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');
  html = html.replace(/^\s*>\s+(.+)$/gm, '<blockquote>$1</blockquote>');
  return html;
}

function updateOutput() {
  const html = convertMarkdown();
  htmlOutput.textContent = html;
  preview.innerHTML = html
}

markdownInput.addEventListener("input", updateOutput);
