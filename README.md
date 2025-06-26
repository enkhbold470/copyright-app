# Copyright Watermark Tool

Well, this is basically a simple web app that adds copyright watermarks to your images. You know how you need to protect your photos? This does that for you.
<img width="1692" alt="image" src="https://github.com/user-attachments/assets/c0977361-23a7-4dda-be25-29408a0d70c8" />

## What it does

- Works with PNG, JPG, and JPEG files
- Lets you type whatever copyright text you want
- You can make the watermark more or less see-through
- Has a clean interface that's kinda like Apple's design
- Just drag and drop your files
- Downloads the watermarked image automatically
- Works on your phone too

## How to get it running

You'll need Python 3.12 and the uv package manager. That's it.

1. Download or clone this thing to your computer
2. Go to the folder:
   ```bash
   cd copyright-app
   ```
3. Install the stuff it needs:
   ```bash
   uv sync
   ```

## How to use it

For development (debugging mode):
```bash
# Copy the example environment file
cp env.example .env

# Start the app
uv run python main.py
```

For production:
```bash
# Set up your environment file
echo "ENV=production" > .env
echo "SECRET_KEY=your-super-secret-key-here" >> .env
echo "DEBUG=false" >> .env

# Run it
uv run python main.py
```

Then just go to `http://localhost:8080` in your browser.

1. Upload an image (PNG, JPG, or JPEG)
2. Type your copyright text (it starts with "© 2024 Your Name")
3. Move the opacity slider to make it more or less transparent
4. Click "Add Copyright & Download"

That's literally it.

## Environment settings

The app uses a `.env` file for configuration. Copy `env.example` to `.env` and change what you need:

```
ENV=development          # or production
SECRET_KEY=your-key-here
HOST=0.0.0.0
PORT=8080
DEBUG=true              # false for production
```

## How it actually works

The app puts your copyright text in the bottom-right corner of your images. It adds a semi-transparent background so you can actually read the text. The original image quality stays good.

Your processed images get "copyright_" added to the front of the filename.

## Deploying to a server

This thing runs on basically any Linux server. It automatically finds fonts that work on different systems. If you're running it in production:

1. Set `ENV=production` in your `.env` file
2. Change the `SECRET_KEY` to something random
3. Set `DEBUG=false`
4. Make sure your server has the required fonts (most Linux servers do)

Common deployment commands:
```bash
# For systemd service
sudo cp your-service-file.service /etc/systemd/system/
sudo systemctl enable your-service-file
sudo systemctl start your-service-file

# Or just run it directly
nohup uv run python main.py &
```

## What's inside

```
copyright-app/
├── app.py              # Main Flask app
├── main.py             # Entry point
├── config.py           # Configuration handler
├── templates/
│   └── index.html     # The web interface
├── env.example        # Environment file template
├── pyproject.toml     # Dependencies
└── LICENSE            # MIT License
```

## Making changes

### Watermark position
You can move where the copyright appears by editing the `add_copyright_to_image()` function in `app.py`:

```python
# Change these numbers to move it around
padding = 20
x = img.width - text_width - padding  # right side
y = img.height - text_height - padding  # bottom
```

### The look and feel
All the styling is in `templates/index.html`. It uses Apple's system fonts and has that clean, modern vibe.

## Security stuff

- Files can't be bigger than 16MB
- Only PNG, JPG, and JPEG files work
- Everything gets processed in memory
- Temporary files get cleaned up automatically
- Make sure you change the secret key if you're putting this on the internet

## License

MIT License. Do whatever you want with it.

## Requirements

- Flask: The web framework
- Pillow: For image processing
- Python 3.12 or newer

That's really all there is to it. Simple tool for a simple job.
