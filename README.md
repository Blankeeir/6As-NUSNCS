# SWJS
A cutting-edge traffic management system based on large-language model. Integration of LLMS with existing data sources to enhance traffic flows, slash congestion, and boost green mobility.

## Before use
Run `make install ` to download the dependencies. 
Then you can run `python3 main.py` to run the server.
You can test whether the setup is correct with:
`curl -X GET http://127.0.0.1/echo -H "Content-Type: application/json" -d '{"user_input":"YourInputHere"}'`
and
`curl http://127.0.0.1/ping`

(Optional) If your development introduce new dependencies, remember to update the `requirements.txt` file.

(Optional) If your development requires open_ai endpoint, copy and rename the `.env.dev` to `.env` and add real API key. DO NOT hardcode and commit your api_key (and other secrets?) anytime.







