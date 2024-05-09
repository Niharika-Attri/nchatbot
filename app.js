const express = require('express')
const morgan = require('morgan')
const {PythonShell} = require('python-shell')

const app = express()

app.listen(3333, () => {
    console.log("connected to port 3333");
})

app.use(express.json())
app.use(morgan('dev'))

// Path to your Python script
var pythonScriptPath = 'model1.py';


// Configure options for PythonShell
var options = {
    mode: 'text',
    pythonOptions: ['-u'],
    scriptPath: '.', // Path to the directory containing the script
    args:[]
};

// Endpoint to handle incoming requests
app.post('/chatbot', (req, res) => {
    
    // user input from request body
    const user_input = req.body.input;
    const query = req.body.query

    if(!user_input){
        res.status(400).json({
            message:"please enter input"
        })
        return
    }

    // adding arguments to options
    options.args.push(user_input, query)

    // Create a new PythonShell instance
    let pyshell = new PythonShell(pythonScriptPath, options);

    // Collect output from Python script
    let output = [];

    // Handle incoming messages from Python script
    pyshell.on('message', (message) => {
        output.push(message)
    });

   
    // Handle errors
    pyshell.on('error', (error) => {
        console.error('PythonShell Error:', error);
        res.status(500).send('An error occurred');
        return
    });

    // Listen for 'close' event
    pyshell.on('close', (code) => {
        console.log('Python process closed with code:', code);
        // Send output back to the client
        res.status(200).json({ output });
    });

});

