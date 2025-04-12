document.addEventListener("DOMContentLoaded", function() {
    const imageContainer = document.querySelector(".image-container");
    const canvas = document.querySelector(".sparks-canvas");
    const ctx = canvas.getContext("2d");

    let particles = [];
    let mouseX = 0;
    let mouseY = 0;

    // Настройки частиц
    const particleCount = 20;
    const particleSpeed = 5;

    function resizeCanvas() {
        canvas.width = imageContainer.clientWidth;
        canvas.height = imageContainer.clientHeight;
    }

    resizeCanvas();

    window.addEventListener("resize", resizeCanvas);

    imageContainer.addEventListener("mousemove", function(e) {
        const rect = imageContainer.getBoundingClientRect();
        mouseX = e.clientX - rect.left;
        mouseY = e.clientY - rect.top;

        for (let i = 0; i < particleCount; i++) {
            particles.push({
                x: mouseX,
                y: mouseY,
                size: Math.random() * 5 + 1,
                speedX: Math.random() * particleSpeed - particleSpeed / 2,
                speedY: Math.random() * particleSpeed - particleSpeed / 2,
                opacity: 1,
                shrinkRate: Math.random() * 0.05 + 0.02
            });
        }
    });

    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        for (let i = 0; i < particles.length; i++) {
            const p = particles[i];
            p.x += p.speedX;
            p.y += p.speedY;
            p.size *= (1 - p.shrinkRate);
            p.opacity -= p.shrinkRate;

            if (p.opacity > 0) {
                ctx.beginPath();
                ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
                ctx.fillStyle = `rgba(255, 255, 0, ${p.opacity})`; // Цвет искр (желтые)
                ctx.fill();
            } else {
                particles.splice(i, 1);
                i--;
            }
        }
    }

    function animate() {
        drawParticles();
        requestAnimationFrame(animate);
    }

    animate();
});
