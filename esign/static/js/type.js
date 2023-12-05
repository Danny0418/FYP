document.addEventListener("DOMContentLoaded", function () {
    const nameInput = document.getElementById("nameInput");
    const fontSelect = document.getElementById("fontSelect");
    const generateButton = document.getElementById("generateButton");
    const generatedSignature = document.getElementById("generatedSignature");
    const downloadButton = document.querySelector('[data-action="save-jpg"]');
    const changeColorButton = document.querySelector('[data-action="change-color"]'); 
    const clearButton = document.querySelector('[data-action="clear"]');    

    generateButton.addEventListener("click", function () {
        const name = nameInput.value;
        const selectedFont = fontSelect.value;

        generatedSignature.style.fontFamily = selectedFont;
        generatedSignature.textContent = name;

        downloadButton.style.display = "block";
    });

    changeColorButton.addEventListener("click", function () {
        // Generate random color
        const randomColor = getRandomColor();
        
        // Set the color to the signature
        generatedSignature.style.color = randomColor;
    });
    
    // Function to generate random color
    function getRandomColor() {
        const letters = "0123456789ABCDEF";
        let color = "#";
        
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        
        return color;
    }
    
    clearButton.addEventListener("click", function () {
        generatedSignature.textContent = ""; // Clear the signature
    });

    downloadButton.addEventListener("click", function () {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        
        // Set the canvas width and height to the generated signature's
        canvas.width = generatedSignature.offsetWidth;
        canvas.height = generatedSignature.offsetHeight + 40;
        context.fillStyle = "white"; // Set the background color
        context.fillRect(0, 0, canvas.width, canvas.height);
        
        context.font = window.getComputedStyle(generatedSignature).font;
        context.fillStyle = window.getComputedStyle(generatedSignature).color;
        context.fillText(nameInput.value, 10, 40);
        
        // Get the canvas data URL
        const dataURL = canvas.toDataURL("image/jpeg");
        
        // Download the image
        const downloadLink = document.createElement("a");
        downloadLink.href = dataURL;
        downloadLink.download = "signature.jpg";
        downloadLink.click();

        window.location.href = "/esign/face_detection/";
    });
});
