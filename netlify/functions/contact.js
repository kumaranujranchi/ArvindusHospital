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
    const requiredFields = ['name', 'email', 'subject', 'message'];
    const missingFields = requiredFields.filter(field => !data[field]);
    
    if (missingFields.length > 0) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ 
          error: 'Missing required fields', 
          missingFields 
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

    // Validate field lengths
    if (data.name.length < 2 || data.name.length > 100) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Name must be between 2 and 100 characters' }),
      };
    }

    if (data.subject.length < 2 || data.subject.length > 200) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Subject must be between 2 and 200 characters' }),
      };
    }

    if (data.message.length < 10 || data.message.length > 1000) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Message must be between 10 and 1000 characters' }),
      };
    }

    // Here you would typically:
    // 1. Save to database
    // 2. Send email to hospital staff
    // 3. Send confirmation email to user
    
    // For now, we'll just log the contact form submission and return success
    console.log('New contact form submission:', {
      name: data.name,
      email: data.email,
      subject: data.subject,
      message: data.message,
      timestamp: new Date().toISOString(),
      userAgent: event.headers['user-agent'] || 'Unknown',
      ip: event.headers['x-forwarded-for'] || event.headers['x-nf-client-connection-ip'] || 'Unknown'
    });

    // In a real implementation, you might want to:
    // - Send an email to the hospital contact team
    // - Send a confirmation email to the user
    // - Store the message in a database or CRM system
    // - Integrate with a ticketing system

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Thank you for contacting us! We will get back to you within 24 hours.',
        messageId: `MSG-${Date.now()}`, // Generate a simple message ID
      }),
    };

  } catch (error) {
    console.error('Error processing contact form:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error. Please try again later.' 
      }),
    };
  }
};
