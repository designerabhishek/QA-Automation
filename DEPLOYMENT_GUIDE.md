# Deployment Guide - Fixing 502 Bad Gateway Error

## Current Issues Identified

The 502 Bad Gateway error on `https://qa-automation-nash.onrender.com/` is likely caused by:

1. **Selenium/Chrome Dependencies**: The app uses Selenium which requires Chrome/Chromium in the container
2. **Resource Limits**: Free tier on Render has memory and CPU limitations
3. **Port Configuration**: Mismatched port settings between Dockerfile and Procfile
4. **Health Check Failures**: The health check might be timing out

## Solutions Implemented

### 1. Fixed Configuration Files

- **Procfile**: Updated to use proper port binding and timeout settings
- **Dockerfile**: Improved health check and container configuration
- **render.yaml**: Added better environment variables and deployment settings

### 2. Added Error Handling

- Added logging to `app.py` for better debugging
- Added health check endpoint at `/health`
- Improved error handling in audit functions

### 3. Created Alternative Versions

- `app_simple.py`: Simplified version without Selenium dependencies
- `test_deployment.py`: Basic test script to verify Flask works

## Deployment Steps

### Option 1: Deploy with Current Fixes

1. **Commit and push your changes**:
   ```bash
   git add .
   git commit -m "Fix 502 Bad Gateway - update deployment config"
   git push
   ```

2. **Monitor Render logs**:
   - Go to your Render dashboard
   - Check the deployment logs for any errors
   - Look for Chrome/Selenium related errors

### Option 2: Test with Simplified Version

If the main app still fails, try deploying the simplified version:

1. **Temporarily rename files**:
   ```bash
   mv app.py app_original.py
   mv app_simple.py app.py
   ```

2. **Update requirements.txt** (remove Selenium dependencies):
   ```txt
   Flask==2.3.3
   gunicorn==21.2.0
   requests==2.31.0
   ```

3. **Deploy and test**:
   ```bash
   git add .
   git commit -m "Test simplified version without Selenium"
   git push
   ```

### Option 3: Use Alternative Deployment

If Render continues to have issues, consider:

1. **Heroku**: Better support for Selenium apps
2. **Railway**: Good free tier for Python apps
3. **DigitalOcean App Platform**: More reliable but paid

## Troubleshooting Steps

### Check Render Logs

1. Go to your Render dashboard
2. Click on your service
3. Go to "Logs" tab
4. Look for:
   - Chrome/Chromium installation errors
   - Memory limit exceeded errors
   - Port binding errors
   - Health check failures

### Test Locally

1. **Test with Docker**:
   ```bash
   docker build -t site-audit .
   docker run -p 10000:10000 site-audit
   ```

2. **Test without Selenium**:
   ```bash
   python app_simple.py
   ```

### Common Error Patterns

1. **"Chrome binary not found"**: Chrome installation issue
2. **"Memory limit exceeded"**: Free tier limitation
3. **"Port already in use"**: Port configuration issue
4. **"Health check failed"**: App not starting properly

## Next Steps

1. **Deploy the current fixes** and monitor logs
2. **If still failing**, try the simplified version
3. **Consider upgrading** to a paid Render plan for better resources
4. **Alternative**: Use a different platform that better supports Selenium

## Monitoring

After deployment, check these endpoints:

- `https://qa-automation-nash.onrender.com/` - Main page
- `https://qa-automation-nash.onrender.com/health` - Health check
- `https://qa-automation-nash.onrender.com/test` - Simple test (if using test_deployment.py)

## Rollback Plan

If the simplified version works, you can:

1. Keep the simplified version for basic functionality
2. Work on optimizing the Selenium version for production
3. Consider using a headless browser service instead of local Chrome
