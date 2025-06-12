
let score = 0;
let time = 30;
let interval;
let circleTimer;
const scoreDisplay = document.getElementById('score');
const timeDisplay = document.getElementById('time');
const playArea = document.getElementById('play-area');
const startBtn = document.getElementById('start-btn');

function startGame() {
  score = 0;
  time = 30;
  scoreDisplay.textContent = score;
  timeDisplay.textContent = time;
  startBtn.disabled = true;
  interval = setInterval(updateTimer, 1000);
  spawnCircle();
}

function updateTimer() {
  time--;
  timeDisplay.textContent = time;
  if (time <= 0) {
    clearInterval(interval);
    clearTimeout(circleTimer);
    alert("¡Tiempo terminado! Tu puntuación es: " + score);
    startBtn.disabled = false;
    playArea.innerHTML = '';
  }
}

function spawnCircle() {
  const circle = document.createElement('div');
  circle.classList.add('circle');
  const size = 50;
  const maxX = playArea.clientWidth - size;
  const maxY = playArea.clientHeight - size;
  circle.style.left = Math.random() * maxX + 'px';
  circle.style.top = Math.random() * maxY + 'px';

  circle.addEventListener('click', () => {
    score++;
    scoreDisplay.textContent = score;
    circle.remove();
    spawnCircle();
  });

  playArea.innerHTML = '';
  playArea.appendChild(circle);
  circleTimer = setTimeout(() => {
    if (playArea.contains(circle)) {
      circle.remove();
      spawnCircle();
    }
  }, 1500);
}

startBtn.addEventListener('click', startGame);
