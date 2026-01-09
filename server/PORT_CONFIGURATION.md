# Web Server Port Configuration

The AMS2 Race Results Web Server can be configured to run on any port and bind to any network interface.

## Default Configuration

- **Port**: 5000
- **Host**: 0.0.0.0 (all interfaces)
- **URL**: http://localhost:5000

## Running on Different Ports

### Linux/Mac

```bash
# Run on default port 5000
./run.sh

# Run on port 8000
./run.sh --port 8000
# or
./run.sh -p 8000

# Run on port 3000 with debug mode
./run.sh -p 3000 --debug

# Listen only on localhost (127.0.0.1)
./run.sh --host 127.0.0.1

# Run on port 8080, localhost only, with debug
./run.sh --port 8080 --host 127.0.0.1 --debug
```

### Windows

```bash
# Run on default port 5000
run.bat

# Run on port 8000
run.bat --port 8000
# or
run.bat -p 8000

# Run on port 3000 with debug mode
run.bat -p 3000 --debug

# Listen only on localhost (127.0.0.1)
run.bat --host 127.0.0.1

# Run on port 8080, localhost only, with debug
run.bat --port 8080 --host 127.0.0.1 --debug
```

## Direct Python Execution

You can also run the app directly with Python:

```bash
# Default port
python3 app.py

# Specify port
python3 app.py --port 8000

# Specify host and port
python3 app.py --host 127.0.0.1 --port 8000

# Enable debug mode
python3 app.py --port 5000 --debug
```

## Command-Line Arguments

### `-p`, `--port PORT`
Port number to run the server on.
- **Default**: 5000
- **Range**: 1-65535
- **Example**: `--port 8000` or `-p 3000`

### `--host HOST`
Network interface address to bind to.
- **Default**: 0.0.0.0 (all interfaces)
- **Common values**:
  - `0.0.0.0` - All interfaces (accessible from any network)
  - `127.0.0.1` - Localhost only (not accessible from network)
  - `192.168.1.100` - Specific IP address
- **Example**: `--host 127.0.0.1`

### `--debug`
Run Flask in debug mode.
- **Features**: Auto-reload, better error pages, debugger
- **Example**: `--debug`

### `-h`, `--help`
Display help message and usage examples.

## Port Considerations

### Port Availability
If a port is already in use, you'll see an error:
```
OSError: [Errno 48] Address already in use
```

**Solutions**:
1. Use a different port: `./run.sh --port 5001`
2. Stop the process using the port
3. On Linux/Mac, find process: `lsof -i :5000`

### Common Port Issues

**Port 5000 in use**
```bash
# Try port 5001
./run.sh --port 5001

# Or check what's using port 5000
lsof -i :5000
```

**Need to run multiple instances**
```bash
# Terminal 1
./run.sh --port 5000

# Terminal 2
./run.sh --port 5001

# Terminal 3
./run.sh --port 5002
```

## Network Access

### Local Only (Recommended for Development)
```bash
./run.sh --host 127.0.0.1 --port 5000
# Access at: http://127.0.0.1:5000
```

### Network Accessible (Production)
```bash
./run.sh --host 0.0.0.0 --port 5000
# Access at: http://<your-ip>:5000
```

### Specific Interface
```bash
./run.sh --host 192.168.1.100 --port 5000
# Access at: http://192.168.1.100:5000
```

## Common Use Cases

### Development (Localhost Only)
```bash
./run.sh --host 127.0.0.1 --debug
```
- Only accessible locally
- Auto-reloads on code changes
- Enhanced error messages

### Testing on Different Port
```bash
./run.sh --port 8888
```
- Doesn't conflict with other services
- Test with browser at http://localhost:8888

### Production Deployment
```bash
./run.sh --host 0.0.0.0 --port 5000
```
- Accessible from network
- Behind reverse proxy (nginx, Apache)
- No debug mode

### Multiple Instances
```bash
# Instance 1
./run.sh --port 5000 &

# Instance 2
./run.sh --port 5001 &

# Instance 3
./run.sh --port 5002 &
```

## Environment Variables

You can also use environment variables (though command-line arguments take precedence):

```bash
# Linux/Mac
export AMS2_PORT=8000
export AMS2_HOST=127.0.0.1
./run.sh

# Windows (PowerShell)
$env:AMS2_PORT=8000
$env:AMS2_HOST=127.0.0.1
run.bat
```

## Firewall and Network

### Opening Port on Firewall
To make the server accessible from other machines:

**Linux (ufw)**
```bash
sudo ufw allow 5000
```

**Linux (iptables)**
```bash
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
```

**Windows (Command Prompt as Admin)**
```bash
netsh advfirewall firewall add rule name="AMS2 Race Recorder" dir=in action=allow protocol=tcp localport=5000
```

### Testing Network Access
```bash
# From another machine
curl http://<server-ip>:5000

# Check if port is open
telnet <server-ip> 5000
```

## Docker Deployment

If running in Docker, expose the port:

```dockerfile
# Dockerfile
EXPOSE 5000
CMD ["./run.sh", "--host", "0.0.0.0", "--port", "5000"]
```

```bash
# Run with custom port
docker run -p 8000:5000 ams2-recorder
```

## Troubleshooting

### "Address already in use" Error
```bash
# Find what's using the port
lsof -i :5000              # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill the process (Linux/Mac)
kill -9 <PID>

# Or use a different port
./run.sh --port 5001
```

### Can't Connect from Another Machine
```bash
# Make sure to use 0.0.0.0 or specific IP
./run.sh --host 0.0.0.0

# Test locally first
./run.sh --host 127.0.0.1
curl http://127.0.0.1:5000

# Then test from another machine
curl http://<your-ip>:5000
```

### Connection Timeout
- Check firewall allows the port
- Verify server is actually running
- Try `lsof -i :5000` to confirm listening

## Performance Notes

- Port numbers don't affect performance
- Higher port numbers (>1024) don't require root/admin
- Use port <1024 only if necessary (requires elevated privileges)

## Security Best Practices

1. **Development**: Use `--host 127.0.0.1` to restrict access
2. **Production**: Use reverse proxy (nginx) with SSL/TLS
3. **Firewall**: Only expose necessary ports
4. **Non-standard ports**: Consider using ports >5000 for less-known services
5. **Root ports**: Avoid ports <1024 unless absolutely necessary

## Reference

### Argument Examples
| Use Case | Command |
|----------|---------|
| Default | `./run.sh` |
| Custom port | `./run.sh --port 8080` |
| Localhost only | `./run.sh --host 127.0.0.1` |
| Debug mode | `./run.sh --debug` |
| All options | `./run.sh --port 8080 --host 127.0.0.1 --debug` |
| Help | `./run.sh --help` |

### Common Ports
| Port | Service | Notes |
|------|---------|-------|
| 80 | HTTP | Requires admin/root |
| 443 | HTTPS | Requires admin/root |
| 3000 | Development | Node.js default |
| 5000 | Development | Flask default |
| 5001 | Alternative | Avoid conflicts |
| 8000 | Alternative | Common web dev |
| 8080 | Alternative | Common proxy |
| 8888 | Alternative | Easy to remember |
| 9000+ | Safe range | Avoid common ports |
