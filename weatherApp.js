const citySelect = document.getElementById("city-select");
const getWeatherBtn = document.getElementById("get-weather-btn");
const weatherCard = document.getElementById("weather-card");

async function getWeather(city) {
  try {
    const response = await fetch(
      `https://weather-proxy.freecodecamp.rocks/api/city/${city}`
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.log(error);
    alert("Something went wrong, please try again later");
    return;
  }
}

async function showWeather(city) {
  let data = await getWeather(city);

  const icon = data?.weather?.[0]?.icon;
  const mainTemp = data?.main?.temp;
  const feelsLike = data?.main?.feels_like;
  const humidity = data?.main?.humidity;
  const windSpeed = data?.wind?.speed;
  const windGust = data?.wind?.gust;
  const weatherMain = data?.weather?.[0]?.main;
  const location = data?.name;

  document.getElementById("weather-icon").src = icon ?? "";
  document.getElementById("main-temperature").textContent = mainTemp ? mainTemp + "℃" : "N/A";
  document.getElementById("feels-like").textContent = feelsLike ? feelsLike + " ℃" : "N/A";
  document.getElementById("humidity").textContent = humidity ? humidity + "%" : "N/A";
  document.getElementById("wind").textContent = windSpeed ? windSpeed + " m/s" : "N/A";
  document.getElementById("wind-gust").textContent = windGust ? windGust + " m/s" : "N/A";
  document.getElementById("weather-main").textContent = weatherMain ?? "N/A";
  document.getElementById("location").textContent = location ?? "N/A";

  weatherCard.classList.remove("hidden");
}

getWeatherBtn.addEventListener("click", () => {
  const city = citySelect.value;

  if (!city) {
    return;
  }

  showWeather(city);
});
