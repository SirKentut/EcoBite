const express = require('express');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());  // For parsing JSON bodies

// 1. Flutter Client -> Backend Server
// Endpoint to receive food image and return weight
app.post('/analyze-food', (req, res) => {
    console.log('Received request:', req.body);

    // TODO: (Subject to change) / suggested async functions below
    // 1. Receive food image
    // 2. Process through OpenAI/other classification (step 2 in diagram)
    // 3. Get volume from Volume Estimation System (step 3)
    // 4. Query density from database (step 4)
        /**
         * How I can do this:
         * - Create a flask service 
         * - 
         */
    // 5. Calculate weight (step 5)

    res.json({
        weight: {
            lbs: 0,
            grams: 0,
            breakdown: [
                {
                    foodItem: "apple",
                    weight: {
                        lbs: 0.5,
                        grams: 226.796
                    },
                    volume: "250ml",
                    density: 0.9 // g/ml
                },
                {
                    foodItem: "sandwich",
                    weight: {
                        lbs: 2,
                        grams: 907.184
                    },
                    volume: "1000ml",
                    density: 0.9 // g/ml
                }
            ]
        }
    });
});

// 2. Backend -> Food Classification Service
// This could be an internal function or separate service
async function classifyFood(foodImage) {
    // TODO: Integrate with OpenAI or other classification models
}

// 3. Backend -> Volume Estimation System
// This could be an API call to your volume estimation service
async function getVolumeEstimation(foodData) {
    // TODO: Call volume estimation system
}

// 4. Database interaction for food densities
async function getFoodDensity(foodItem) {
    // TODO: Query database for food density
}

// 5. Weight calculation
function calculateWeight(volume, density) {
    return volume * density;
}

// Health check endpoint
app.get('/ping', (req, res)=>{
    res.status(200);
    res.send("Pong: TreeHacks 2025");
});

app.listen(PORT, (error) =>{
    if(!error)
        console.log("Server is Successfully Running, and App is listening on port " + PORT)
    else 
        console.log("Error occurred, server can't start", error);
    }
);
