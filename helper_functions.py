def update_script():
    
    script_path = os.path.join(os.path.dirname(__file__), 'update.bat')
    if not os.path.exists(script_path):
        exc_handler('error', f"{script_path} does not exist")
        return

    # Function to run the batch script and read its output
    def run_script():
        process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                yield output.strip()
        rc = process.poll()
        return rc

    # Run the script with a progress bar
    try:
        with Progress() as progress:
            task = progress.add_task(f":thumbs_up:[{SUCCESS_COLOR}] log [/{SUCCESS_COLOR}]Updating...", total=1000)
            previous_percentage = 0

            for line in run_script():
                if line.isdigit():
                    current_percentage = int(line)
                    # Interpolate between previous and current percentage
                    for i in range(previous_percentage + 1, current_percentage + 1):
                        progress.update(task, completed=i)
                        time.sleep(0.001)  # Adjust the sleep time for smoother/slower updates
                    previous_percentage = current_percentage

        exc_handler('success', f"Update complete.")
    except Exception as e:
        exc_handler('error', f"Update failed: {e}")

# exc_handler("option", f"message")
def exc_handler(message_type, message):
    if message_type == "error":
        console.print(f":thumbs_down:[{ERROR_COLOR}] log [/{ERROR_COLOR}][{ERR_SUCC_COLOR}]{message}[/{ERR_SUCC_COLOR}]")
    elif message_type == "success":
        console.print(f":thumbs_up:[{SUCCESS_COLOR}] log [/{SUCCESS_COLOR}][{ERR_SUCC_COLOR}]{message}[/{ERR_SUCC_COLOR}]")
    else:
        print(message)  # Default print without any color
