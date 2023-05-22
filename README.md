<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/Your-Cheese/AI_Chatbot">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">AI Chatbot GUI</h3>

  <p align="center">
    Easily set up your own AI Chatbot that can talk to you in real-time
    <br />
    <a href="https://github.com/Your-Cheese/AI_Chatbot"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Your-Cheese/AI_Chatbot">View Demo</a>
    ·
    <a href="https://github.com/Your-Cheese/AI_Chatbot/issues">Report Bug</a>
    ·
    <a href="https://github.com/Your-Cheese/AI_Chatbot/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <!-- <li><a href="#contact">Contact</a></li> -->
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Product Name Screen Shot][product-screenshot]

This is a GUI that functions as an AI chatbot and can act as the basis for an AI VTuber. It allows the user to provide input to it through either Twitch chat or through the microphone. Afterwards, it is processed through a LLM of the user's choice through the <a href="https://github.com/oobabooga/text-generation-webui">oobabooga text-generation-webui</a>'s API, and an audio response is generated using one of the two text-to-speech systems. Responses should be near real-time when there are a large number of users in Twitch chat due to the use of separate threads for generating the text and playing audio. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* <a href="https://flet.dev/">Flet</a>
* <a href="https://github.com/oobabooga/text-generation-webui">oobabooga text-generation-webui</a>
* <a href="https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/">Azure Speech SDK</a>
* <a href="https://github.com/coqui-ai/TTS">Coqui TTS</a> (<a href="https://arxiv.org/pdf/2106.06103">VITS model</a>)
* <a href="https://github.com/Uberi/speech_recognition">Uberi's SpeechRecognition Python Library</a> (<a href="https://github.com/openai/whisper">OpenAI Whisper model</a>)
* <a href="https://github.com/Teekeks/pyTwitchAPI">PyTwitchAPI</a>
* <a href="https://github.com/spatialaudio/python-sounddevice/">python-sounddevice</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites
* A GPU with CUDA support if using Coqui TTS (Download the necessary Pytorch version beforehand and follow the pip installation if not using CUDA)
* <a href="https://github.com/oobabooga/text-generation-webui">oobabooga text-generation-webui</a> with a language model to use
* (Optional) <a href="https://vb-audio.com/Voicemeeter/index.htm">Voicemeeter</a> for virtual audio cables
* (Optional) <a href="https://denchisoft.com/">VTube Studio</a> with the <a href="https://lualucky.itch.io/vts-desktop-audio-plugin">desktop audio plugin</a> installed and a Live2D model

### Installation

_Below is an example of how you can instruct your audience on installing and setting up your app. This template doesn't rely on any external dependencies or services._

1. Obtain an <a href="https://portal.azure.com/#home">Azure</a> subscription key for the Speech service under Cognitive Services.
2. Create a<a href="https://dev.twitch.tv/console/apps">Twitch application</a> with an ID and secret.
3. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
4. Install the requirements. It is recommended to use a conda or venv environment.
   For a conda environment, use the following command.
   ```sh
   conda env create -f environment.yaml
   ```
   For pip, use the following command.
   ```sh
   pip install -r requirements.txt
   ```
5. Start the oobabooga text-generation-webui with the --API command line argument.
6. Launch the program with the following command.
   ```js
   python gui_main.py
   ```
7. Open the settings by clicking the cog in the top right corner of the GUI and fill in the fields to be able to use the Azure and Twitch APIs.
8. Choose whether to use Coqui or Azure for text-to-speech, and select the correct audio input and output devices to use. (If you want to use this program with VTube Studio, connect the audio output to the Voicemeeter virtual input cable.)
9. Click the text box icon and fill in the prompt information to feed the language model when taking input.
10. You can now click the Twitch Connection button to connect to Twitch chat. The Conversation Mode button will enable speech-to-text, and the AI button will start sending requests to the oobabooga webui API to obtain outputs that will be fed into the text-to-speech system.
Optional: Launch VTube Studio and open the Live2D model that you will use. Set the audio output of Voicemeeter to its audio input. Set the mouth to move in the y-axis based on one of the parameters for audio volume. (WIP, more details to be added later)


<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage

Coming soon

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ ] Add Chat Logs and output to a file to use for subtitles
- [ ] Add a usage example
- [ ] Text input from the GUI
- [ ] More customization options in settings (?)
- [ ] Potentially implement usage of the superbooga extension through the text-generation-webui API (?)
- [ ] Japanese text-to-speech output (if there's any interest)

See the [open issues](https://github.com/Your-Cheese/AI_Chatbot/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
<!-- ## Contact


Project Link: [https://github.com/your_username/repo_name](https://github.com/your_username/repo_name) -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Inspired by [Neuro-sama](https://www.twitch.tv/vedal987)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Your-Cheese/AI_Chatbot.svg?style=for-the-badge
[contributors-url]: https://github.com/Your-Cheese/AI_Chatbot/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Your-Cheese/AI_Chatbot.svg?style=for-the-badge
[forks-url]: https://github.com/Your-Cheese/AI_Chatbot/network/members
[stars-shield]: https://img.shields.io/github/stars/Your-Cheese/AI_Chatbot.svg?style=for-the-badge
[stars-url]: https://github.com/Your-Cheese/AI_Chatbot/stargazers
[issues-shield]: https://img.shields.io/github/issues/Your-Cheese/AI_Chatbot.svg?style=for-the-badge
[issues-url]: https://github.com/Your-Cheese/AI_Chatbot/issues
[license-shield]: https://img.shields.io/github/license/Your-Cheese/AI_Chatbot.svg?style=for-the-badge
[license-url]: https://github.com/Your-Cheese/AI_Chatbot/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/david-z-3a2a7639/
[product-screenshot]: images/GUI_screenshot.png