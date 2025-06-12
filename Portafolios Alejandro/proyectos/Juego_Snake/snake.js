const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");

const scale = 20;
const rows = canvas.height / scale;
const cols = canvas.width / scale;

let snake;
let food;
let score = 0;
let gameInterval;
let gameOver = false;

(function setup() {
  snake = new Snake();
  food = new Food();
  food.pickLocation();

  gameInterval = window.setInterval(() => {
    if (gameOver) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    food.draw();
    snake.update();
    snake.draw();

    if (snake.eat(food)) {
      score++;
      document.getElementById("score").innerText = `Puntaje: ${score}`;
      food.pickLocation();
    }

    if (snake.checkCollision()) {
      gameOver = true;
      alert(`Game Over! Tu puntaje fue: ${score}`);
      resetGame();
    }
  }, 150);
})();

window.addEventListener("keydown", (e) => {
  const direction = e.key.replace("Arrow", "").toLowerCase();
  snake.changeDirection(direction);
});

function resetGame() {
  score = 0;
  document.getElementById("score").innerText = `Puntaje: ${score}`;
  snake = new Snake();
  food.pickLocation();
  gameOver = false;
}

function Snake() {
  this.body = [{ x: 10, y: 10 }];
  this.xSpeed = 0;
  this.ySpeed = 0;
  this.justAte = false;

  this.draw = function () {
    ctx.fillStyle = "#0ff";
    ctx.shadowColor = "#0ff";
    ctx.shadowBlur = 10;
    for (let part of this.body) {
      ctx.fillRect(part.x * scale, part.y * scale, scale, scale);
    }
    ctx.shadowBlur = 0;
  };

  this.update = function () {
    let head = { x: this.body[0].x + this.xSpeed, y: this.body[0].y + this.ySpeed };

    // Termina si se sale de los bordes
    if (head.x >= cols || head.x < 0 || head.y >= rows || head.y < 0) {
      gameOver = true;
      alert(`Game Over! Tu puntaje fue: ${score}`);
      resetGame();
    
    }

    this.body.unshift(head);

    if (!this.justAte) {
      this.body.pop();
    } else {
      this.justAte = false;
    }
  };

  this.changeDirection = function (direction) {
    switch (direction) {
      case "up":
        if (this.ySpeed === 1) break;
        this.xSpeed = 0;
        this.ySpeed = -1;
        break;
      case "down":
        if (this.ySpeed === -1) break;
        this.xSpeed = 0;
        this.ySpeed = 1;
        break;
      case "left":
        if (this.xSpeed === 1) break;
        this.xSpeed = -1;
        this.ySpeed = 0;
        break;
      case "right":
        if (this.xSpeed === -1) break;
        this.xSpeed = 1;
        this.ySpeed = 0;
        break;
    }
  };

  this.eat = function (food) {
    const head = this.body[0];
    if (head.x === food.x && head.y === food.y) {
      this.justAte = true;
      return true;
    }
    return false;
  };

  this.checkCollision = function () {
    const head = this.body[0];
    for (let i = 1; i < this.body.length; i++) {
      if (this.body[i].x === head.x && this.body[i].y === head.y) return true;
    }
    return false;
  };
}

function Food() {
  this.x;
  this.y;

  this.pickLocation = function () {
    this.x = Math.floor(Math.random() * cols);
    this.y = Math.floor(Math.random() * rows);
  };

  this.draw = function () {
    ctx.fillStyle = "#f0f";
    ctx.shadowColor = "#f0f";
    ctx.shadowBlur = 15;
    ctx.fillRect(this.x * scale, this.y * scale, scale, scale);
    ctx.shadowBlur = 0;
  };
}


// Iniciar el juego la primera vez
resetGame();
