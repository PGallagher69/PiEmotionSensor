# Pi Emotion Sensor
A Raspberry Pi Emotion Sensor using Cognitive Services, Tweepy, a Scroll pHat HD and a Blinkt

Install the Blinkt library from your home directory using;

```shell
curl https://get.pimoroni.com/blinkt | bash
```

Install the Scroll pHat HD library from your home directory using;

```shell
curl https://get.pimoroni.com/scrollphathd | bash
```

Note, To use both the Blinkt and the Scroll pHat HD together, then you'll need to stack the two hats, soldering connections between the two.

You will need to install the Azure Cognitive Services SDK using;

```shell
python3 -m pip install cognitive-face
python3 -m pip install --upgrade azure-cognitiveservices-vision-face
```

If you need to run the script at startup, then you'll also need to run the above commands as sudo.
