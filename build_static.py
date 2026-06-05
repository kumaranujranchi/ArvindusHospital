import os
from app import create_app

def main():
    # Set config to testing
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for static page generation

    routes = {
        '/': 'index.html',
        '/about': 'about.html',
        '/departments': 'departments.html',
        '/doctors': 'doctors.html',
        '/patient-care': 'patient_care.html',
        '/testimonials': 'testimonials.html',
        '/blog': 'blog.html',
        '/careers': 'careers.html',
        '/news': 'news.html',
        '/appointment': 'appointment.html',
        '/contact': 'contact.html',
    }

    client = app.test_client()

    for url, filename in routes.items():
        print(f"Rendering {url} -> {filename}...")
        response = client.get(url)
        if response.status_code == 200:
            # Add a small replacement to fix any potential relative URLs if needed,
            # but Flask templates use url_for('static', ...) which returns /static/...
            # which works perfectly on Netlify root deployment.
            html_content = response.get_data(as_text=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print("  Done!")
        else:
            print(f"  Error: {response.status_code}")

    # Generate 404.html and 500.html
    print("Generating 404.html and 500.html...")
    with app.test_request_context():
        from flask import render_template
        from forms import NewsletterForm
        
        # 404
        html_404 = render_template('404.html', newsletter_form=NewsletterForm())
        with open('404.html', 'w', encoding='utf-8') as f:
            f.write(html_404)
        
        # 500
        html_500 = render_template('500.html', newsletter_form=NewsletterForm())
        with open('500.html', 'w', encoding='utf-8') as f:
            f.write(html_500)
    
    print("Finished generating all static pages!")

if __name__ == '__main__':
    main()
