<h1 align="center" id="title">Bitcoin Price Alert System</h1>

<p id="description">A Django based project which will notify if Bitcoin traded on a specified price.</p>

<h2>Project Architecture:</h2>

<img src="https://i.ibb.co/vhZ5SH6/Architecture.png" alt="project-screenshot" width="auto" />

Components:

*   REST API SERVER
      * Supported APIs
          * ```/register/``` to register a user.
          * ```/api/token/``` to generate JWT token for registered user.
          * ```/api/token/refresh``` to generate JWT token using refresh token.
          * ```/alerts/create/``` to create alert.
          * ```/alerts/fetch-all``` to get all alerts. This api paginates the response and supports status filter as well.
       * Tasks performed by server
          * JWT Authentication
          * Pagination
          * Caching the user data
          * Caching the price alerts
*     
*   something else

<h2>🛠️ Installation Steps:</h2>

<p>1. Clone the repository</p>

```
git clone https://github.com/sourcenaman/btc-price-alert.git
```

<p>2. Build images</p>

```
docker-compose build
```

<p>3. Run the project (in background)</p>

```
docker-compose up -d
```

<p>4. Run the project</p>

```
docker-compose up
```
