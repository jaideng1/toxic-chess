const path = require('path')
var app = require('express')()

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'display.html'))
})

app.get('/display.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'display.js'))
})

app.get('/connections.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'connections.js'))
})

app.get('/pieces.js', (req, res) => {
    res.sendFile(path.join(__dirname, 'pieces.js'))
})

app.get('/display.css', (req, res) => {
    res.sendFile(path.join(__dirname, 'display.css'))
})

app.listen(3000, () => {
    console.log("Test server started on port 3000.")
})