# Sudoku Solving Twitter Bot

Send a image of a unsolved Sudoku puzzle as a tweet to [@easySudoku](https://twitter.com/easysudoku) and get the solved puzzle as a reply.

## Dependencies

* A Twitter app created on [apps.twitter.com](https://apps.twitter.com/)
* [Python](https://www.python.org)
* Python Libraries (requirements.txt)

## Create and configure a Twitter app

1. Create a Twitter app on [apps.twitter.com](https://apps.twitter.com/)

2. On the **Permissions** tab > **Access** section > enable **Read, Write and Access direct messages**.

3. On the **Keys and Access Tokens** tab > **Your Access Token** section > click **Create my access token** button.

4. On the **Keys and Access Tokens** tab, take note of the `consumer key`, `consumer secret`, `access token` and `access token secret`.

## Setup & Run

You have to follow these steps in the right order. 

### Setup Bot

1. Install python requirements

    ```bash
    pip3 install -r requirements.txt
    ```

2. Define key variables locally using the keys, access tokens noted previously and your twitter user id from [gettwitterid.com](http://gettwitterid.com) (replace the text after the =)

    ```bash
    export CONSUMER_KEY={INSERT_CONSUMER_KEY}
    export CONSUMER_SECRET={INSERT_CONSUMER_SECRET}
    export ACCESS_TOKEN={INSERT_ACCESS_TOKEN}
    export ACCESS_TOKEN_SECRET={INSERT_ACCESS_TOKEN_SECRET}
    export PORT={INSERT_FLASK_PORT}
    export CURRENT_USER_ID={INSERT_USER_ID}
    ```

### Deploy Bot

1. Start the flask server

```bash
python3 server.py
```

2. Make sure your flask server is public (for example with a nginx to https://your-domain.com/twitter)

### Setup Twitter Webhook

1. Setup Bot and Deploy the Bot

2. Go to [developer.twitter.com/environments](https://developer.twitter.com/en/account/environments)

3. On **Account Activity API/Sandbox** > **Set up dev environment** button > add **Dev environment label**

4. Define environment variables locally using your Dev environment label and your webhook url like https://your-domain.com/twitter (replace the text after the =)

    ```bash
    export ENV_LABEL={INSERT_ENV_LABEL}
    export WEBHOOK_ULR={INSERT_WEBHHOK_URL}
    ```

5. Add your URL as webhook

    ```bash
    python webhook-scripts/create-webhook.py
    ```

6. Subscribe your twitter account to the created webhook

    ```bash
    python webhook-scripts/subscribe-webhook.py
    ```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

