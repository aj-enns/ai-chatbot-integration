# Deploy a Python (Flask) web app to Azure App Service - Sample Application

This is the sample Flask application for the Azure Quickstart [Deploy a Python (Django or Flask) web app to Azure App Service](https://docs.microsoft.com/en-us/azure/app-service/quickstart-python). For instructions on how to create the Azure resources and deploy the application to Azure, refer to the Quickstart article.

Sample applications are available for the other frameworks here:

* Django [https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-django-webapp-quickstart)
* FastAPI [https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart](https://github.com/Azure-Samples/msdocs-python-fastapi-webapp-quickstart)

If you need an Azure account, you can [create one for free](https://azure.microsoft.com/en-us/free/).

## Integrating Copilot Studio Chat Bot into a Python Website

This repository demonstrates how to integrate the Copilot Studio Chat bot into a Python (Flask) website using a direct link.

### Bot Secret Token

The bot secret token is a crucial part of the integration process. It is used to authenticate requests to the bot service. Ensure that you keep this token secure and do not expose it in your code.

### Setting Up the Bot Secret Token

To set up the bot secret token, follow these steps:

1. Create a `.env` file in the root directory of your project.
2. Add the following line to the `.env` file, replacing `YOUR_BOT_SECRET` with your actual bot secret token:

   ```
   BOT_SECRET=YOUR_BOT_SECRET
   ```

3. Load the environment variables in your `app.py` file using the `dotenv` package.

### `generate_token` Endpoint

The `generate_token` endpoint in `app.py` is responsible for generating a token to authenticate the chat bot. Here is a brief explanation of the endpoint:

```python
@app.route('/generate_token')
def generate_token():
    # Replace with your bot's secret and endpoint
    bot_secret = BOT_SECRET
    bot_endpoint = "https://directline.botframework.com/v3/directline/tokens/generate"

    headers = {
        "Authorization": f"Bearer {bot_secret}",
        "Content-Type": "application/json"
    }

    response = requests.post(bot_endpoint, headers=headers)
    if response.status_code == 200:
        token = response.json().get("token")
        return jsonify({"token": token})
    else:
        return jsonify({"error": "Failed to generate token"}), 500
```

This endpoint uses the bot secret token to request a new token from the bot service, which is then used to authenticate the chat bot.
