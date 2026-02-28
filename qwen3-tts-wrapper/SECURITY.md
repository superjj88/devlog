# Security Documentation

This document describes the security measures implemented in the Qwen3-TTS wrapper.

## Overview

The Qwen3-TTS wrapper implements multiple layers of security to protect against common vulnerabilities and attacks.

## Security Features

### 1. Configuration Management

- **Environment Variables**: All sensitive configuration is loaded from environment variables via `.env` file
- **Configuration Template**: `.env.example` provides a template for required variables
- **No Hardcoded Secrets**: No hardcoded passwords, API keys, or tokens

### 2. Input Validation

- **Text Validation**: User input is validated for length, content, and format
- **Sanitization**: Input is sanitized to prevent injection attacks
- **Command Validation**: Socket commands are validated before execution

### 3. Rate Limiting

- **Sliding Window Algorithm**: Prevents abuse by limiting requests per time window
- **Per-Client Tracking**: Rate limits are tracked per client identifier
- **Configurable Limits**: Default is 60 requests per minute

### 4. Temporary File Security

- **Secure Permissions**: Temporary files are created with owner-only read/write permissions
- **Automatic Cleanup**: Temporary files are tracked and cleaned up on exit
- **No Predictable Names**: Uses system-provided secure temporary file generation

### 5. Unix Socket Security

- **File Permissions**: Socket file permissions can be configured via environment
- **Access Control**: Only authorized processes can connect to the socket
- **Connection Validation**: All incoming connections are validated

### 6. Logging

- **Security Events**: Security-relevant events are logged separately
- **Structured Logging**: Logs are formatted as JSON for easy parsing
- **Sensitive Data Redaction**: Sensitive data is automatically redacted from logs

## Security Best Practices

### For Developers

1. **Never commit `.env` files** - They contain sensitive configuration
2. **Use environment variables** for all sensitive data
3. **Validate all user input** before processing
4. **Log security events** for audit purposes

### For Operators

1. **Set appropriate file permissions** on the socket file
2. **Monitor logs** for suspicious activity
3. **Configure rate limits** based on your needs
4. **Regularly rotate credentials** and API keys

## Threat Model

### Potential Threats

1. **Input Injection**: Malicious input could cause unexpected behavior
   - **Mitigation**: Input validation and sanitization

2. **Denial of Service**: Excessive requests could exhaust resources
   - **Mitigation**: Rate limiting

3. **Information Disclosure**: Sensitive data could be exposed in logs
   - **Mitigation**: Automatic redaction of sensitive data

4. **Unauthorized Access**: Unauthorized processes could connect to the socket
   - **Mitigation**: File permissions and connection validation

### Assumptions

1. The underlying system is secure
2. Users have appropriate permissions
3. Network connections (if any) are secured

## Security Contact

For security issues, please contact the development team.

## License

This project follows the same license as the main Qwen3-TTS wrapper.
