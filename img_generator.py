"""Student Card Image Generator"""
import io
import random
from PIL import Image, ImageDraw, ImageFont


def generate_school_email(first_name: str, last_name: str, school_domain: str) -> str:
    """
    Generate random school email based on school domain
    
    Args:
        first_name: First name
        last_name: Last name
        school_domain: School domain (e.g., 'mit.edu', 'stanford.edu')
    
    Returns:
        str: Generated email address
    
    Example:
        generate_school_email('John', 'Doe', 'mit.edu') -> 'A2B4C6D8@MIT.EDU'
    """
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    username = ''.join(random.choice(chars) for _ in range(8))
    return f"{username}@{school_domain.upper()}"


def generate_student_id():
    """
    Generate random student ID (9 digits)
    
    Returns:
        str: 9-digit student ID starting with 9
    """
    return f"9{random.randint(10000000, 99999999)}"


def generate_image(first_name: str, last_name: str, school_id: str) -> bytes:
    """
    Generate fake student card image as PNG bytes
    
    Args:
        first_name: First name
        last_name: Last name
        school_id: School ID (used for identification on card)
    
    Returns:
        bytes: PNG image data
    """
    try:
        # Create blank white image (800x500)
        img = Image.new('RGB', (800, 500), color='white')
        draw = ImageDraw.Draw(img)
        
        # Try to load fonts, fallback to default if not available
        try:
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 48)
            font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
            font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        except:
            # Fallback to default font if fonts not available
            font_title = ImageFont.load_default()
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Generate student ID
        student_id = generate_student_id()
        
        # Get school name if possible
        try:
            import config
            school_name = "University"
            for key, school in config.SCHOOLS.items():
                if str(school['id']) == str(school_id):
                    school_name = school['name']
                    break
        except:
            school_name = "University"
        
        # Draw header background (blue banner)
        draw.rectangle([(0, 0), (800, 80)], fill='#1E407C')
        
        # Draw title
        draw.text((50, 20), "STUDENT ID CARD", fill='white', font=font_title)
        
        # Draw student information
        y_offset = 120
        
        # Full name
        draw.text((50, y_offset), "Name:", fill='#555', font=font_medium)
        draw.text((200, y_offset), f"{first_name} {last_name}", fill='#000', font=font_large)
        y_offset += 60
        
        # Student ID
        draw.text((50, y_offset), "Student ID:", fill='#555', font=font_medium)
        draw.text((200, y_offset), student_id, fill='#000', font=font_large)
        y_offset += 60
        
        # University name
        draw.text((50, y_offset), "University:", fill='#555', font=font_medium)
        # Truncate long names
        display_name = school_name[:35] + "..." if len(school_name) > 35 else school_name
        draw.text((200, y_offset), display_name, fill='#000', font=font_medium)
        y_offset += 60
        
        # Academic year
        draw.text((50, y_offset), "Academic Year:", fill='#555', font=font_medium)
        draw.text((200, y_offset), "2025-2026", fill='#000', font=font_medium)
        y_offset += 60
        
        # Status badge
        draw.text((50, y_offset), "Status:", fill='#555', font=font_medium)
        draw.rectangle([(200, y_offset - 5), (330, y_offset + 30)], fill='#e6fffa', outline='#007a5e')
        draw.text((210, y_offset), "ENROLLED", fill='#007a5e', font=font_medium)
        
        # Draw footer
        draw.text((50, 460), "Valid through: December 2026", fill='#888', font=font_small)
        
        # Add border
        draw.rectangle([(10, 10), (790, 490)], outline='#1E407C', width=3)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
        
    except Exception as e:
        raise Exception(f"Failed to generate image: {str(e)}")


if __name__ == '__main__':
    # Test code
    print("Testing Student Card Generator...")
    print("=" * 60)
    
    first_name = "John"
    last_name = "Smith"
    school_domain = "mit.edu"
    school_id = "1953"
    
    print(f"Name: {first_name} {last_name}")
    print(f"Student ID: {generate_student_id()}")
    print(f"Email: {generate_school_email(first_name, last_name, school_domain)}")
    print(f"School ID: {school_id}")
    print()
    
    try:
        # Generate image
        img_data = generate_image(first_name, last_name, school_id)
        
        # Save test image
        with open('test_student_card.png', 'wb') as f:
            f.write(img_data)
        
        print(f"✅ Image generated successfully!")
        print(f"✅ Size: {len(img_data) / 1024:.2f} KB")
        print(f"✅ Saved as: test_student_card.png")
        print()
        
        # Test multiple emails
        print("Testing email generation with different domains:")
        print("-" * 60)
        domains = ['mit.edu', 'stanford.edu', 'harvard.edu', 'caltech.edu']
        for domain in domains:
            email = generate_school_email(first_name, last_name, domain)
            print(f"  {domain:20s} -> {email}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
