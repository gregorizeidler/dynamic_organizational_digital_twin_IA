# 🛠️ Setup Instructions

## Environment Configuration

Create a `.env` file in the project root with the following content:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4-1106-preview

# Organization Configuration  
ORGANIZATION_NAME=TechCorp AI Startup

# Simulation Configuration
SIMULATION_SPEED=normal
DEBUG_MODE=False
```

## Step-by-Step Setup

### 1. Get OpenAI API Key
1. Go to [OpenAI API Keys](https://platform.openai.com/api-keys)
2. Create a new API key
3. Copy the key for use in the next step

### 2. Configure Environment
1. Create a `.env` file in the project root directory
2. Add your OpenAI API key to the file:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```
3. Customize other settings as needed

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

## Configuration Options

### OpenAI Models
- `gpt-4-1106-preview` (Recommended) - Latest GPT-4 with enhanced capabilities
- `gpt-4` - Standard GPT-4 model
- `gpt-3.5-turbo` - Faster and cheaper alternative

### Simulation Speed
- `slow` - 1 day every 5 seconds
- `normal` - 1 day every 2 seconds  
- `fast` - 1 day every 1 second
- `turbo` - 1 day every 0.5 seconds

### Organization Names
You can customize the organization name to create different company scenarios:
- `TechCorp AI Startup`
- `Innovation Labs Inc`
- `Digital Dynamics Ltd`
- `Future Tech Solutions`

## Troubleshooting

### Common Issues

**ImportError: No module named 'agents'**
- Make sure you're running from the project root directory
- Verify all files are in their correct directories

**OpenAI API Error**
- Check that your API key is valid and has sufficient credits
- Verify the model name is correct
- Ensure you have access to GPT-4 (may require paid plan)

**Streamlit Connection Error**
- Check that port 8501 is available
- Try running on a different port: `streamlit run app.py --server.port 8502`

### File Structure Verification
Your project should look like this:
```
organizational-digital-twin/
├── agents/
│   ├── __init__.py
│   ├── base_agent.py
│   ├── ceo_agent.py
│   ├── cfo_agent.py
│   ├── cto_agent.py
│   ├── cmo_agent.py
│   └── hr_agent.py
├── core/
│   ├── __init__.py
│   ├── communication_system.py
│   └── organizational_simulator.py
├── app.py
├── config.py
├── requirements.txt
├── .env
└── README.md
```

## Security Notes

- ⚠️ Never commit your `.env` file to version control
- 🔐 Keep your OpenAI API key secure and don't share it
- 💰 Monitor your OpenAI usage to avoid unexpected charges
- 🛡️ Use environment variables for sensitive configuration

## Performance Tips

- Start with shorter simulation runs to test the system
- Use GPT-3.5-turbo for development/testing to reduce costs
- Monitor API usage and set up billing alerts
- Use manual simulation mode for debugging 