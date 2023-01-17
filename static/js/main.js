// find the output element
const output = document.getElementById("output");

// initialize codemirror and pass configuration to support Python and the dracula theme
const editor = CodeMirror.fromTextArea(
  document.getElementById("code"), {
    mode: {
      name: "python",
      version: 3,
      singleLineStringErrors: false,
    },
    theme: "dracula",
    lineNumbers: true,
    indentUnit: 4,
    matchBrackets: true,
  }
);