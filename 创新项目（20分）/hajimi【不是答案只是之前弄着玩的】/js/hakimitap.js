// Hakimitap - 基于Mikutap风格的哈基米互动音乐网站
// 基于Canvas实现，简化版本，不依赖外部库

document.addEventListener('DOMContentLoaded', function() {
    // 主要DOM元素
    const view = document.getElementById('view');
    const sceneTop = document.getElementById('scene_top');
    const sceneLoading = document.getElementById('scene_loading');
    const sceneMain = document.getElementById('scene_main');
    const about = document.getElementById('about');
    const aboutCover = document.getElementById('about_cover');
    const btStart = document.getElementById('bt_start');
    const btAbout = document.getElementById('bt_about');
    const btClose = document.getElementById('bt_close');
    const btBack = document.getElementById('bt_back');
    const btFs = document.getElementById('bt_fs');
    const btFeedback = document.getElementById('bt_feedback');
    const btBacktrack = document.getElementById('bt_backtrack');

    // 音频相关变量
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    const audioContext = new AudioContext();
    let audioBuffers = {};
    let feedbackEnabled = true;
    let backtrackEnabled = true;

    // Canvas相关变量
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    let particles = [];
    let shapes = [];
    let animationId = null;

    // 初始化Canvas尺寸
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // 粒子类
    class Particle {
        constructor(x, y, color, type) {
            this.x = x;
            this.y = y;
            this.color = color;
            this.type = type;
            this.size = Math.random() * 15 + 5;
            this.speedX = (Math.random() - 0.5) * 10;
            this.speedY = (Math.random() - 0.5) * 10;
            this.life = 1;
            this.decay = Math.random() * 0.02 + 0.01;
            this.rotation = Math.random() * Math.PI * 2;
            this.rotationSpeed = (Math.random() - 0.5) * 0.2;
        }

        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            this.speedY += 0.2; // 重力
            this.life -= this.decay;
            this.size *= 0.98;
            this.rotation += this.rotationSpeed;
        }

        draw() {
            ctx.save();
            ctx.globalAlpha = this.life;
            ctx.fillStyle = this.color;
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation);

            // 根据类型绘制不同形状
            if (this.type === 0) { // 圆形
                ctx.beginPath();
                ctx.arc(0, 0, this.size, 0, Math.PI * 2);
                ctx.fill();
            } else if (this.type === 1) { // 方形
                ctx.fillRect(-this.size/2, -this.size/2, this.size, this.size);
            } else if (this.type === 2) { // 三角形
                ctx.beginPath();
                ctx.moveTo(0, -this.size);
                ctx.lineTo(-this.size, this.size);
                ctx.lineTo(this.size, this.size);
                ctx.closePath();
                ctx.fill();
            }

            ctx.restore();
        }
    }

    // 形状类
    class Shape {
        constructor(x, y, color, type) {
            this.x = x;
            this.y = y;
            this.color = color;
            this.type = type;
            this.size = 0;
            this.maxSize = Math.random() * 100 + 50;
            this.growth = Math.random() * 5 + 2;
            this.life = 1;
            this.decay = 0.01;
            this.rotation = 0;
            this.rotationSpeed = (Math.random() - 0.5) * 0.1;
        }

        update() {
            if (this.size < this.maxSize) {
                this.size += this.growth;
            } else {
                this.life -= this.decay;
            }
            this.rotation += this.rotationSpeed;
        }

        draw() {
            ctx.save();
            ctx.globalAlpha = this.life;
            ctx.strokeStyle = this.color;
            ctx.lineWidth = 2;
            ctx.translate(this.x, this.y);
            ctx.rotate(this.rotation);

            // 根据类型绘制不同形状
            if (this.type === 0) { // 圆形
                ctx.beginPath();
                ctx.arc(0, 0, this.size, 0, Math.PI * 2);
                ctx.stroke();
            } else if (this.type === 1) { // 方形
                ctx.strokeRect(-this.size/2, -this.size/2, this.size, this.size);
            } else if (this.type === 2) { // 星形
                const spikes = 5;
                const outerRadius = this.size;
                const innerRadius = this.size * 0.5;

                ctx.beginPath();
                for (let i = 0; i < spikes * 2; i++) {
                    const radius = i % 2 === 0 ? outerRadius : innerRadius;
                    const angle = (i * Math.PI) / spikes;
                    const x = Math.cos(angle) * radius;
                    const y = Math.sin(angle) * radius;

                    if (i === 0) {
                        ctx.moveTo(x, y);
                    } else {
                        ctx.lineTo(x, y);
                    }
                }
                ctx.closePath();
                ctx.stroke();
            }

            ctx.restore();
        }
    }

    // 创建粒子爆炸效果
    function createParticles(x, y, color, count = 10) {
        for (let i = 0; i < count; i++) {
            const type = Math.floor(Math.random() * 3);
            particles.push(new Particle(x, y, color, type));
        }
    }

    // 创建形状
    function createShape(x, y, color) {
        const type = Math.floor(Math.random() * 3);
        shapes.push(new Shape(x, y, color, type));
    }

    // 动画循环
    function animate() {
        // 半透明覆盖，创建拖尾效果
        ctx.fillStyle = 'rgba(255, 158, 199, 0.1)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 更新和绘制形状
        for (let i = shapes.length - 1; i >= 0; i--) {
            const shape = shapes[i];
            shape.update();
            shape.draw();

            if (shape.life <= 0) {
                shapes.splice(i, 1);
            }
        }

        // 更新和绘制粒子
        for (let i = particles.length - 1; i >= 0; i--) {
            const particle = particles[i];
            particle.update();
            particle.draw();

            if (particle.life <= 0 || particle.y > canvas.height) {
                particles.splice(i, 1);
            }
        }

        animationId = requestAnimationFrame(animate);
    }

    // 播放声音
    function playSound(index) {
        if (audioContext.state === 'suspended') {
            audioContext.resume();
        }

        // 这里应该加载并播放哈基米音效
        // 由于没有实际音频文件，我们使用Web Audio API创建简单的声音
        const oscillator = audioContext.createOscillator();
        const gainNode = audioContext.createGain();

        oscillator.connect(gainNode);
        gainNode.connect(audioContext.destination);

        // 根据索引设置不同的音调
        const frequencies = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25];
        oscillator.frequency.value = frequencies[index % frequencies.length];

        // 设置音量包络
        gainNode.gain.setValueAtTime(0.3, audioContext.currentTime);
        gainNode.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.5);

        oscillator.start(audioContext.currentTime);
        oscillator.stop(audioContext.currentTime + 0.5);
    }

    // 处理点击/触摸事件
    function handleInteraction(x, y) {
        // 根据位置决定颜色
        const colors = ['#FF6B9D', '#C66FBC', '#7F7FD5', '#91EAE4', '#86A8E7'];
        const color = colors[Math.floor(Math.random() * colors.length)];

        // 创建形状和粒子
        createShape(x, y, color);
        createParticles(x, y, color, 20);

        // 播放声音
        const soundIndex = Math.floor(Math.random() * 8);
        playSound(soundIndex);

        // 如果启用了反馈，添加振动
        if (feedbackEnabled && navigator.vibrate) {
            navigator.vibrate(50);
        }
    }

    // 事件监听器
    canvas.addEventListener('mousedown', (e) => {
        handleInteraction(e.clientX, e.clientY);
    });

    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        const touch = e.touches[0];
        handleInteraction(touch.clientX, touch.clientY);
    });

    // 键盘事件
    document.addEventListener('keydown', (e) => {
        if (sceneMain.style.display === 'block') {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height;
            handleInteraction(x, y);
        }
    });

    // 按钮事件
    btStart.addEventListener('click', (e) => {
        e.preventDefault();
        sceneTop.style.display = 'none';
        sceneLoading.style.display = 'block';

        // 模拟加载过程
        setTimeout(() => {
            sceneLoading.style.display = 'none';
            sceneMain.style.display = 'block';
            view.appendChild(canvas);
            animate();
        }, 1000);
    });

    btAbout.addEventListener('click', (e) => {
        e.preventDefault();
        about.style.display = 'block';
        aboutCover.style.display = 'block';
    });

    btClose.addEventListener('click', () => {
        about.style.display = 'none';
        aboutCover.style.display = 'none';
    });

    aboutCover.addEventListener('click', () => {
        about.style.display = 'none';
        aboutCover.style.display = 'none';
    });

    btBack.addEventListener('click', () => {
        sceneMain.style.display = 'none';
        sceneTop.style.display = 'block';
        if (animationId) {
            cancelAnimationFrame(animationId);
        }
        if (canvas.parentNode) {
            canvas.parentNode.removeChild(canvas);
        }
    });

    btFs.addEventListener('click', () => {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    });

    btFeedback.addEventListener('click', (e) => {
        e.preventDefault();
        feedbackEnabled = !feedbackEnabled;
        btFeedback.querySelector('a').textContent = `反馈: ${feedbackEnabled ? '开启' : '关闭'}`;
    });

    btBacktrack.addEventListener('click', (e) => {
        e.preventDefault();
        backtrackEnabled = !backtrackEnabled;
        btBacktrack.querySelector('a').textContent = `背景音乐: ${backtrackEnabled ? '开启' : '关闭'}`;
    });

    // 初始显示
    sceneTop.style.display = 'block';
});
