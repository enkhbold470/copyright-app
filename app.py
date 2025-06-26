import os
import logging
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from PIL import Image, ImageDraw, ImageFont
import io
import tempfile
from werkzeug.utils import secure_filename
from config import config

# Configure logging
if config.ENV == 'production':
    logging.basicConfig(level=logging.INFO)
else:
    logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = config.UPLOAD_FOLDER
OUTPUT_FOLDER = config.OUTPUT_FOLDER

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def find_font():
    """Find available fonts that work on Linux servers"""
    font_paths = [
        # Common Linux fonts
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
        '/usr/share/fonts/TTF/DejaVuSans.ttf',
        '/System/Fonts/Helvetica.ttc',  # macOS
        '/System/Library/Fonts/Helvetica.ttc',  # macOS
        'C:/Windows/Fonts/arial.ttf',  # Windows
    ]
    
    for font_path in font_paths:
        if os.path.exists(font_path):
            return font_path
    return None

def add_copyright_to_image(image_path, copyright_text, opacity=128):
    """Add copyright text to image with transparency"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Create a transparent overlay
            overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Try to use a system font, fallback to default
            try:
                font_size = max(20, min(img.width, img.height) // 40)
                font_path = find_font()
                if font_path:
                    font = ImageFont.truetype(font_path, font_size)
                else:
                    font = ImageFont.load_default()
            except (OSError, IOError) as e:
                logger.warning(f"Could not load font: {e}. Using default.")
                font = ImageFont.load_default()
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), copyright_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Position text in bottom right corner with padding
            padding = 20
            x = img.width - text_width - padding
            y = img.height - text_height - padding
            
            # Add semi-transparent background for text
            bg_padding = 10
            draw.rectangle([
                x - bg_padding, 
                y - bg_padding, 
                x + text_width + bg_padding, 
                y + text_height + bg_padding
            ], fill=(0, 0, 0, opacity // 2))
            
            # Draw copyright text
            draw.text((x, y), copyright_text, font=font, fill=(255, 255, 255, opacity))
            
            # Composite the overlay onto the original image
            result = Image.alpha_composite(img, overlay)
            
            # Convert back to RGB if original was not RGBA
            if image_path.lower().endswith(('.jpg', '.jpeg')):
                result = result.convert('RGB')
            
            return result
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    copyright_text = request.form.get('copyright_text', '© Your Copyright')
    opacity = int(request.form.get('opacity', 128))
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1]) as temp_file:
            file.save(temp_file.name)
            
            try:
                # Process image
                result_image = add_copyright_to_image(temp_file.name, copyright_text, opacity)
                
                # Save result to memory buffer
                img_buffer = io.BytesIO()
                format_type = 'PNG' if filename.lower().endswith('.png') else 'JPEG'
                result_image.save(img_buffer, format=format_type, quality=95)
                img_buffer.seek(0)
                
                # Clean up temp file
                os.unlink(temp_file.name)
                
                # Return the processed image
                output_filename = f"copyright_{filename}"
                logger.info(f"Successfully processed {filename}")
                return send_file(
                    img_buffer,
                    as_attachment=True,
                    download_name=output_filename,
                    mimetype=f'image/{format_type.lower()}'
                )
                
            except Exception as e:
                # Clean up temp file
                if os.path.exists(temp_file.name):
                    os.unlink(temp_file.name)
                logger.error(f'Error processing image: {str(e)}')
                flash(f'Error processing image: {str(e)}', 'error')
                return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload PNG, JPG, or JPEG files only.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    flash("File is too large. Maximum size is 16MB.", 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    logger.error(f"Internal server error: {e}")
    flash("Something went wrong. Please try again.", 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    logger.info(f"Starting app in {config.ENV} mode")
    logger.info(f"Debug mode: {config.DEBUG}")
    logger.info(f"Host: {config.HOST}, Port: {config.PORT}")
    
    app.run(debug=config.DEBUG, host=config.HOST, port=config.PORT)
