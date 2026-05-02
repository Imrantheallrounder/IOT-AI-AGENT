# 🤖 IoT Agent - Voice-Controlled Smart Home Assistant

A powerful, voice-controlled IoT agent that uses wake word detection, natural language processing, and MQTT to control your smart home devices. Built with Python, featuring advanced AI capabilities and a robust device management system.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)

## 📚 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [🔧 Detailed Configuration Guide](#-detailed-configuration-guide)
- [🏠 Device Management](#-device-management)
- [💬 Voice Commands Examples](#-voice-commands-examples)
- [🛠️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [🔧 Development](#-development)
- [🤝 Contributing](#-contributing)

## ✨ Features

- 🎤 **Wake Word Detection** - Listen for custom wake words using Porcupine
- 🗣️ **Voice Recognition** - Convert speech to text using Google Speech Recognition
- 🧠 **AI-Powered Intent Recognition** - Understand user queries with Google Gemini AI
- 🏠 **Smart Home Control** - Control devices via MQTT with natural language
- 📱 **Device Management** - YAML-based device registry with full CRUD operations
- 🔊 **Audio Feedback** - Play chime sounds for user interaction
- 🔄 **Workflow Engine** - LlamaIndex-powered workflow management
- 🛡️ **Security** - Environment-based configuration and restricted query detection

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone access
- MQTT broker (e.g., Mosquitto)
- Google Gemini API key
- Porcupine wake word API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd IOT-AGENT
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Configure your devices**
   ```bash
   # Edit devices/devices.yaml with your smart home devices
   ```

6. **Start the agent**
   ```bash
   python main.py
   ```

## 🎯 How It Works

### 1. Wake Word Detection
The agent continuously listens for wake words like "Hey Jarvis", "Alexa", or custom keywords using Porcupine's advanced wake word detection.

### 2. Voice Recognition
Once activated, it captures your voice command and converts it to text using Google's Speech Recognition API.

### 3. Intent Classification
The AI analyzes your query to determine if you want to:
- **Control a device** (turn on lights, adjust thermostat)
- **Get information** (weather, time, general questions)
- **Restricted content** (blocked for safety)

### 4. Device Control
For device control, the AI extracts:
- **Floor** (ground, 1st, 2nd)
- **Room** (bedroom, kitchen, living room)
- **Device** (light, fan, AC)
- **Action** (on/off, adjust settings)

### 5. MQTT Communication
Commands are published to your MQTT broker for device control.

## 🏠 Device Management

### Adding Devices

```python
from devices.loader import add_device

add_device(
    device_id="bulb-001",
    device_name="Smart Bulb",
    device_description="LED smart bulb with dimming",
    device_location="bedroom_a",
    device_type="light",
    mqtt_topic="bedroom",
    capabilities=["on_off", "brightness", "color"]
)
```

### Device Configuration (YAML)

```yaml
devices:
  - device_id: bulb-001
    device_name: light bulb
    device_description: a light bulb that can be turned on or off
    device_location: bedroom_a
    device_type: light
    mqtt_topic: bedroom
    capabilities:
      - on_off
      - brightness
```

## 💬 Voice Commands Examples

### Device Control
- *"Turn on the bedroom light"*
- *"Switch off the kitchen fan"*
- *"Turn on the AC in the living room"*
- *"Turn off all lights on the first floor"*

### General Queries
- *"What's the weather today?"*
- *"What time is it?"*
- *"Tell me a joke"*

## 🛠️ Configuration

### Environment Variables (.env)
```bash
# AI Model
MODEL_NAME=gemini-2.5-flash
GOOGLE_API_KEY=your_gemini_api_key

# Wake Word Detection
WAKEWORD_API_KEY=your_porcupine_api_key

# MQTT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883
```

## 📁 Project Structure

```
IOT-AGENT/
├── main.py                 # Main application entry point
├── requirements.txt        # Python dependencies
├── .env                    # Environment configuration
├── devices/                # Device management system
│   ├── models.py          # Pydantic device models
│   ├── loader.py          # Device CRUD operations
│   ├── devices.yaml       # Device registry
│   └── example_usage.py   # Usage examples
├── wakeword/              # Wake word detection
│   └── wakeword_detection.py
├── prompts.py             # AI prompt templates
├── pydantic_structure.py  # Data models and events
├── transcribe.py          # Speech-to-text functionality
├── utility.py             # MQTT utilities
└── sounds.py              # Audio feedback
```

## 🔧 Development

### Running Tests
```bash
# Test device management
python devices/example_usage.py

# Test wake word detection
python wakeword/wakeword_detection.py
```

### Adding New Device Types
1. Update `pydantic_structure.py` with new device capabilities
2. Modify prompts in `prompts.py` to recognize new devices
3. Add device to `devices/devices.yaml`
4. Update MQTT topics in `utility.py` if needed

### Custom Wake Words
Edit `wakeword/wakeword_detection.py` to add your preferred wake words:
```python
keywords = ["jarvis", "alexa", "hey google", "your-custom-word"]
```
Available default keywords are:\nalexa, blueberry, hey google, pico clock, hey siri, computer, terminator, grapefruit, americano, hey barista, jarvis, porcupine, ok google, picovoice, grasshopper, bumblebee

Visit [Picovoice](https://picovoice.ai/) for generating custom wakeword model. And pass the model path as parameter in the code.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Porcupine](https://picovoice.ai/) for wake word detection
- [Google Gemini](https://ai.google.dev/) for AI capabilities
- [LlamaIndex](https://llamaindex.ai/) for workflow management
- [MQTT](https://mqtt.org/) for IoT communication

## Support

- **Issues**: [GitHub Issues](https://github.com/your-username/IOT-AGENT/issues)
- **Documentation**: Check the `docs/` folder for detailed guides
- **Community**: Join our Discord/Telegram for discussions


------------------------------------------------------------------------------------------


# 🔧 Detailed Configuration Guide

This guide will help you set up your IoT Agent with the necessary API keys and configuration.

## 📋 Prerequisites

Before you start, you'll need:

1. **Google Gemini API Key** - For AI-powered intent recognition
2. **Porcupine API Key** - For wake word detection
3. **MQTT Broker** - For device communication (e.g., Mosquitto)

## 🔑 Environment Variables

Create a `.env` file in your project root with the following variables:

```bash
# AI Model Configuration
MODEL_NAME=gemini-2.5-flash
GOOGLE_API_KEY=your_gemini_api_key_here

# Wake Word Detection (Porcupine)
WAKEWORD_API_KEY=your_porcupine_api_key_here

# MQTT Configuration
MQTT_BROKER=localhost
MQTT_PORT=1883

# Optional: Custom wake word keywords (comma-separated)
# WAKEWORD_KEYWORDS=jarvis,alexa,hey google,porcupine

# Optional: Audio feedback sound path
# CHIME_SOUND_PATH=/path/to/your/chime.mp3
```

## 🚀 Getting API Keys

### Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" in the top right
4. Create a new API key or use an existing one
5. Copy the key to your `.env` file

### Porcupine API Key

1. Visit [Picovoice Console](https://console.picovoice.ai/)
2. Sign up for a free account
3. Navigate to "Access Keys"
4. Create a new access key
5. Copy the key to your `.env` file

## 🏠 MQTT Broker Setup

### Option 1: Local Mosquitto (Recommended)

**Install Mosquitto:**

**macOS:**
```bash
brew install mosquitto
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install mosquitto mosquitto-clients
```

**Mac:**
```
brew install espeak-ng
```

**Windows:**
Download from [Mosquitto Downloads](https://mosquitto.org/download/)

**Start Mosquitto:**
```bash
# macOS/Linux
mosquitto

# Windows (in Command Prompt as Administrator)
mosquitto.exe
```

### Option 2: Cloud MQTT Services

- **HiveMQ**: Free tier available
- **CloudMQTT**: Free tier available
- **AWS IoT Core**: For advanced users

## 🎤 Audio Configuration

### Microphone Setup

Ensure your microphone is properly configured and accessible by Python:

```bash
# Test microphone access
python -c "import speech_recognition as sr; print('Microphone available:', sr.Microphone.list_microphone_names())"
```

### Custom Wake Words

Edit `wakeword/wakeword_detection.py` to customize wake words:

```python
keywords = ["jarvis", "alexa", "hey google", "your-custom-word"]
```

### Audio Feedback

To customize the chime sound:

1. Place your audio file in the project
2. Update the path in `sounds.py` or set `CHIME_SOUND_PATH` in `.env`

## 🏠 Device Configuration

### Adding Your First Device

1. **Edit `devices/devices.yaml`:**
```yaml
devices:
  - device_id: bulb-001
    device_name: light bulb
    device_description: a light bulb that can be turned on or off
    device_location: bedroom_a
    device_type: light
    mqtt_topic: bedroom
    capabilities:
      - on_off
      - brightness
```

2. **Or use the Python API:**
```python
from devices.loader import add_device

add_device(
    device_id="bulb-001",
    device_name="Smart Bulb",
    device_description="LED smart bulb with dimming",
    device_location="bedroom_a",
    device_type="light",
    mqtt_topic="bedroom",
    capabilities=["on_off", "brightness", "color"]
)
```

## 🔍 Testing Your Setup

### 1. Test Device Management
```bash
python devices/example_usage.py
```

### 2. Test Wake Word Detection
```bash
python wakeword/wakeword_detection.py
```

### 3. Test MQTT Connection
```bash
# Install mosquitto-clients if not already installed
mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"
```

### 4. Run the Full Application
```bash
python main.py
```

## 🛠️ Troubleshooting

### Common Issues

**"No module named 'pvporcupine'"**
```bash
pip install pvporcupine
```

**"Microphone not found"**
- Check microphone permissions
- Ensure microphone is not used by other applications
- Try different microphone index in `transcribe.py`

**"MQTT connection failed"**
- Ensure Mosquitto is running: `mosquitto`
- Check firewall settings
- Verify broker IP and port in `.env`

**"API key invalid"**
- Verify API keys are correct
- Check for extra spaces or characters
- Ensure API keys have proper permissions

### Debug Mode

Enable debug logging by modifying `main.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## 📞 Support

If you encounter issues:

1. Check the [README.md](README.md) for general information
2. Review this configuration guide
3. Check the troubleshooting section above
4. Open an issue on GitHub with detailed error messages

**Happy configuring! 🎉** 

---

**Made with ❤️ for smart homes everywhere**

*Turn your home into an intelligent living space with the power of voice and AI!* 