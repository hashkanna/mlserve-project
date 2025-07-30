#!/usr/bin/env python3
"""Create sample images for the demo."""

import base64
from io import BytesIO
try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

def create_sample_image_with_canvas():
    """Create sample images using HTML5 Canvas (JavaScript)."""
    # This will be handled by the JavaScript canvas code we already added
    return """
    Sample images are now created dynamically using HTML5 Canvas in the browser.
    
    The samples include:
    1. 🐕 Golden Retriever (Orange gradient)
    2. 🚗 Sports Car (Blue gradient)  
    3. ☕ Coffee Cup (Green gradient)
    
    Each image is generated as a 224x224 PNG with:
    - Gradient background
    - Checkerboard pattern overlay
    - Descriptive text
    - Emoji icon
    """

def create_simple_svg_samples():
    """Create simple SVG samples that definitely work."""
    samples = []
    
    # Sample 1: Dog
    svg1 = '''
    <svg width="224" height="224" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#FFB74D;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#FF8A65;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="224" height="224" fill="url(#grad1)" rx="12"/>
        <text x="112" y="90" text-anchor="middle" fill="white" font-size="20" font-family="Arial">Golden Retriever</text>
        <text x="112" y="140" text-anchor="middle" fill="white" font-size="48">🐕</text>
    </svg>
    '''
    
    # Sample 2: Car
    svg2 = '''
    <svg width="224" height="224" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad2" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#64B5F6;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#42A5F5;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="224" height="224" fill="url(#grad2)" rx="12"/>
        <text x="112" y="90" text-anchor="middle" fill="white" font-size="20" font-family="Arial">Sports Car</text>
        <text x="112" y="140" text-anchor="middle" fill="white" font-size="48">🚗</text>
    </svg>
    '''
    
    # Sample 3: Coffee
    svg3 = '''
    <svg width="224" height="224" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <linearGradient id="grad3" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:#8BC34A;stop-opacity:1" />
                <stop offset="100%" style="stop-color:#66BB6A;stop-opacity:1" />
            </linearGradient>
        </defs>
        <rect width="224" height="224" fill="url(#grad3)" rx="12"/>
        <text x="112" y="90" text-anchor="middle" fill="white" font-size="20" font-family="Arial">Coffee Cup</text>
        <text x="112" y="140" text-anchor="middle" fill="white" font-size="48">☕</text>
    </svg>
    '''
    
    # Convert to base64 data URLs
    samples = [
        ("Golden Retriever", f"data:image/svg+xml;base64,{base64.b64encode(svg1.encode()).decode()}"),
        ("Sports Car", f"data:image/svg+xml;base64,{base64.b64encode(svg2.encode()).decode()}"),
        ("Coffee Cup", f"data:image/svg+xml;base64,{base64.b64encode(svg3.encode()).decode()}")
    ]
    
    return samples

def main():
    print("Creating sample images for MLServe Demo...")
    
    if PIL_AVAILABLE:
        print("✅ PIL available - but using JavaScript Canvas for better browser compatibility")
    else:
        print("ℹ️  PIL not available - using JavaScript Canvas approach")
    
    print("\n" + create_sample_image_with_canvas())
    
    print("\n🔧 Alternative: SVG samples are also available if needed")
    samples = create_simple_svg_samples()
    for i, (name, data_url) in enumerate(samples, 1):
        print(f"   Sample {i}: {name} ({len(data_url)} chars)")

if __name__ == "__main__":
    main()