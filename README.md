 
# 📊 Music Trend Aggregator – Python Microservice

This microservice powers the **trend analysis and report generation** for the Music Trend Aggregator platform. It processes normalized song data from Spotify, YouTube, and TikTok to produce insightful analytics.

---

## 🚀 Features

### 🔍 Core Analytics
- 📈 **Weekly Trend Reports**  
  Highlights rising songs, top genres, and artist momentum.

- 🧠 **Genre Movement Analysis**  
  Tracks genre popularity trends week over week.

- 🌟 **Artist Growth Tracker**  
  Analyzes artist performance and discovery spikes.

- 📊 **Exportable Insights**  
  All analysis is exposed via clean JSON APIs.

---

## ⚙️ Tech Stack

| Component        | Technology        |
|------------------|-------------------|
| Language         | Python 3.10+       |
| Framework        | Flask              |
| Processing       | Pandas, NumPy      |
| API Docs         | Flask-RESTful      |
| Deployment       | Render.com         |

---


---

## 🔧 API Endpoints

| Method | Endpoint               | Description                        |
|--------|------------------------|------------------------------------|
| POST   | `/weekly-report`       | Get weekly trending summary        |
| POST   | `/genre-movement`      | Get genre movement analysis        |

**Example Request:**
```json
POST /weekly-report
{
  "tenantId": "tenant1"
}


{
  "topGenres": ["pop", "hip-hop", "edm"],
  "risingSongs": [{ "title": "Calm Down", "growth": 120% }],
  ...
}


# Clone the repo
git clone https://github.com/tushar-1745/music-trend-aggregator-py.git
cd music-trend-aggregator-py

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the service
python app.py


// /src/api/reportsApi.js

export const getWeeklyReport = () =>
  axios.post(`${VITE_PY_API}/weekly-report`, {
    tenantId: 'tenant1'
  }).then(res => res.data);
