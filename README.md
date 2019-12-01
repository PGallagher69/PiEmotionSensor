# Pi Emotion Sensor

## What it's about:

A Raspberry Pi Emotion Sensor using Azure Cognitive Services, Tweepy, a Scroll pHat HD and a Blinkt.

## Installation Instructions:

### Twitter:

Apply for a Twitter Developer Account at;

https://developer.twitter.com

Create a New Twitter app and grab;

- Consumer API Key (ckey)
- Consumer API Secret (csecret)
- Access Token (atoken)
- Access Token Secret (asecret)

Fill in the fields in the PiEmotionSensor.py file.

### Azure Cognitive Services:

Create an Azure Cognitive Services Resource at;

https://portal.azure.com

Grab;

- Key1 (KEY)
- Endpoint (ENDPOINT)

Fill in the fields in the PiEmotionSensor.py file

### Blinkt:

Install the Blinkt library from your home directory using;

```shell
curl https://get.pimoroni.com/blinkt | bash
```

### Scroll pHat HD:

Install the Scroll pHat HD library from your home directory using;

```shell
curl https://get.pimoroni.com/scrollphathd | bash
```

Note: To use both the Blinkt and the Scroll pHat HD together, then you'll need to stack the two hats, soldering connections between the two.

### Azure Cognitive Services SDK:

Install the Azure Cognitive Services SDK using;

```shell
python3 -m pip install cognitive-face
python3 -m pip install --upgrade azure-cognitiveservices-vision-face
```

### Tweepy:

Install Tweepy using;

```shell
python3 -m pip install tweepy
```

NOTE: If you need to run the script at startup, then you'll also need to run the above commands as sudo.
