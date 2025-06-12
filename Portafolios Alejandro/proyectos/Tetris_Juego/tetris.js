const tetris = document.getElementById('tetris');
const scoreDisplay = document.getElementById('score');
let grid = [];
let score = 0;
const rows = 20;
const cols = 10;

for (let i = 0; i < rows * cols; i++) {
  const cell = document.createElement('div');
  cell.classList.add('cell');
  tetris.appendChild(cell);
  grid.push(cell);
}

const shapes = [
  [1, cols + 1, cols * 2 + 1, 2],       // L
  [0, cols, cols + 1, cols * 2 + 1],   // Z
  [1, cols, cols + 1, cols + 2],       // T
  [0, 1, cols, cols + 1],              // O
  [1, cols + 1, cols * 2 + 1, cols * 3 + 1] // I
];

let current = 0;
let position = 4;

function draw() {
  clear();
  shapes[current].forEach(i => grid[position + i]?.classList.add('active'));
}

function clear() {
  grid.forEach(cell => cell.classList.remove('active'));
}

function freeze() {
  shapes[current].forEach(i => {
    const index = position + i;
    grid[index]?.classList.remove('active');
    grid[index]?.classList.add('fixed');
  });
}

function isCollision(offset) {
  return shapes[current].some(i => {
    const index = position + i + offset;
    return (
      index >= rows * cols ||
      grid[index]?.classList.contains('fixed') ||
      (offset === 1 && (position + i) % cols === cols - 1) ||
      (offset === -1 && (position + i) % cols === 0)
    );
  });
}

function moveDown() {
  if (!isCollision(cols)) {
    position += cols;
  } else {
    freeze();
    removeLines();
    current = Math.floor(Math.random() * shapes.length);
    position = 4;
    if (isCollision(0)) {
      alert("Game Over");
      clearInterval(gameLoop);
    }
  }
  draw();
}

function moveLeft() {
  if (!isCollision(-1)) {
    position -= 1;
    draw();
  }
}

function moveRight() {
  if (!isCollision(1)) {
    position += 1;
    draw();
  }
}

function rotate() {
  clear();
  current = (current + 1) % shapes.length;
  draw();
}

function removeLines() {
  for (let r = 0; r < rows; r++) {
    const row = grid.slice(r * cols, (r + 1) * cols);
    if (row.every(cell => cell.classList.contains('fixed'))) {
      row.forEach(cell => cell.classList.remove('fixed'));
      const removed = grid.splice(r * cols, cols);
      grid = removed.concat(grid);
      grid.forEach(cell => tetris.appendChild(cell));
      score += 10;
      scoreDisplay.textContent = `Puntaje: ${score}`;
    }
  }
}

document.addEventListener('keydown', e => {
  if (e.key === 'ArrowLeft') moveLeft();
  if (e.key === 'ArrowRight') moveRight();
  if (e.key === 'ArrowDown') moveDown();
  if (e.key === 'ArrowUp') rotate();
});

draw();
const gameLoop = setInterval(moveDown, 800);
