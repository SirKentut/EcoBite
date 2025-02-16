const express = require('express');
const axios = require('axios');

const app = express();
const PORT = 3000;

// Middleware
app.use(express.json());  // For parsing JSON bodies

// 1. Flutter Client -> Backend Server
// Endpoint to receive food image and return weight
app.post('/analyze-food', async (req, res) => {
    console.log('Received request:', req.body);

    // TODO: (Subject to change) / suggested async functions below
    // 1. Receive food image

    // 2. Process through OpenAI/other classification (step 2 in diagram)

    //expected json object format for detected food
    const detectedFoods = {
        "foods": [
            {"name": "chicken breast"},
            {"name": "apple slices, dried"},
            {"name": "potato chips"}
        ]
    };
    // 3. Get volume from Volume Estimation System (step 3)

        // Expected results: Volume:{'rice': 340.0309850402668, 'vegetable': 65.82886736721441, 'chicken': 188.60914207925677} unit: cm^3

        const volumeData = {
            'chicken breast': 188.60914207925677,
            'apple slices, dried': 65.82886736721441,
            'potato chips': 340.0309850402668
        };

    console.log('Volume results:', volumeData);
        
    // Step 4: Get densities for all detected foods
    const densityResults = await getFoodDensity(detectedFoods);
    console.log('Density results:', densityResults);
    /*
        [
            {
                "density": 1.07,
                "food_name": "chicken breast",
                "source": "api"
            },
            {
                "density": 0.24,
                "food_name": "apple slices, dried",
                "source": "reference"
            },
            {
                "density": 0.09,
                "food_name": "potato chips",
                "source": "reference"
            }
        ]
    */
    
    // 5. Calculate weight (step 5) by taking the volume and density data
    const response  = calculateTotalWeight(volumeData, densityResults);
    console.log('Weights calculated:', response);
    res.json(response);
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

// 4. Database interaction for food densities// Add the density service function
async function getFoodDensity(foods) {
    try {
        const response = await axios.post('http://localhost:5000/density/process-foods', {
            foods: foods.foods  // Access the foods array from the input object
        }, {
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        return response.data.foods;
    } catch (error) {
        console.error('Error getting food density:', error.message);
        throw error;
    }
}

// 5. Weight calculation
function gramsToLbs(grams) {
    return grams * 0.00220462;
}

function calculateTotalWeight(volumeData, densityResults) {
    // Initialize the response object
    const response = {
        weight: {
            lbs: 0,
            grams: 0,
            breakdown: []
        }
    };

    // Create a map of food names to densities for easy lookup
    const densityMap = {};
    densityResults.forEach(item => {
        densityMap[item.food_name] = item.density;
    });

    // Calculate weight for each food item
    for (const [foodName, volume] of Object.entries(volumeData)) {
        // Skip if we don't have density data for this food
        if (!densityMap[foodName]) {
            console.warn(`No density data found for ${foodName}`);
            continue;
        }

        // Calculate weight in grams (density * volume)
        const weightGrams = volume * densityMap[foodName];
        const weightLbs = gramsToLbs(weightGrams);

        // Add to the breakdown
        response.weight.breakdown.push({
            foodItem: foodName,
            weight: {
                lbs: Number(weightLbs.toFixed(2)),
                grams: Number(weightGrams.toFixed(2))
            },
            volume: `${volume.toFixed(1)}ml`,
            density: densityMap[foodName]
        });

        // Add to totals
        response.weight.grams += weightGrams;
        response.weight.lbs += weightLbs;
    }

    // Round the totals
    response.weight.grams = Number(response.weight.grams.toFixed(2));
    response.weight.lbs = Number(response.weight.lbs.toFixed(2));

    return response;
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
