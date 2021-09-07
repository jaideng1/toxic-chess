
var board = new Array(8);

const SIDES = {
  WHITE: "white",
  BLACK: "black"
}

var currentTurn = SIDES.WHITE;

function getBoardDistance(pos1, pos2) {
  return Math.sqrt(Math.pow(pos2.x - pos1.x, 2) + Math.pow(pos2.y - pos1.y, 2))
}

function getGridDir(grid, dir) {
  if (dir == "up-left") {
    return grid[0];
  } else if (dir == "up") {
    return grid[1];
  } else if (dir == "up-right") {
    return grid[2];
  } else if (dir == "left") {
    return grid[3];
  } else if (dir == "right") {
    return grid[5];
  } else if (dir == "down-left") {
    return grid[6];
  } else if (dir == "down") {
    return grid[7];
  } else if (dir == "down-right") {
    return grid[8];
  }

  return grid[4];
}

function kingInCheck(side) {
  let king = null;

  for (let row of board) {
    for (let piece of row) {
      if (!piece) continue;
      if (piece.type == "king" && piece.side == side) king = piece;
    }
  }

  for (let row of board) {
    for (let piece of row) {
      if (!piece) continue;
      if (piece.side != side && piece.isLegalMove(king.position)) {
        return true;
      }
    }
  }

  return false;
}

function getDirection(pos1, pos2) {
  if (pos1.x == pos2.x) {
    if (pos1.y > pos2.y) {
      return "down";
    } else return "up";
  } else if (pos1.y == pos2.y) {
    if (pos1.x > pos2.x) {
      return "left";
    } else return "right";
  } else {
    if (pos1.y > pos2.y) {
      if (pos1.x > pos2.x) {
        return "down-left";
      } else return "down-right";
    } else {
      if (pos1.x > pos2.x) {
        return "up-left";
      } else return "up-right";
    }
  }
}

function isDiangle(dir) {return dir.includes("-")}

function getBoardPiecesBetweenTwoLocs(loc1, loc2) {
  let dir = getDirection(loc1, loc2)
  let pieces = [];
  if (isDiangle(dir) || dir.includes("up") || dir.includes("down")) {
    let isUp = dir.includes("up");
    let x = loc1.x;
    for (let i = isUp ? loc1.y : loc2.y; i < (isUp ? loc2.y : loc2.y) + 1; i++) {
      pieces.push(board[i][x]);
      if (isDiangle(dir)) x += (dir.includes("right")) ? 1 : -1;
    }
  } else {
    let isRight = (dir == "right");
    for (let i = isRight ? loc1.x : loc2.x; i < (isRight ? loc2.x : loc1.x) + 1; i++) {
      pieces.push(board[loc1.y][i]);
    }
  }
  return pieces;
}

class Piece {
  constructor(type, grid, side, pos) {
    if (board) {} else throw "Board does not exist."

    this.grid = grid;
    this.type = type;
    this.side = side;
    this.position = pos;

    this.haveMoved = false;
  }

  isPossible(to) {
    let dir = getDirection(this.position, to);
    if (!isDiangle(dir)) {
      return true;
    } else {
      let adjY = this.position.y - to.y;
      let adjX = this.position.x - to.x;

      return Math.abs(adjY) == Math.abs(adjX);
    }
  }

  isLegalMove(to) {
    if (!this.isPossible(to)) return false;

    let dir = getDirection(this.position, to);

    if (getBoardDistance(this.position, to) > getGridDir(this.grid, dir)) {
      if (this.type == "king" && !this.haveMoved) {
        if (this.side == SIDES.WHITE) {
          if (to.x == 6 && board[0][8] instanceof Rook) {
            if (!board[0][8].haveMoved && to.y == this.position.y) {
              if (board[0][7] == null && board[0][6] == null) {
                return true;
              }
            }
          } else if (to.x == 2 && board[0][0] instanceof Rook) {
            if (!board[0][0].haveMoved && to.y == this.position.y) {
              if (board[0][1] == null && board[0][2] == null && board[0][3] == null) {
                return true;
              }
            }
          }
        } else {
          if (to.x == 6 && board[7][8] instanceof Rook) {
            if (!board[0][8].haveMoved && to.y == this.position.y) {
              if (board[0][7] == null && board[7][6] == null) {
                return true;
              }
            }
          } else if (to.x == 2 && board[7][0] instanceof Rook) {
            if (!board[7][0].haveMoved && to.y == this.position.y) {
              if (board[7][1] == null && board[7][2] == null && board[7][3] == null) {
                return true;
              }
            }
          }
        }
      }

      return false;
    }

    if (isDiangle(dir)) {
      return this.canGoDiangle() && !this.piecesInTheWay(to);
    }

    return this.canGoNonDiangle() && !this.piecesInTheWay(to);
  }

  piecesInTheWay(to) {
    let pieces = getBoardPiecesBetweenTwoLocs(this.position, to);
    for (let i = 0; i < pieces.length; i++) {
      if (i == 0 || i == pieces.length - 1) continue;
      if (pieces[i] != null) return true;
    }

    if (pieces[pieces.length - 1]) if (pieces[pieces.length - 1].side == this.side) return true;

    return false;
  }

  canGoDiangle() {
    let grid = this.grid;
    return (grid[0] > 0 && grid[2] > 0 && grid[6] > 0 && grid[8] > 0);
  }

  canGoNonDiangle() {
    let grid = this.grid;
    return (grid[1] > 0 && grid[3] > 0 && grid[5] > 0 && grid[7] > 0);
  }

