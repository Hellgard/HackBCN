# SimplifAI for HackBCN

Welcome to SimplifAI, a cutting-edge project developed for the HackBCN event. SimplifAI is designed to revolutionize the way we interact with AI, focusing on natural language processing and speech recognition to create a more intuitive and human-like interaction.

## Features

- **Speech Recognition**: Utilizes advanced models to accurately transcribe spoken words into text.
- **Natural Language Understanding**: Processes and understands the user's intent from the transcribed text.
- **Emotion Recognition**: Analyzes the user's voice to detect emotions, enhancing the interaction experience.
- **Responsive AI**: Generates appropriate responses based on the user's input and emotional state.
- **Multilingual Support**: Supports multiple languages, making it accessible to a wider audience.

## Technology Stack

- Python 3.10.11
- NumPy
- Transformers
- SpeechRecognition
- OpenAI
- Pygame
- gTTS (Google Text-to-Speech)

## Project Structure

- `software/`: Main directory containing the Python scripts and models.
    - `app.py`: The main application script.
    - `Class/`: Contains classes for audio data, robot behavior, and speech recognition.
    - `Config/`: Configuration files and utilities.
    - `GenerateResponse.py`: Handles response generation using OpenAI.
    - `Listener.py`, `Loop.py`, `TurnOff.py`: Core functionalities for listening, processing, and turning off the robot.
- `Chrome_extension/`: Contains the files for the Chrome extension part of the project.
- `README.md`: This file, providing an overview of the project.
- `requirements.txt`: Lists all the Python dependencies.

## Setup

1. Clone the repository to your local machine.
2. Install Python 3.10.11 if not already installed.
3. Navigate to the `software/` directory.
4. Install the required Python packages: `pip install -r requirements.txt`.
5. Run `main.py` to start the application: `python main.py`.

## Contributing

We welcome contributions! If you have suggestions or want to improve SimplifAI, please feel free to fork the repository, make changes, and submit a pull request.

## Authors

- Erwan - Initial work and development for HackBCN.
- Julien - Initial work and development for HackBCN.
- Thomas - Initial work and development for HackBCN.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- HackBCN organizers and community for the opportunity to develop this project.
- Open-source projects and libraries that made this project possible.

Thank you for checking out SimplifAI. We hope you find it as exciting as we do!