"""Student Card Image Generator - HTML Screenshot Version"""
import io
import random
from datetime import datetime


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
    Generate random student ID (9 digits starting with 9)
    
    Returns:
        str: 9-digit student ID
    """
    return f"9{random.randint(10000000, 99999999)}"


def generate_html(first_name: str, last_name: str, school_name: str, school_id: str) -> str:
    """
    Generate Student Portal HTML page
    
    Args:
        first_name: First name
        last_name: Last name
        school_name: University name
        school_id: School ID
    
    Returns:
        str: HTML content
    """
    student_id = generate_student_id()
    full_name = f"{first_name} {last_name}"
    current_date = datetime.now().strftime('%m/%d/%Y, %I:%M:%S %p')
    
    # Random major selection
    majors = [
        'Computer Science (BS)',
        'Software Engineering (BS)',
        'Information Sciences and Technology (BS)',
        'Data Science (BS)',
        'Electrical Engineering (BS)',
        'Mechanical Engineering (BS)',
        'Business Administration (BS)',
        'Psychology (BA)',
        'Biology (BS)',
        'Mathematics (BS)'
    ]
    major = random.choice(majors)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Student Portal - My Class Schedule</title>
    <style>
        :root {{
            --primary-blue: #1E407C;
            --light-blue: #96BEE6;
            --bg-gray: #f4f4f4;
            --text-color: #333;
        }}

        body {{
            font-family: "Roboto", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #e0e0e0;
            margin: 0;
            padding: 20px;
            color: var(--text-color);
            display: flex;
            justify-content: center;
        }}

        .viewport {{
            width: 100%;
            max-width: 1100px;
            background-color: #fff;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            min-height: 800px;
            display: flex;
            flex-direction: column;
        }}

        .header {{
            background-color: var(--primary-blue);
            color: white;
            padding: 0 20px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 15px;
        }}

        .logo {{
            font-family: "Georgia", serif;
            font-size: 20px;
            font-weight: bold;
            letter-spacing: 1px;
            border-right: 1px solid rgba(255,255,255,0.3);
            padding-right: 15px;
        }}

        .system-name {{
            font-size: 18px;
            font-weight: 300;
        }}

        .user-menu {{
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}

        .nav-bar {{
            background-color: #f8f8f8;
            border-bottom: 1px solid #ddd;
            padding: 10px 20px;
            font-size: 13px;
            color: #666;
            display: flex;
            gap: 20px;
        }}
        
        .nav-item {{ 
            cursor: pointer; 
        }}
        
        .nav-item.active {{ 
            color: var(--primary-blue); 
            font-weight: bold; 
            border-bottom: 2px solid var(--primary-blue); 
            padding-bottom: 8px; 
        }}

        .content {{
            padding: 30px;
            flex: 1;
        }}

        .page-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }}

        .page-title {{
            font-size: 24px;
            color: var(--primary-blue);
            margin: 0;
        }}

        .term-selector {{
            background: #fff;
            border: 1px solid #ccc;
            padding: 5px 10px;
            border-radius: 4px;
            font-size: 14px;
            color: #333;
            font-weight: bold;
        }}

        .student-card {{
            background: #fcfcfc;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin-bottom: 25px;
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            font-size: 13px;
        }}
        
        .info-label {{ 
            color: #777; 
            font-size: 11px; 
            text-transform: uppercase; 
            margin-bottom: 4px; 
        }}
        
        .info-val {{ 
            font-weight: bold; 
            color: #333; 
            font-size: 14px; 
        }}
        
        .status-badge {{
            background-color: #e6fffa; 
            color: #007a5e;
            padding: 4px 8px; 
            border-radius: 4px; 
            font-weight: bold; 
            border: 1px solid #b2f5ea;
        }}

        .schedule-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}

        .schedule-table th {{
            text-align: left;
            padding: 12px;
            background-color: #f0f0f0;
            border-bottom: 2px solid #ccc;
            color: #555;
        }}

        .schedule-table td {{
            padding: 15px 12px;
            border-bottom: 1px solid #eee;
        }}

        .course-code {{ 
            font-weight: bold; 
            color: var(--primary-blue); 
        }}
        
        .course-title {{ 
            font-weight: 500; 
        }}

        .footer {{
            margin-top: 50px; 
            border-top: 1px solid #ddd; 
            padding-top: 10px; 
            font-size: 11px; 
            color: #888; 
            text-align: center;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .viewport {{ box-shadow: none; max-width: 100%; min-height: auto; }}
            .nav-bar {{ display: none; }}
            @page {{ margin: 1cm; size: landscape; }}
        }}
    </style>
</head>
<body>

<div class="viewport">
    <div class="header">
        <div class="brand">
            <div class="logo">University Portal</div>
            <div class="system-name">Student Information System</div>
        </div>
        <div class="user-menu">
            <span>Welcome, <strong>{full_name}</strong></span>
            <span>|</span>
            <span>Sign Out</span>
        </div>
    </div>

    <div class="nav-bar">
        <div class="nav-item">Student Home</div>
        <div class="nav-item active">My Class Schedule</div>
        <div class="nav-item">Academics</div>
        <div class="nav-item">Finances</div>
        <div class="nav-item">Campus Life</div>
    </div>

    <div class="content">
        <div class="page-header">
            <h1 class="page-title">My Class Schedule</h1>
            <div class="term-selector">
                Term: <strong>Fall 2025</strong> (Aug 25 - Dec 12)
            </div>
        </div>

        <div class="student-card">
            <div>
                <div class="info-label">Student Name</div>
                <div class="info-val">{full_name}</div>
            </div>
            <div>
                <div class="info-label">Student ID</div>
                <div class="info-val">{student_id}</div>
            </div>
            <div>
                <div class="info-label">Academic Program</div>
                <div class="info-val">{major}</div>
            </div>
            <div>
                <div class="info-label">Enrollment Status</div>
                <div class="status-badge">✅ ENROLLED</div>
            </div>
        </div>

        <div style="margin-bottom: 10px; font-size: 12px; color: #666; text-align: right;">
            University: <strong>{school_name}</strong> | School ID: <strong>{school_id}</strong><br>
            Data retrieved: <span>{current_date}</span>
        </div>

        <table class="schedule-table">
            <thead>
                <tr>
                    <th width="10%">Class Nbr</th>
                    <th width="15%">Course</th>
                    <th width="35%">Title</th>
                    <th width="20%">Days & Times</th>
                    <th width="10%">Room</th>
                    <th width="10%">Units</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>14920</td>
                    <td class="course-code">CMPSC 465</td>
                    <td class="course-title">Data Structures and Algorithms</td>
                    <td>MoWeFr 10:10AM - 11:00AM</td>
                    <td>Willard 062</td>
                    <td>3.00</td>
                </tr>
                <tr>
                    <td>18233</td>
                    <td class="course-code">MATH 230</td>
                    <td class="course-title">Calculus and Vector Analysis</td>
                    <td>TuTh 1:35PM - 2:50PM</td>
                    <td>Thomas 102</td>
                    <td>4.00</td>
                </tr>
                <tr>
                    <td>20491</td>
                    <td class="course-code">CMPSC 473</td>
                    <td class="course-title">Operating Systems Design</td>
                    <td>MoWe 2:30PM - 3:45PM</td>
                    <td>Westgate E201</td>
                    <td>3.00</td>
                </tr>
                <tr>
                    <td>11029</td>
                    <td class="course-code">ENGL 202C</td>
                    <td class="course-title">Technical Writing</td>
                    <td>Fr 1:25PM - 2:15PM</td>
                    <td>Boucke 304</td>
                    <td>3.00</td>
                </tr>
                <tr>
                    <td>15502</td>
                    <td class="course-code">STAT 318</td>
                    <td class="course-title">Elementary Probability</td>
                    <td>TuTh 9:05AM - 10:20AM</td>
                    <td>Osmond 112</td>
                    <td>3.00</td>
                </tr>
            </tbody>
        </table>

        <div class="footer">
            &copy; 2025 {school_name}. All rights reserved.<br>
            Student Information System - Verification ID: {school_id}
        </div>
    </div>
</div>

</body>
</html>
"""
    
    return html