  move(to) {
    this.haveMoved = true;

    board[to.y][to.x] = this;
    board[this.position.y][this.position.x] = null;

    this.position = to;
  }
}

class King extends Piece {
  constructor(side, pos) {
    super("king", [
      1.5, 1 ,1.5,
      1  , 0 ,1  ,
      1.5, 1 ,1.5
    ], side, pos)
  }
}

class Queen extends Piece {
  constructor(side, pos) {
    super("queen", [
      9,9,9,
      9,0,9,
      9,9,9
    ], side, pos)
  }
}

class Rook extends Piece {
  constructor(side, pos) {
    super("rook", [
      0,9,0,
      9,0,9,
      0,9,0
    ], side, pos)
  }
}

class Bishop extends Piece {
  constructor(side, pos) {
    super("bishop", [
      9,0,9,
      0,0,0,
      9,0,9
    ], side, pos)
  }
}

class Knight extends Piece {
  constructor(side, pos) {
    super("knight", null, side, pos)
  }
  isLegalMove(to) {
    if (board[to.y][to.x]) if (board[to.y][to.x].side == this.side) return false;

    if (this.position.x - 2 == to.x || this.position.x + 2 == to.x) {
      if (this.position.y - 1 == to.y || this.position.y + 1 == to.y) {
        return true;
      }
    } else if (this.position.x - 1 == to.x || this.position.x + 1 == to.x) {
      if (this.position.y - 2 == to.y || this.position.y + 2 == to.y) {
        return true;
      }
    }
  }
}

class Pawn extends Piece {
  constructor(side, pos) {
    super("pawn", null, side, pos)
  }

  isLegalMove(to) {
    if (this.side == SIDES.WHITE) {
      if (to.y <= this.position.y + 1 + (this.haveMoved ? 0 : 1)) {
        if (to.y > this.position.y) {
          if (to.x == this.position.x) {
            let pieces = getBoardPiecesBetweenTwoLocs(this.position, to.y);

            if (pieces[pieces.length - 1] != null) {
              return false;
            }

            if (pieces.length == 3) {
              if (pieces[1] != null) {
                return;
              }
            }

            return true;
          } else {
            if (this.position.x - 1 == to.x || this.position.x + 1 == to.x) {
              if (board[to.y][to.x]) {
                if (board[to.y][to.x].side != this.side) return true;
              }
            }

            //// TODO: Add en passant
          }
        }
      }
    } else {
      if (to.y >= this.position.y - 1 - (this.haveMoved ? 0 : 1)) {
        if (to.y < this.position.y) {
          if (to.x == this.position.x) {
            let pieces = getBoardPiecesBetweenTwoLocs(this.position, to.y);

            if (pieces[pieces.length - 1] != null) {
              return false;
            }

            if (pieces.length == 3) {
              if (pieces[1] != null) {
                return;
              }
            }

            return true;
          } else {
            if (this.position.x - 1 == to.x || this.position.x + 1 == to.x) {
              if (board[to.y][to.x]) {
                if (board[to.y][to.x].side != this.side) return true;
              }
            }
          }
        }
      }
    }

    return false;
  }

  move(to) {
    this.haveMovedYet = true;

    board[to.y][to.x] = this;
    board[this.position.y][this.position.x] = null;

    this.position = to;
  }
}

function createBoard(isTestBoard) {
  if (isTestBoard) return createTestBoard();

  let board = new Array(8);
  //BTW board is flipped, so the white is on top in the board grid but in the display it's on bottom.
  for (let i = 0; i < board.length; i++) {
    board[i] = [];

    if (i == 0 || i == 7) {
      let side = (i == 0) ? SIDES.WHITE : SIDES.BLACK;
      let left = new Queen(side, createVector(3,i));
      let right = new King(side, createVector(4,i));

      // if (side == SIDES.BLACK) {
      //   right = new King(side, createVector(3,i));
      //   left = new Queen(side, createVector(4,i));
      // }

      board[i] = [
        new Rook(side, createVector(0,i)),
        new Knight(side, createVector(1,i)),
        new Bishop(side, createVector(2,i)),
        left,
        right,
        new Bishop(side, createVector(5,i)),
        new Knight(side, createVector(6,i)),
        new Rook(side, createVector(7,i)),
      ]

    } else if (i == 1 || i == 6) {
      let side = (i == 1) ? SIDES.WHITE : SIDES.BLACK;
      board[i] = [
        new Pawn(side, createVector(0,i)),
        new Pawn(side, createVector(1,i)),
        new Pawn(side, createVector(2,i)),
        new Pawn(side, createVector(3,i)),
        new Pawn(side, createVector(4,i)),
        new Pawn(side, createVector(5,i)),
        new Pawn(side, createVector(6,i)),
        new Pawn(side, createVector(7,i)),
      ];
    } else {
      board[i] = generateNulls(8);
    }
  }
  return board;
}

function createTestBoard() {
  let board = new Array(8);

  for (let i = 0; i < board.length; i++) {
    board[i] = [];

    board[i] = generateNulls(8);
  }

  board[3][3] = new Queen(SIDES.WHITE, createVector(3,3))

  return board;
}

function generateNulls(len) {
  let nls = [];
  for (let i = 0; i < len; i++) {
    nls.push(null)
  }
  return nls;
}

function createPieceFromName(name, side, loc) {
  switch(name) {
    case "pawn":
      return new Pawn(side, loc)
    case "king":
      return new King(side, loc)
    case "queen":
      return new Queen(side, loc)
    case "knight":
      return new Knight(side, loc)
    case "bishop":
      return new Bishop(side, loc)
    case "rook":
      return new Bishop(side, loc)
    default:
      return null
  }
}
