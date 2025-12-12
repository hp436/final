# Final Project — FastAPI Calculator + New Feature Integration (Power Operation)

##  This application extends the original FastAPI Calculator and Authentication system by introducing a new calculation feature: Power (a^b). The project now includes:
- A FastAPI backend with user registration, login, JWT authentication, and full CRUD support for calculator operations.
- An enhanced calculator that supports addition, subtraction, multiplication, division, and the newly implemented power operation (a^b).
- A user-friendly HTML front-end updated to include the new feature.
- A complete automated testing suite:
- Unit tests for operation logic
- Integration tests for API routes
- End-to-end (E2E) tests using Playwright to validate real browser behavior
- Docker containerization with a published Docker Hub image for seamless deployment.
---


# Running the App

### **Create venv**

```bash
python3 -m venv venv
source venv/bin/activate
```

### **Install Requirements**
```bash
pip install -r requirements.txt
```


### **Start FastAPI locally**
```bash
uvicorn main:app --reload
```
Visit 
http://127.0.0.1:8000/docs

Server runs at:
http://127.0.0.1:8000
http://127.0.0.1:8000/docs (Swagger API)

---

## Running the tests
``` bash
pytest
```

```bash
npx playwright install
npx playwright test
```

--- 

# Running the Front-end

### The front-end files are located in the templates/ folder:
templates/index.html
templates/register.html
templates/login.html

### To test the UI:

Start the backend:
uvicorn main:app --reload

Open in browser:
http://127.0.0.1:8000/
http://127.0.0.1:8000/register
http://127.0.0.1:8000/login

### These pages communicate with the backend using JavaScript fetch().



--- 


## Dockerhub link

https://hub.docker.com/repository/docker/hv2915/final/general