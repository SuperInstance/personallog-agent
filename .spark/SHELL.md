# Spark Shell — personallog-agent

## Protocol
Version: 1.0 | Storage: `.spark/` directory

## What is personallog-agent
Tracks personallog activities and operations.
Part of the Cocapn Fleet — domain agent with PLATO integration.

## Rooms
- **domain/** — what this agent does
- **lessons/** — what happened
- **active/** — what's happening now
- **decisions/** — choices made
- **questions/** — what we don't know

## Connection to Fleet
Bootstrap Spark → Bootstrap Bomb → PLATO → greenhorn → personallog-agent

See: github.com/SuperInstance/personallog-agent
