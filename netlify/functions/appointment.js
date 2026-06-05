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
    const requiredFields = ['name', 'email', 'phone', 'department', 'date', 'time'];
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

    // Validate phone number (basic validation)
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    if (!phoneRegex.test(data.phone.replace(/[\s\-\(\)]/g, ''))) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Invalid phone number format' }),
      };
    }

    // Validate date (should be in the future)
    const appointmentDate = new Date(data.date);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    if (appointmentDate < today) {
      return {
        statusCode: 400,
        headers,
        body: JSON.stringify({ error: 'Appointment date must be in the future' }),
      };
    }

    // Here you would typically:
    // 1. Save to database
    // 2. Send confirmation email
    // 3. Send notification to hospital staff
    
    // For now, we'll just log the appointment and return success
    console.log('New appointment booking:', {
      name: data.name,
      email: data.email,
      phone: data.phone,
      department: data.department,
      doctor: data.doctor || 'Not specified',
      date: data.date,
      time: data.time,
      message: data.message || 'No message',
      timestamp: new Date().toISOString()
    });

    // In a real implementation, you might want to:
    // - Send an email confirmation to the patient
    // - Send a notification to the hospital staff
    // - Store the appointment in a database
    // - Integrate with a calendar system

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        message: 'Appointment booked successfully! We will contact you soon to confirm your appointment.',
        appointmentId: `APT-${Date.now()}`, // Generate a simple appointment ID
      }),
    };

  } catch (error) {
    console.error('Error processing appointment:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Internal server error. Please try again later.' 
      }),
    };
  }
};
