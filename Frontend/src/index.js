require('dotenv').config();
const axios = require('axios');

async function getWeatherForecast(location, timesteps = ['1h', '1d'], units = 'metric') {
    const baseUrl = 'https://api.tomorrow.io/v4/weather/forecast';
    const apiKey = process.env.TOMORROW_IO_API_KEY;

    try {
        const response = await axios.get(baseUrl, {
            params: {
                location,               
                timesteps: timesteps.join(','), 
                units,                  
                apikey: apiKey          
            },
        });

        const { data } = response;
        return data;
    } catch (error) {
        console.error('Error fetching weather forecast:', error.response?.data || error.message);
    }
}

// Example Usage
(async () => {
    const location = '42.3478,-71.0466'; 
    const timesteps = ['1h', '1d'];      
    const units = 'metric';             

    const forecast = await getWeatherForecast(location, timesteps, units);
    console.log('Weather Forecast:', forecast);
})();