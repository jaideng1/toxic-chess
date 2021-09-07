const turnText = document.getElementById("turn"),
    readyButton = document.getElementById('confirm');

var currentTurn = "white";

async function api(ext, method="GET", body={}) {
    let response, data;

    try {
        if (method == "GET") {
            response = await fetch("http://" + location.host + "/api" + (ext.startsWith("/") ? ext : '/' + ext))
        } else {
            response = await fetch("http://" + location.host + "/api" + (ext.startsWith("/") ? ext : '/' + ext), {
                method: "POST",
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json'
                },
                redirect: 'follow',
                body: JSON.stringify(body)
            })
            return {
                success: true
            }
        }
    } catch (e) {
        return {
            success: false
        }
    }

    try {
        data = await response.json()
    } catch (e) {
        return {
            success: false
        }
    }

    return data
}

function onFinishTurn() {
    api('/finishturn')
    setTurn((turn == 'white') ? 'black' : 'white')
}

function setTurn(turn) {
    if (turn == 'black') {
        turnText.textContent = "Current Turn: Black (Computer)"
    } else turnText.textContent = "Current Turn: White (You)"
}

function onStart() {
    setTurn(currentTurn)
    api('started').then(data => {
        if (!data.success) {
            console.error("There was an error getting the data.")
        }
    })
    readyButton.textContent = "Click this once you're finished with your turn."
    readyButton.onclick = () => {
        onFinishTurn()
    }
}

function setupChecking() {
    setInterval(() => {
        checkApi()
    }, 1000)
}

let piece_names = [
    "pawns",
    "rooks",
    "queen",
    "king",
    "knights",
    "bishops"
]

var checkChoices = true;

async function checkApi() {
    let data = await api("/board")
    if (data["success"] != null) if (data["success"] == null) return;

   // print(data)

    let wherePiecesAre = []
    
    for (let piece of piece_names) {
        // print((data["white"])[piece], data["white"], piece)
        let l = (data["white"])[piece].length;
        for (let i = 0; i < l; i++) {
            let black_p = (((data["black"])[piece])[i] > -1) ? gridNumberToXY(((data["black"])[piece])[i]) : -1
            let white_p = (((data["white"])[piece])[i] > -1) ? gridNumberToXY(((data["white"])[piece])[i]) : -1

            //console.log(white_p, ((data["white"])[piece])[i])

            let pieceSplit = piece.split('')
            if (pieceSplit[pieceSplit.length - 1] == 's') {
                pieceSplit.pop()
            }
            
            let name = pieceSplit.join('')

            if (black_p != -1) {
                if (board[black_p.y][black_p.x] == null) {
                    board[black_p.y][black_p.x] = createPieceFromName(name, "black", black_p)
                } else if (board[black_p.y][black_p.x].type != name || board[black_p.y][black_p.x].side != "black") {
                    board[black_p.y][black_p.x] = createPieceFromName(name, "black", black_p)
                }

                wherePiecesAre.push({
                    x: black_p.x,
                    y: black_p.y,
                    piece: name,
                    side: "black"
                })
            }
            
            if (white_p != -1) {
                if (board[white_p.y][white_p.x] == null) {
                    board[white_p.y][white_p.x] = createPieceFromName(name, "white", white_p)
                } else if (board[white_p.y][white_p.x].type != name || board[white_p.y][white_p.x].side != "white") {
                    board[white_p.y][white_p.x] = createPieceFromName(name, "white", white_p)
                }

                wherePiecesAre.push({
                    x: white_p.x,
                    y: white_p.y,
                    piece: name,
                    side: "white"
                })
            }
            
        }

        let choices = await api('/choose')
        if (checkChoices) colored = choices;

        let turn = await api('/turn')
        currentTurn = turn;

        if (currentTurn == "black") {
            readyButton.disabled = true;
        } else readyButton.disabled = false;
    }

    for (let y = 0; y < 8; y++) {
        for (let x = 0; x < 8; x++) {
            if (!checkIfLocationIsInList({x, y}, wherePiecesAre) && board[y][x] != null) {
                console.log("Loc is not in list", {x,y})
                board[y][x] = null;
            }
        }
    }
}

function checkIfLocationIsInList(loc, list) {
    for (let loc_ of list) {
        if (loc_.x == loc.x && loc_.y == loc.y) {
            return true;
        }
    }
}

function chooseCustomChoice() {
    if (colored.length == 0) {alert('There are no choices currently.'); return;}

    let to = prompt('What is [the piece] taking?')
    api('choose', "POST", {
        choice: -1,
        move: to
    })
}