const express = require('express')
const morgan = require('morgan')
const {PythonShell} = require('python-shell')

const app = express()

app.listen(3333, () => {
    console.log("connected to port 3333");
})

app.use(express.json())
app.use(morgan('dev'))

// Endpoint to handle incoming requests
app.post('/chatbot', (req, res) => {
    
    // Retrieve user input from query parameter
    const user_input = req.body.input;
    const query = req.body.query

    if(!user_input){
        res.status(400).json({
            message:"please enter input"
        })
        return
    }

    // Path to your Python script
    const pythonScriptPath = 'model1.py';

    // Configure options for PythonShell
    const options = {
        mode: 'text',
        pythonOptions: ['-u'],
        scriptPath: '.', // Path to the directory containing the script
        //args: [JSON.stringify(user_input), JSON.stringify(query)], // Pass user input as argument
        args:[user_input, query]

    };

    // Create a new PythonShell instance
    let pyshell = new PythonShell(pythonScriptPath, options);

    // Collect output from Python script
    let output = [];

    // Handle incoming messages from Python script
    pyshell.on('message', (message) => {
        output.push(message)
        // console.log("message:", message);
        //res.json({output})
    });
        // const messageTimeout = 5000;
        // setTimeout(() => {
        //     console.log('No message received within the timeout period.');
        //     res.status(408).json({
        //         message: "Request timed out"
        //     })
        //     return
        // }, messageTimeout);
   
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

