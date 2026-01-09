# Quick Start Guide

## Running the Web Server

### Default (Port 5000)
```bash
# Linux/Mac
cd server
./run.sh

# Windows
cd server
run.bat
```
Then open http://localhost:5000

### Custom Port
```bash
# Linux/Mac: Port 8000
./run.sh --port 8000

# Windows: Port 8000
run.bat --port 8000
```

### Localhost Only (Development)
```bash
# Linux/Mac
./run.sh --host 127.0.0.1

# Windows
run.bat --host 127.0.0.1
```

### Debug Mode
```bash
# Linux/Mac
./run.sh --debug

# Windows
run.bat --debug
```

### All Options
```bash
# Linux/Mac
./run.sh --port 8080 --host 127.0.0.1 --debug

# Windows
run.bat --port 8080 --host 127.0.0.1 --debug
```

## Getting Help
```bash
# Linux/Mac
./run.sh --help

# Windows
run.bat --help
```

## Common Scenarios

| Scenario | Command |
|----------|---------|
| Default | `./run.sh` |
| Port 8000 | `./run.sh --port 8000` |
| Localhost only | `./run.sh --host 127.0.0.1` |
| Debug mode | `./run.sh --debug` |
| Help | `./run.sh --help` |

## Stopping the Server
Press **Ctrl+C** to stop the server.

## Port Already in Use?
Try a different port:
```bash
./run.sh --port 5001
./run.sh --port 8000
./run.sh --port 3000
```

## More Information
- See `PORT_CONFIGURATION.md` for detailed port configuration
- See `TESTING.md` for running tests
- See main `README.md` for full documentation