def generate_image(first_name: str, last_name: str, school_id: str) -> bytes:
    """
    Generate Student Portal screenshot as PNG
    
    Args:
        first_name: First name
        last_name: Last name
        school_id: School ID (used to lookup school name from config)
    
    Returns:
        bytes: PNG image data
    """
    try:
        from playwright.sync_api import sync_playwright
        
        # Try to get school name from config
        try:
            import config
            # Find school by ID
            school_name = "University"
            for key, school in config.SCHOOLS.items():
                if str(school['id']) == str(school_id):
                    school_name = school['name']
                    break
        except:
            school_name = "University"
        
        # Generate HTML
        html_content = generate_html(first_name, last_name, school_name, school_id)
        
        # Use Playwright to take screenshot
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1200, 'height': 900})
            page.set_content(html_content, wait_until='load')
            page.wait_for_timeout(500)  # Wait for styles to load
            screenshot_bytes = page.screenshot(type='png', full_page=True)
            browser.close()
        
        return screenshot_bytes
        
    except ImportError:
        raise Exception("Playwright not installed. Run: pip install playwright && playwright install chromium")
    except Exception as e:
        raise Exception(f"Failed to generate image: {str(e)}")


if __name__ == '__main__':
    # Test code
    print("Testing Student Card Generator (HTML Version)...")
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
        with open('test_student_portal.png', 'wb') as f:
            f.write(img_data)
        
        print(f"✅ Image generated successfully!")
        print(f"✅ Size: {len(img_data) / 1024:.2f} KB")
        print(f"✅ Saved as: test_student_portal.png")
        print()
        
        # Test email generation
        print("Testing email generation with different domains:")
        print("-" * 60)
        domains = ['mit.edu', 'stanford.edu', 'harvard.edu', 'caltech.edu']
        for domain in domains:
            email = generate_school_email(first_name, last_name, domain)
            print(f"  {domain:20s} -> {email}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
