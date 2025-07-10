#!/bin/bash

# Configuration
REMOTE_USER="ai"
REMOTE_HOST="ai-develop"
REMOTE_BASE_DIR="/home/ai"
REMOTE_CHROMA_DIR="$REMOTE_BASE_DIR/chroma"
REMOTE_SNAPSHOT_DIR="$REMOTE_BASE_DIR/db-snapshots"
TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
SNAPSHOT_NAME="db-$TIMESTAMP"

# 1. Rename remote chroma dir to db-{datetime} and move to db-snapshots
echo "Archiving remote chroma directory..."
ssh $REMOTE_USER@$REMOTE_HOST << EOF
    mkdir -p $REMOTE_SNAPSHOT_DIR
    if [ -d "$REMOTE_CHROMA_DIR" ]; then
        mv "$REMOTE_CHROMA_DIR" "$REMOTE_SNAPSHOT_DIR/$SNAPSHOT_NAME"
        echo "Renamed and moved to $REMOTE_SNAPSHOT_DIR/$SNAPSHOT_NAME"
    else
        echo "No existing chroma directory found on remote."
    fi
EOF

# 2. Copy local chroma dir to remote
echo "Copying local chroma directory to remote..."
scp -r ./chroma $REMOTE_USER@$REMOTE_HOST:$REMOTE_CHROMA_DIR

echo "Sync complete."

