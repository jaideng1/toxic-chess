var pieceNames = ["pawn", "rook", "king", "queen", "bishop", "knight"]

var IMAGES = {
  pawn: {
    white: 'https://cdn3.iconfinder.com/data/icons/chess-game-outline/32/chess_game-03-512.png',
    black: 'https://cdn0.iconfinder.com/data/icons/chess-26/128/2-512.png',
  },
  rook: {
    white: 'https://cdn1.iconfinder.com/data/icons/entertainment-events-hobbies/24/chess-rook-512.png',
    black: 'https://cdn3.iconfinder.com/data/icons/chess-7/100/black_rook-512.png',
  },
  king: {
    white: 'https://cdn.shopify.com/s/files/1/2209/1363/products/additional_megachess-44_33afb3f4-7bfe-4438-a46a-46b5d1b35078.png?v=1569064235',
    black: 'https://static.thenounproject.com/png/108498-200.png',
  },
  queen: {
    white: 'https://cdn2.iconfinder.com/data/icons/chess-pieces-1/500/Chess-Icons-Expanded-05-512.png',
    black: 'https://cdn2.iconfinder.com/data/icons/chess-pieces-1/500/Chess-Icons-Expanded-11-512.png',
  },
  bishop: {
    white: 'https://static.thenounproject.com/png/2275826-200.png',
    black: 'https://cdn4.iconfinder.com/data/icons/board-games-1/110/Bishop-512.png',
  },
  knight: {
    white: 'https://www.symbols.com/images/symbol/3408_white-knight.png',
    black: 'https://freesvg.org/img/Chess-Knight.png',
  },
}

const boardContainer = document.getElementById("board-container")

function setup() {
  board = createBoard(false);
  canvas = createCanvas(500,500)

  boardContainer.appendChild(canvas.canvas)

  for (let name of pieceNames) {
    try {
      IMAGES[name].white = loadImage(IMAGES[name].white);
    } catch (e) { console.log("Err getting " + name + ", white") }
    try {
      IMAGES[name].black = loadImage(IMAGES[name].black);
    } catch (e) { console.log("Err getting " + name + ", white") }
  }

  setupChecking()
}

let printAmount = 0;

var colored = []

function draw() {
  let size = 500 / 8;
  for (let y = 0; y < 8; y++) {
    for (let x = 0; x < 8; x++) {
      if (y % 2 != 0) {
        fill((x % 2)?255:[36, 143, 64])
      } else fill((x % 2)?[36, 143, 64]:255);

      if (gridSupposedToBeColored(x, y)) fill(196, 165, 81)

      rect(x * size, y * size, size, size);
    }
  }

  for (let i = board.length - 1; i > -1; i--) {
    for (let j = 0; j < board[i].length; j++) {
      if (board[i][j] == null) continue;

      image((IMAGES[board[i][j].type])[board[i][j].side], j * size, (7 - i) * size, size, size)
    }
  }
}

var nameCoords = [
    'a',
    'b',
    'c',
    'd',
    'e',
    'f',
    'g',
    'h'
]

function gridSupposedToBeColored(x, y) {
  for (let g of colored) {
    let c = chessCoordToXY(g)
    if (c.x == x && (7 - c.y) == y && board[y][x] != null) {
      return true;
    }
  }
  return false;
}

function getColoredGridIndex(x, y) {
  let i = 0;
  for (let g of colored) {
    let c = chessCoordToXY(g)
    if (c.x == x && (7 - c.y) == y) {
      return i;
    }
    i++;
  }
  return -1;
}

function gridNumberToChessCoord(gridN) {
    let y = 7 - Math.floor(gridN / 8)
    let x = gridN % 8 + 1

    return nameCoords[y] + x;
}

function chessCoordToXY(chessCoord) {
    let y = nameCoords.indexOf(chessCoord.split('')[0])
    let x = parseInt(chessCoord.split('')[1]) - 1

    return createVector(y, x) //Messed the naming up, too lazy to change them so i just change these two
}

function gridNumberToXY(gridNumber) {
    return chessCoordToXY(gridNumberToChessCoord(gridNumber))
}

function mousePressed() {
    if (colored.length == 0) return;

    let size = 500 / 8;
  
    for (let y = 0; y < 8; y++) {
      for (let x = 0; x < 8; x++) {
        if (mouseX > x * size && mouseX < (x + 1) * size) {
          if (mouseY > y * size && mouseY < (y + 1) * size) {
            let selected = createVector(x, y);
  
            if (gridSupposedToBeColored(x, y)) {
              console.log("Person chose ", selected)

              api('/choose', "POST", {
                choice: getColoredGridIndex(x, y)
              })
            }
          }
        }
      }
    }
  }
  