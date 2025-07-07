exports.handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: '',
    };
  }

  // Only allow POST requests
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' }),
    };
  }

  try {
    // Parse the form data
    const data = JSON.parse(event.body);
    
    // Validate required fields
    if (!data.email) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          error: 'Email is required' 
        }),
      };
    }

    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid email format' }),
      };
    }

    // Check for common disposable email domains (optional security measure)
    const disposableEmailDomains = [
      '10minutemail.com',
      'tempmail.org',
      'guerrillamail.com',
      'mailinator.com'
    ];
    
    const emailDomain = data.email.split('@')[1].toLowerCase();
    if (disposableEmailDomains.includes(emailDomain)) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Please use a valid email address' }),
      };
    }

    // Here you would typically:
    // 1. Check if email already exists in newsletter list
    // 2. Add to newsletter database/service (like Mailchimp, SendGrid, etc.)
    // 3. Send welcome email
    
    // For now, we'll just log the newsletter subscription and return success
    console.log('New newsletter subscription:', {
      email: data.email,
      timestamp: new Date().toISOString(),
      userAgent: event.headers['user-agent'] || 'Unknown',
      ip: event.headers['x-forwarded-for'] || event.headers['x-nf-client-connection-ip'] || 'Unknown'
    });

    // In a real implementation, you might want to:
    // - Add the email to a newsletter service like Mailchimp or SendGrid
    // - Send a welcome email with health tips
    // - Store the subscription in a database
    // - Implement double opt-in for GDPR compliance

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Thank you for subscribing to our newsletter! You will receive health tips and updates from Arvindu Hospitals.',
      }),
    };

  } catch (error) {
    console.error('Error processing newsletter subscription:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error. Please try again later.' 
      }),
    };
  }
};
