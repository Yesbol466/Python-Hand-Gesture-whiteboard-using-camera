document.addEventListener('DOMContentLoaded', (event) => {
    const videoElement = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    // Set canvas size
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    // Get access to the webcam
    if (navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                videoElement.srcObject = stream;
            })
            .catch(function(error) {
                console.log("Something went wrong!");
            });
    }

    let drawing = false;

    const startDrawing = (e) => {
        drawing = true;
        draw(e);
    };

    const endDrawing = () => {
        drawing = false;
        ctx.beginPath(); // Begin a new path (to not connect the dots)
    };

    const draw = (e) => {
        if (!drawing) return;
        ctx.lineWidth = 5;
        ctx.lineCap = 'round';
        ctx.strokeStyle = 'yellow'; // Line color

        ctx.lineTo(e.clientX, e.clientY);
        ctx.stroke();
        ctx.beginPath();
        ctx.moveTo(e.clientX, e.clientY);
    };

    // Mouse events
    canvas.addEventListener('mousedown', startDrawing);
    canvas.addEventListener('mouseup', endDrawing);
    canvas.addEventListener('mousemove', draw);

    // Optional: Handle touch events for mobile browsers
    canvas.addEventListener('touchstart', (e) => startDrawing(e.touches[0]));
    canvas.addEventListener('touchend', endDrawing);
    canvas.addEventListener('touchmove', (e) => draw(e.touches[0]));
});
