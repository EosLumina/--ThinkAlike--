#!/bin/bash

# === Configuration ===
REPO="EosLumina/--ThinkAlike--"
BRANCH="main"
LIMIT=50 # How many recent failed runs to fetch
LOG_FILE="github_actions_failures_summary.log"
# === End Configuration ===

echo "Starting GitHub Actions failure analysis for $REPO on branch $BRANCH..."
echo "Fetching details for the latest $LIMIT failed runs."
echo "Output will be saved to $LOG_FILE"
echo "This may take a few minutes..."

# Check if gh is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI 'gh' not found."
    echo "Please install it (see: https://cli.github.com/) and authenticate using 'gh auth login'."
    exit 1
fi

# Check gh authentication status - it's crucial for accessing repository data
if ! gh auth status &> /dev/null; then
    echo "Error: GitHub CLI 'gh' is not authenticated."
    echo "Please run 'gh auth login' and follow the prompts."
    exit 1
fi

# Check if jq is installed (useful for parsing JSON output from gh)
if ! command -v jq &> /dev/null; then
    echo "Warning: 'jq' command not found. Trying to proceed without it, but JSON parsing might be less reliable."
    # Consider installing jq if possible (e.g., sudo apt-get update && sudo apt-get install jq)
fi

# Initialize/Clear the log file
> "$LOG_FILE"
echo "Initialized log file: $LOG_FILE"
echo "==================================================" >> "$LOG_FILE"
echo " GitHub Actions Failure Summary" >> "$LOG_FILE"
echo " Repository: $REPO" >> "$LOG_FILE"
echo " Branch: $BRANCH" >> "$LOG_FILE"
echo " Date: $(date)" >> "$LOG_FILE"
echo "==================================================" >> "$LOG_FILE"


# Get the IDs of the latest failed runs using gh CLI and jq if available
echo "Fetching failed run IDs..."
if command -v jq &> /dev/null; then
    FAILED_RUN_IDS=$(gh run list --repo "$REPO" --branch "$BRANCH" --status failure --limit "$LIMIT" --json databaseId --jq '.[].databaseId' 2>/dev/null)
else
    # Fallback without jq - less robust parsing
    FAILED_RUN_IDS=$(gh run list --repo "$REPO" --branch "$BRANCH" --status failure --limit "$LIMIT" | awk 'NR>1 {print $7}') # Attempt to get ID from column 7
fi


if [[ -z "$FAILED_RUN_IDS" ]]; then
    echo "No recent failed runs found for branch '$BRANCH' within the limit of $LIMIT."
    echo "No recent failed runs found." >> "$LOG_FILE"
    exit 0
fi

echo "Found $(echo "$FAILED_RUN_IDS" | wc -w) failed run(s) to process."

# Loop through each failed run ID
TOTAL_RUNS=$(echo "$FAILED_RUN_IDS" | wc -w)
COUNT=0
for RUN_ID in $FAILED_RUN_IDS; do
    COUNT=$((COUNT + 1))
    echo "Processing Run ID: $RUN_ID ($COUNT/$TOTAL_RUNS)..."

    # Get run details (Workflow Name, Timestamp, URL) using JSON if jq is available
    if command -v jq &> /dev/null; then
        RUN_INFO=$(gh run view "$RUN_ID" --repo "$REPO" --json name,createdAt,url --jq '{name: .name, createdAt: .createdAt, url: .url}' 2>/dev/null)
        WORKFLOW_NAME=$(echo "$RUN_INFO" | jq -r '.name // "N/A"')
        CREATED_AT=$(echo "$RUN_INFO" | jq -r '.createdAt // "N/A"')
        RUN_URL=$(echo "$RUN_INFO" | jq -r '.url // "N/A"')
    else
        # Fallback without jq - might be less accurate
        RUN_DETAILS_RAW=$(gh run view "$RUN_ID" --repo "$REPO" 2>/dev/null)
        WORKFLOW_NAME=$(echo "$RUN_DETAILS_RAW" | grep 'workflow:' | cut -d ':' -f 2- | xargs || echo "N/A")
        CREATED_AT=$(echo "$RUN_DETAILS_RAW" | grep 'created:' | cut -d ':' -f 2- | xargs || echo "N/A")
        RUN_URL=$(gh run view "$RUN_ID" --repo "$REPO" --web 2>/dev/null || echo "N/A") # Get web URL directly
    fi


    # Append basic info to log
    echo "" >> "$LOG_FILE"
    echo "--- Run ID: $RUN_ID ---" >> "$LOG_FILE"
    echo "Workflow: $WORKFLOW_NAME" >> "$LOG_FILE"
    echo "Timestamp: $CREATED_AT" >> "$LOG_FILE"
    echo "URL: $RUN_URL" >> "$LOG_FILE"

    # Get failed job logs (this fetches only the sections around failures)
    echo "  Fetching failed steps log summary..."
    FAILED_LOG_SNIPPET=$(gh run view "$RUN_ID" --repo "$REPO" --log-failed 2>&1) # Capture stderr too

    if [ $? -ne 0 ] || [[ "$FAILED_LOG_SNIPPET" == *"no failed steps found"* ]] || [[ -z "$FAILED_LOG_SNIPPET" ]]; then
         echo "  No specific failed steps found via --log-failed, or error fetching log."
         echo "Failed Steps Log: (Could not retrieve or none found via --log-failed)" >> "$LOG_FILE"
         # You could add a fallback here to try and get the full log if needed, but it can be very large.
         # e.g., gh run view "$RUN_ID" --repo "$REPO" --log | tail -n 50 >> "$LOG_FILE"
    else
        echo "  Appending failed log snippet..."
        echo "" >> "$LOG_FILE"
        echo "Failed Steps Log Snippet:" >> "$LOG_FILE"
        # Add indentation for readability in the log file
        echo "$FAILED_LOG_SNIPPET" | sed 's/^/  /' >> "$LOG_FILE"
    fi

    echo "--------------------------------------------------" >> "$LOG_FILE"
    sleep 0.5 # Small delay to be polite to the GitHub API
done

echo "Analysis complete."
echo "Summary of the latest $LIMIT failed runs saved to $LOG_FILE"
