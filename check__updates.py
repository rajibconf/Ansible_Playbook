import json
import subprocess
from datetime import datetime

def get_updates():
    try:
        # Run the command to check for upgradable packages
        result = subprocess.run(
            ["apt", "list", "--upgradable"],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True
        )
        
        # Parse the output and extract details
        lines = result.stdout.strip().split("\n")
        updates = []

        for line in lines[1:]:  # Skip the first line (Listing...)
            parts = line.split()
            if len(parts) >= 3:
                package, version, repo = parts[0], parts[1], parts[2]
                arch = parts[3] if len(parts) > 3 else "unknown"
                current_version = parts[-1] if len(parts) > 4 else "N/A"
                updates.append({
                    "Package": package,
                    "Repository": repo,
                    "Version": version,
                    "Architecture": arch,
                    "Current Version": current_version
                })
        return updates
    except Exception as e:
        print(f"Error while fetching updates: {e}")
        return []

def generate_report():
    # Get current date and time
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Fetch updates
    updates = get_updates()

    # Prepare the report in JSON format
    report = {
        "System Update Check": now,
        "Available Updates": updates
    }

    return report

if __name__ == "__main__":
    # Generate the report
    report = generate_report()

    # Print the report in JSON format
    print(json.dumps(report, indent=2))
